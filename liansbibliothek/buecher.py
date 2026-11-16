import pandas as pd
from sqlalchemy import text  # for preparing SQL command to run
from sqlalchemy.exc import IntegrityError  # using to declare Error in Database
from database import engine  # getting connection string from database


# READ
def read_buecher(*, include_status=False):
    read_query = text("""
         SELECT
            b.BuchID,
            b.ISBN,
            b.Titel,
            b.GenreID,
            g.Name AS Genre,
            b.StandortID,
            s.Bezeichnung AS Standort,
            b.Verleihbar,
            CONCAT(f.Vorname, ' ', f.Nachname) AS Borrower,
            CASE
                WHEN l.LeihID IS NOT NULL THEN 'On loan'
                WHEN b.Verleihbar = 1 THEN 'Available'
                ELSE 'Not lendable'
            END AS Status
        FROM Buecher AS b
        JOIN Genres AS g
            ON b.GenreID = g.GenreID
        JOIN Standorte AS s
            ON b.StandortID = s.StandortID
        LEFT JOIN Leihgaben AS l ON l.LeihID = (
            SELECT MAX(active.LeihID)
            FROM Leihgaben AS active
            WHERE active.BuchID = b.BuchID AND active.Rueckgabedatum IS NULL
        )
        LEFT JOIN Freunde AS f ON f.FreundID = l.FreundID
        ORDER BY b.BuchID
    """)

    with engine.connect() as connection:  # open a database connection and put it in 'connection'
        df = pd.read_sql(
            read_query, con=connection
        )  # run read_sql function and store the result in df as dataframe

    return df if include_status else df.drop(columns=["Borrower", "Status"])


def read_available_books():
    books = read_buecher(include_status=True)
    return books.loc[books["Status"].eq("Available")]


_UNCHANGED = object()


def book_title(value):
    value = value.strip()
    if not value or len(value) > 255:
        raise ValueError("The title must be between 1 and 255 characters.")
    return value


def book_isbn(value):
    if value is not None:
        value = value.strip() or None
    if value is not None and len(value) > 13:
        raise ValueError("ISBN must be at most 13 characters.")
    return value


def replace_book_authors(connection, book_id, author_ids):
    connection.execute(
        text("DELETE FROM Buch_Autor WHERE BuchID = :book_id"),
        {"book_id": book_id},
    )
    links = [
        {"book_id": book_id, "author_id": author_id}
        for author_id in dict.fromkeys(author_ids)
    ]
    if links:
        connection.execute(
            text("""
                INSERT INTO Buch_Autor (BuchID, AutorID)
                VALUES (:book_id, :author_id)
            """),
            links,
        )


def create_buch(
    title, genre_id, standort_id, isbn=None, Verleihbar=0, *, author_ids=()
):
    """Insert a book and its author links, then return the new BuchID."""
    if Verleihbar not in (0, 1):
        raise ValueError("Verleihbar must be 0 (not lendable) or 1 (lendable).")

    query = text("""
        INSERT INTO Buecher (Titel, GenreID, StandortID, ISBN, Verleihbar)
        VALUES (:title, :genre_id, :standort_id, :isbn, :lendable)
    """)
    values = {
        "title": book_title(title),
        "genre_id": genre_id,
        "standort_id": standort_id,
        "isbn": book_isbn(isbn),
        "lendable": int(Verleihbar),
    }
    with engine.begin() as connection:
        book_id = connection.execute(query, values).lastrowid
        if author_ids:
            replace_book_authors(connection, book_id, author_ids)
        return book_id


