# import General libraries
from datetime import date, timedelta
from html import escape
import logging
import pandas as pd
import streamlit as st
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# import my CRUD files
from autoren import create_author, read_authors
from buecher import (
    create_buch,
    delete_buecher,
    read_available_books,
    read_book_author_ids,
    read_book_locations,
    read_buecher,
    update_buecher,
)
from freund import create_friend, delete_friend, read_friends, update_friend
from genres import create_genre, delete_genre, read_genres, update_genre
from leihgaben import create_loan, read_loan_overview, read_loans, return_book
from standort import create_location, delete_location, read_locations, update_location

DASHBOARD_STYLE = """
<style>
    .stApp { background: #f8f7f3; color: #242032; }
    [data-testid="stHeader"] { background: #f8f7f3; }
    [data-testid="stSidebar"] { background: #eeebf5; border-right: 1px solid #ded9e8; }
    [data-testid="stSidebar"] [data-testid="stHeading"] h2 { color: #322452; }
    .stMainBlockContainer { max-width: 1300px; padding-top: 3rem; }
    [data-testid="stMetric"] { background: #fff; border-color: #e6e0ec; border-radius: 14px; }
    [data-testid="stMetricValue"] { color: #352452; font-weight: 700; }
    [data-testid="stForm"] { background: #fff; border-radius: 14px; }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        width: 100%; padding: .5rem .65rem; border-radius: 9px;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: #ded0ec; color: #362044;
    }
    .st-key-library_hero {
        position: relative; overflow: hidden; isolation: isolate;
        background: linear-gradient(110deg, #431938, #55274e);
        color: #fff; border-radius: 20px;
        padding: clamp(1.3rem, 4vw, 2.7rem); margin-bottom: .5rem;
    }
    .st-key-library_hero::after {
        content: ""; position: absolute; z-index: -1; right: -3rem; top: -6rem;
        width: 23rem; height: 23rem; border-radius: 50%;
        background: repeating-radial-gradient(circle at center,
            transparent 0 18px, #ffffff15 19px 20px, transparent 21px 32px);
        pointer-events: none;
    }
    .library-hero-heading h1 {
        font-family: "DM Serif Display", Georgia, serif; font-weight: 500;
        color: #fff; font-size: clamp(2.1rem, 5vw, 3.75rem);
        line-height: 1.05; margin: 0; padding: 0;
    }
    .library-hero-heading p { color: #f3e6f3; margin: .75rem 0 .6rem; }
    .st-key-library_hero button {
        background: #fff; border: 1px solid #e8dceb; color: #431938;
    }
    .st-key-overview_cards button {
        justify-content: flex-start; text-align: left; position: relative;
        min-height: 6rem; padding: .7rem 1.65rem .7rem .9rem;
        border: 1px solid #d8cbdc; border-radius: 12px; color: #2b2030;
        background: #fff;
    }
    .st-key-overview_cards button::after {
        content: "›"; position: absolute; right: .7rem; font-size: 1.5rem;
        color: #5c3861;
    }
    .st-key-overview_cards button strong { font-size: 1.75rem; line-height: 1.2; }
    .st-key-overview_cards button[kind="primary"],
    .st-key-overview_cards button:hover {
        background: #efe3f5; color: #2b2030; border-color: #6b426b;
    }
    .st-key-clear_overview_filter button {
        background: #eadcf3; border-color: transparent; color: #402744;
        border-radius: 100px;
    }
    .library-table-wrap {
        overflow-x: auto; border: 1px solid #cfc2d4; border-radius: 11px;
    }
    .library-table {
        width: 100%; border-collapse: collapse; text-align: left;
        color: #27202d; background: #fffdfa; font-size: .91rem;
    }
    .library-table th, .library-table td { padding: .62rem .9rem; }
    .library-table th { background: #e7dcec; white-space: nowrap; }
    .library-table td { border-top: 1px solid #e5dce6; }
    .status-pill { display: inline-block; padding: .12rem .65rem; border-radius: 99px; white-space: nowrap; }
    .status-pill.available { background: #d4eed8; color: #19482a; }
    .status-pill.on-loan { background: #ead8fb; color: #422557; }
    .status-pill.not-lendable { background: #e5e2e8; color: #423d49; }
    .library-table .overdue-row td { background: #fde1e1; color: #661d25; }
    .status-pill.overdue { background: #f8bfc2; color: #6a161e; font-weight: 650; }
    @media (max-width: 700px) {
        .st-key-overview_cards button { min-height: 4.5rem; }
        .library-table th, .library-table td { padding: .55rem .6rem; }
    }
</style>
"""


# define a function to do a "action" and show a "message". we used *args and **kwars, because we need recall this function in different ways.
# action is different function from other files like as create_bucher()
def save(action, message, *args, dependency_message=None, **kwargs):
    """Write once, display a message, and reload the data."""
    try:
        result = action(*args, **kwargs)
        if result == 0:
            st.error(
                "The record was not found or is no longer eligible for this action."
            )
            return
    except ValueError as error:
        st.error(str(error))
        return
    except IntegrityError as error:
        code = error.orig.args[0]  # extracting the original error code from MySQL
        if code == 1062:
            st.error("This value is already registered.")
        elif code == 1452:
            st.error("One of the selected items no longer exists.")
        elif code == 1451 and dependency_message:
            st.error(dependency_message)
        else:
            logging.exception("Database constraint rejected the change")
            st.error("A database constraint prevented this change.")
        return
    except SQLAlchemyError:
        logging.exception("Database write failed")
        st.error("Could not save. See the terminal for details.")
        return

    st.session_state["notice"] = message  # save a success meassage in session_state
    st.rerun()  # updating the page but we keep the last message in session_state


# create a dictionary from Freund table. rows is as a dataframe.id_column is the FreundID
# this function create a dictionary and show them as a line to line in webscreen
def person_labels(rows, id_column):
    return {  # return a dictionary
        row[id_column]: f"{row['Vorname']} {row['Nachname']} (#{row[id_column]})"
        for row in rows.to_dict("records")
    }


# create a dictionary from Buch table. rows is as a dataframe.id_column is the BuchID
# this function create a dictionary and show them as a line to line in webscreen
def book_labels(rows):
    return {row.BuchID: f"{row.Titel} (#{row.BuchID})" for row in rows.itertuples()}


# create a menu list that user can select it
# "label" is the name of menu list. "labels" is dictionary of name and IDs.
# retuen a menu list(Select box).
# "label" is menu title, "option" is the menu options(id of option), "index" is the defualt option.
# "format_func" is the format of showing the name of options id."key" is the wiegdt ID.
def select_id(label, labels, current=None, key=None):
    options = list(labels)
    index = (
        options.index(current) if current in labels else None
    )  # if the IDs exist in dictionary then find the location of that in list
    return st.selectbox(label, options, index=index, format_func=labels.get, key=key)


# create a general function to delete a information
# "label" is the record type like as book. "labels" is dictionary of recordname and IDs.
#"delete" is the delete function
#dependency_message is a message when there is a dependency
def delete_form(label, labels, delete, dependency_message, *, note=None):
    if not labels:
        st.info(f"There is no {label} to delete.")
        return
    #create a form for deleting
    with st.form(f"delete_{label}", enter_to_submit=False):
        item_id = select_id(f"Select a {label} to delete", labels)
        if note:
            st.caption(note)
        confirmed = st.checkbox("I confirm this deletion")#create a checkbox that user confirm it
        submitted = st.form_submit_button("Delete")#send a form

    if submitted:
        if item_id is None or not confirmed:
            st.error(f"Select a {label} and confirm the deletion.")
        else:
            save(
                delete,
                f"{label.capitalize()} deleted.",
                item_id,
                dependency_message=dependency_message,
            )