def update_buecher(
    buch_id,
    buch_title,
    *,
    genre_id=None,
    standort_id=None,
    isbn=_UNCHANGED,
    lendable=None,
    author_ids=None,
):
    """Update book fields and, when supplied, replace its author links."""
    if lendable is not None and lendable not in (0, 1):
        raise ValueError("Lendable must be 0 or 1.")
    change_isbn = isbn is not _UNCHANGED
    query = text("""
        UPDATE Buecher
        SET Titel = :title,
            GenreID = COALESCE(:genre_id, GenreID),
            StandortID = COALESCE(:standort_id, StandortID),
            ISBN = CASE WHEN :change_isbn = 1 THEN :isbn ELSE ISBN END,
            Verleihbar = COALESCE(:lendable, Verleihbar)
        WHERE BuchID = :book_id
    """)
    values = {
        "book_id": buch_id,
        "title": book_title(buch_title),
        "genre_id": genre_id,
        "standort_id": standort_id,
        "change_isbn": int(change_isbn),
        "isbn": book_isbn(isbn) if change_isbn else None,
        "lendable": int(lendable) if lendable is not None else None,
    }
    with engine.begin() as connection:
        count = connection.execute(query, values).rowcount
        if count and author_ids is not None:
            replace_book_authors(connection, buch_id, author_ids)
        return count


def read_book_author_ids(book_id):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
            SELECT AutorID FROM Buch_Autor WHERE BuchID = :book_id
        """),
            {"book_id": book_id},
        )
        return list(result.scalars())


def read_book_locations():
    books = read_buecher(include_status=True).rename(
        columns={"BuchID": "Book ID", "Titel": "Title", "Standort": "Shelf"}
    )
    books["Borrower"] = books["Borrower"].fillna("")
    books["Current location"] = books["Shelf"].where(
        books["Status"].ne("On loan"), "With " + books["Borrower"]
    )
    return books.sort_values(["Title", "Book ID"])[
        ["Book ID", "Title", "Status", "Current location", "Borrower", "Shelf"]
    ]


# DELETE
def delete_buecher(buch_id):
    delete_query = text("""
        DELETE FROM Buecher
        WHERE BuchID = :buch_id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            delete_query,
            {"buch_id": buch_id},
        )
    return result.rowcount


# MENU
"""def main():
    try:
        while True:
            print("\n--- Books Menu ---")
            print("1. Show books")
            print("2. Add book")
            print("3. Edit book title")
            print("4. Delete book")
            print("0. Exit")

            try:
                choice = int(input("Choose an operation: "))

                if choice == 0:
                    break

                elif choice == 1:
                    books = read_buecher()

                    if books.empty:
                        print("No books found.")
                    else:
                        print(books.to_string(index=False))

                elif choice == 2:
                    # Show valid genre and location IDs.
                    with engine.connect() as connection:
                        genres = pd.read_sql(
                            text("SELECT * FROM Genres"),
                            con=connection,
                        )
                        locations = pd.read_sql(
                            text("SELECT * FROM Standorte"),
                            con=connection,
                        )

                    print("\nAvailable genres:")
                    print(genres.to_string(index=False))

                    print("\nAvailable locations:")
                    print(locations.to_string(index=False))

                    title = input("Title: ")
                    genre_id = int(input("GenreID: "))
                    location_id = int(input("StandortID: "))
                    isbn = input("ISBN (Enter to skip): ")
                    lendable = int(input("Lendable (0 = no, 1 = yes): "))

                    create_buch(
                        title,
                        genre_id,
                        location_id,
                        isbn,
                        lendable,
                    )

                    print("Book added successfully.")

                elif choice == 3:
                    print(read_buecher().to_string(index=False))

                    book_id = int(input("BuchID to update: "))
                    new_title = input("New title: ")

                    count = update_buecher(book_id, new_title)

                    if count == 0:
                        print("Book not found.")
                    else:
                        print("Book updated successfully.")

                elif choice == 4:
                    print(read_buecher().to_string(index=False))

                    book_id = int(input("BuchID to delete: "))

                    confirmation = (
                        input("Type yes to delete this book: ").strip().lower()
                    )

                    if confirmation == "yes":
                        count = delete_buecher(book_id)

                        if count == 0:
                            print("Book not found.")
                        else:
                            print("Book deleted successfully.")
                    else:
                        print("Deletion cancelled.")

                else:
                    print("Invalid selection.")

            except ValueError as error:
                print(f"Invalid input: {error}")

            except IntegrityError as error:
                error_code = error.orig.args[0]

                if error_code == 1062:
                    print("This ISBN already exists.")

                elif error_code == 1452:
                    print("GenreID or StandortID does not exist.")

                elif error_code == 1451:
                    print("This book has a loan history " "and cannot be deleted.")

                else:
                    raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
"""