def loans_page():
    operation = st.radio(
        "Action",
        ["Lend a book", "Record return", "Loan history"],
        horizontal=True,
        key="loan_action",
    )
    if operation == "Loan history":
        loan_history_page()
        return

    if operation == "Lend a book":
        available = read_available_books()
        friends = read_friends()
        if available.empty or friends.empty:
            st.info("You need an available book and a friend to record a loan.")
            return

        with st.form("new_loan"):
            book_id = select_id("Book", book_labels(available))
            friend_id = select_id("Friend", person_labels(friends, "FreundID"))
            loan_date = st.date_input("Loan date", value=date.today())
            due_date = st.date_input(
                "Due date", value=date.today() + timedelta(days=14)
            )
            submitted = st.form_submit_button("Record loan")

        if submitted:
            if book_id is None or friend_id is None:
                st.error("Select a book and a friend.")
            else:
                save(
                    create_loan,
                    "Loan recorded.",
                    book_id,
                    friend_id,
                    loan_date,
                    due_date,
                )

    else:
        active = read_loans(active_only=True)
        if active.empty:
            st.info("There are no active loans.")
            return

        labels = {
            row.LeihID: f"{row.Titel} — {row.Vorname} {row.Nachname} (#{row.LeihID})"
            for row in active.itertuples()
        }
        with st.form("return_loan"):
            loan_id = select_id("Active loan", labels)
            returned = st.date_input("Return date", value=date.today())
            submitted = st.form_submit_button("Record return")

        if submitted:
            if loan_id is None:
                st.error("Select a loan.")
            else:
                loan = active.loc[active["LeihID"].eq(loan_id)].iloc[0]
                if returned < pd.Timestamp(loan["Verleihdatum"]).date():
                    st.error("The return date cannot be before the loan date.")
                else:
                    save(return_book, "Return recorded.", loan_id, returned)


def books_page():
    books = read_buecher(include_status=True)
    catalog = books[["BuchID", "Titel", "Genre", "Standort", "Status"]]
    st.dataframe(
        catalog.rename(
            columns={
                "BuchID": "Book ID",
                "Titel": "Title",
                "Standort": "Storage location",
            }
        ),
        hide_index=True,
    )

    operation = st.radio(
        "Action",
        ["Add book", "Edit book", "Delete book"],
        horizontal=True,
        key="book_action",
    )
    if operation == "Delete book":
        delete_form(
            "book",
            book_labels(books),
            delete_buecher,
            "This book has a loan history and cannot be deleted.",
            note="Deleting a book also removes its author links.",
        )
        return

    book_id = None
    current = {}
    if operation == "Edit book":
        if books.empty:
            st.info("No books have been added yet.")
            return
        book_id = select_id("Book to edit", book_labels(books))
        if book_id is None:
            return
        current = books.loc[books["BuchID"].eq(book_id)].iloc[0].to_dict()

    genres = read_genres()
    locations = read_locations()
    if genres.empty or locations.empty:
        st.info("Add at least one genre and one storage location first.")
        return

    with st.expander("Add a new author"):
        with st.form("new_author"):
            first = st.text_input("Author first name")
            last = st.text_input("Author last name")
            add_author = st.form_submit_button("Add author")
        if add_author:
            save(create_author, "Author added.", first, last)

    authors = person_labels(read_authors(), "AutorID")
    current_authors = read_book_author_ids(book_id) if book_id is not None else []
    genre_labels = dict(zip(genres["GenreID"], genres["Name"]))
    location_labels = dict(zip(locations["StandortID"], locations["Bezeichnung"]))

    with st.form(f"book_{book_id}"):
        title = st.text_input("Title", value=current.get("Titel", ""), max_chars=255)
        genre_id = select_id("Genre", genre_labels, current.get("GenreID"))
        location_id = select_id(
            "Storage location", location_labels, current.get("StandortID")
        )
        author_ids = st.multiselect(
            "Authors", list(authors), default=current_authors, format_func=authors.get
        )
        isbn_value = current.get("ISBN")
        isbn = st.text_input(
            "ISBN", value="" if pd.isna(isbn_value) else str(isbn_value)
        )
        lendable = st.checkbox("Lendable", value=bool(current.get("Verleihbar", 1)))
        submitted = st.form_submit_button("Save book")

    if submitted:
        if genre_id is None or location_id is None:
            st.error("Select a genre and a storage location.")
        else:
            if book_id is None:
                save(
                    create_buch,
                    "Book added.",
                    title,
                    genre_id,
                    location_id,
                    isbn,
                    int(lendable),
                    author_ids=author_ids,
                )
            else:
                save(
                    update_buecher,
                    "Book updated.",
                    book_id,
                    title,
                    genre_id=genre_id,
                    standort_id=location_id,
                    isbn=isbn,
                    lendable=lendable,
                    author_ids=author_ids,
                )


def friends_page():
    friends = read_friends()
    st.dataframe(
        friends.rename(
            columns={
                "FreundID": "Friend ID",
                "Vorname": "First name",
                "Nachname": "Last name",
                "Telefon": "Phone",
            }
        ),
        hide_index=True,
    )
    operation = st.radio(
        "Action",
        ["Add friend", "Edit friend", "Delete friend"],
        horizontal=True,
        key="friend_action",
    )
    if operation == "Delete friend":
        delete_form(
            "friend",
            person_labels(friends, "FreundID"),
            delete_friend,
            "This friend has a loan history and cannot be deleted.",
        )
        return

    friend_id = None
    current = {}
    if operation == "Edit friend":
        if friends.empty:
            st.info("No friends have been added yet.")
            return
        friend_id = select_id("Friend to edit", person_labels(friends, "FreundID"))
        if friend_id is None:
            return
        current = (
            friends.loc[friends["FreundID"].eq(friend_id)].iloc[0].fillna("").to_dict()
        )

    with st.form(f"friend_{friend_id}"):
        first = st.text_input(
            "First name", value=current.get("Vorname", ""), max_chars=100
        )
        last = st.text_input(
            "Last name", value=current.get("Nachname", ""), max_chars=100
        )
        phone = st.text_input("Phone", value=current.get("Telefon", ""), max_chars=30)
        email = st.text_input("Email", value=current.get("Email", ""), max_chars=255)
        submitted = st.form_submit_button("Save friend")

    if submitted:
        if friend_id is None:
            save(create_friend, "Friend added.", first, last, phone, email)
        else:
            save(
                update_friend,
                "Friend details saved.",
                friend_id,
                first,
                last,
                phone,
                email,
            )


def named_page(
    rows, id_column, name_column, create, update, delete, label, dependency_message
):
    st.dataframe(
        rows.rename(columns={id_column: "ID", name_column: "Name"}), hide_index=True
    )
    operation = st.radio(
        "Action", ["Add", "Edit", "Delete"], horizontal=True, key=id_column
    )
    item_id = None
    labels = dict(zip(rows[id_column], rows[name_column]))

    if operation == "Delete":
        delete_form(label, labels, delete, dependency_message)
        return

    if operation == "Edit":
        if not labels:
            st.info("Add an item first.")
            return
        item_id = select_id(f"Select a {label}", labels)
        if item_id is None:
            return

    with st.form(f"{id_column}_{item_id}"):
        name = st.text_input("Name", value=labels.get(item_id, ""))
        submitted = st.form_submit_button("Save")

    if submitted:
        if item_id is None:
            save(create, "New item added.", name)
        else:
            save(update, "Name saved.", item_id, name)


def filter_rows(rows, columns, term):
    if not term:
        return rows
    matches = rows[columns].apply(
        lambda column: column.astype("string").str.contains(
            term, case=False, regex=False, na=False
        )
    )
    return rows.loc[matches.any(axis=1)]


def display_table(rows):
    """Render dashboard tables with status pills and full-row overdue emphasis."""
    status_styles = {
        "Available": "available",
        "On loan": "on-loan",
        "Not lendable": "not-lendable",
        "Overdue": "overdue",
        "Returned": "available",
    }
    headers = "".join(
        f'<th scope="col">{escape(column)}</th>' for column in rows.columns
    )
    body = []
    for record in rows.to_dict("records"):
        row_class = ' class="overdue-row"' if record.get("Status") == "Overdue" else ""
        cells = []
        for column, value in record.items():
            if pd.isna(value):
                value = ""
            elif isinstance(value, pd.Timestamp):
                value = value.strftime("%d %b %Y")
            content = escape(str(value))
            if column == "Status" and value in status_styles:
                content = (
                    f'<span class="status-pill {status_styles[value]}">{content}</span>'
                )
            cells.append(f"<td>{content}</td>")
        body.append(f"<tr{row_class}>{''.join(cells)}</tr>")
    st.html(
        '<div class="library-table-wrap"><table class="library-table">'
        f"<thead><tr>{headers}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
    )


def loan_history_page():
    term = st.text_input(
        "Search by book title or borrower", key="history_search"
    ).strip()
    rows = filter_rows(read_loan_overview(), ["Title", "Borrower"], term)
    if rows.empty:
        st.info("No matching loans found.")
        return
    display_table(
        rows[["Title", "Borrower", "Loan date", "Due date", "Return date", "Status"]]
    )


def go_to(section, loan_action=None):
    st.session_state["library_section"] = section
    if loan_action is not None:
        st.session_state["loan_action"] = loan_action


def set_overview_filter(label):
    current = st.session_state.get("overview_filter")
    st.session_state["overview_filter"] = None if current == label else label


def dashboard_page():
    with st.container(key="library_hero"):
        st.html("""
            <div class="library-hero-heading">
                <h1>Liane’s Library</h1>
                <p>Find a book, check who has it, or record a loan or return.</p>
            </div>
        """)
        lend, return_action, add = st.columns(3)
        lend.button(
            "Lend a book",
            width="stretch",
            on_click=go_to,
            args=("Loans", "Lend a book"),
        )
        return_action.button(
            "Record return",
            width="stretch",
            on_click=go_to,
            args=("Loans", "Record return"),
        )
        add.button("Add a book", width="stretch", on_click=go_to, args=("Books",))

    books = read_book_locations()
    active = read_loan_overview(active_only=True).sort_values("Due date")
    overdue = active.loc[active["Status"].eq("Overdue")]
    available = books.loc[books["Status"].eq("Available")]
    selected = st.session_state.get("overview_filter")
    cards = {
        "Books in catalog": books["Book ID"].nunique(),
        "Available to lend": len(available),
        "Active loans": len(active),
        "Overdue loans": len(overdue),
    }
    with st.container(key="overview_cards"):
        for column, (label, count) in zip(st.columns(4), cards.items()):
            column.button(
                f"{label}  \n**{count}**",
                key="overview_" + label.lower().replace(" ", "_"),
                type="primary" if selected == label else "secondary",
                width="stretch",
                on_click=set_overview_filter,
                args=(label,),
            )

    st.subheader("Find a book")
    term = st.text_input(
        "Search by title, borrower, or shelf",
        placeholder="Search by title, borrower, or shelf",
        key="dashboard_search",
        label_visibility="collapsed",
    ).strip()
    if selected:
        st.button(
            f"{selected} ×",
            key="clear_overview_filter",
            on_click=set_overview_filter,
            args=(selected,),
            help="Clear the selected filter",
        )

    if selected in {"Active loans", "Overdue loans"}:
        matching_loans = overdue if selected == "Overdue loans" else active
        # Match shelf as well as title and borrower while searching active loans.
        shelves = books[["Book ID", "Shelf"]].drop_duplicates("Book ID")
        matching_loans = matching_loans.merge(
            shelves, how="left", left_on="BuchID", right_on="Book ID"
        )
        matching_loans = filter_rows(
            matching_loans, ["Title", "Borrower", "Shelf"], term
        )
        if matching_loans.empty:
            st.info("No loans match this filter.")
        else:
            display_table(matching_loans[["Title", "Borrower", "Due date", "Status"]])
    else:
        results = available if selected == "Available to lend" else books
        results = filter_rows(results, ["Title", "Borrower", "Shelf"], term)
        if results.empty:
            st.info("No books match this search.")
        else:
            if selected:
                st.caption(f"{len(results)} {'book' if len(results) == 1 else 'books'}")
            display_table(results[["Title", "Status", "Current location", "Shelf"]])

    st.subheader("Active loans")
    if active.empty:
        st.info("There are no active loans.")
    else:
        display_table(active[["Title", "Borrower", "Due date", "Status"]])


def main():
    st.set_page_config(page_title="Liane's Library", layout="wide")
    st.html(DASHBOARD_STYLE)
    st.sidebar.header("Liane’s Library")
    page = st.sidebar.radio(
        "Navigation",
        ["Overview", "Loans", "Books", "Friends", "Genres", "Storage locations"],
        key="library_section",
        label_visibility="collapsed",
    )
    if page != "Overview":
        st.title(page)
    notice = st.session_state.pop("notice", None)
    if notice:
        st.success(notice)

    try:
        if page == "Overview":
            dashboard_page()
        elif page == "Loans":
            loans_page()
        elif page == "Books":
            books_page()
        elif page == "Friends":
            friends_page()
        elif page == "Genres":
            named_page(
                read_genres(),
                "GenreID",
                "Name",
                create_genre,
                update_genre,
                delete_genre,
                "genre",
                "Assign the books to another genre before deleting this one.",
            )
        else:
            named_page(
                read_locations(),
                "StandortID",
                "Bezeichnung",
                create_location,
                update_location,
                delete_location,
                "storage location",
                "Move the books to another storage location before deleting this one.",
            )
    except SQLAlchemyError:
        logging.exception("Database read failed")
        st.error("Could not load data from MySQL. See the terminal for details.")


if __name__ == "__main__":
    main()
