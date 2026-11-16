from datetime import date

import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from database import engine


# READ
def read_loans(*, active_only=False):
    query = text("""
        SELECT l.LeihID, l.BuchID, b.Titel,
               l.FreundID, f.Vorname, f.Nachname,
               l.Verleihdatum, l.Faelligkeitsdatum, l.Rueckgabedatum
        FROM Leihgaben AS l
        JOIN Buecher AS b ON b.BuchID = l.BuchID
        JOIN Freunde AS f ON f.FreundID = l.FreundID
        WHERE :active_only = 0 OR l.Rueckgabedatum IS NULL
        ORDER BY l.LeihID DESC
    """)

    with engine.connect() as connection:
        return pd.read_sql(
            query, con=connection, params={"active_only": int(active_only)}
        )

# Read function for overview page
def read_loan_overview(today=None, *, active_only=False):
    """Return the loan history with names, normalized dates and display status."""
    today = date.today() if today is None else today
    loans = read_loans(active_only=active_only).rename(
        columns={
            "LeihID": "Loan ID",
            "Titel": "Title",
            "Verleihdatum": "Loan date",
            "Faelligkeitsdatum": "Due date",
            "Rueckgabedatum": "Return date",
        }
    )
    loans["Borrower"] = loans["Vorname"] + " " + loans["Nachname"]
    for column in ("Loan date", "Due date", "Return date"):
        loans[column] = pd.to_datetime(loans[column], errors="coerce")
    active = loans["Return date"].isna()
    loans["Status"] = active.map({True: "On loan", False: "Returned"})
    loans.loc[active & loans["Due date"].lt(pd.Timestamp(today)), "Status"] = "Overdue"
    return loans


# CREATE
def create_loan(book_id, friend_id, loan_date, due_date):
    if due_date < loan_date:
        raise ValueError("Due date cannot be before the loan date.")

    with engine.begin() as connection:
        # Lock this book until the availability check and insert finish.
        book = connection.execute(
            text("""
                SELECT Verleihbar
                FROM Buecher
                WHERE BuchID = :book_id
                FOR UPDATE
            """),
            {"book_id": book_id},
        ).first()

        if book is None:
            raise ValueError("Book not found.")

        if book.Verleihbar != 1:
            raise ValueError("This book is not available for lending.")

        active_loan = connection.execute(
            text("""
                SELECT LeihID
                FROM Leihgaben
                WHERE BuchID = :book_id
                  AND Rueckgabedatum IS NULL
                LIMIT 1
            """),
            {"book_id": book_id},
        ).first()

        if active_loan is not None:
            raise ValueError("This book is already on loan.")

        result = connection.execute(
            text("""
                INSERT INTO Leihgaben
                    (BuchID, FreundID, Verleihdatum, Faelligkeitsdatum)
                VALUES
                    (:book_id, :friend_id, :loan_date, :due_date)
            """),
            {
                "book_id": book_id,
                "friend_id": friend_id,
                "loan_date": loan_date,
                "due_date": due_date,
            },
        )

        return result.lastrowid


# UPDATE: change the due date of an active loan
def update_due_date(loan_id, due_date):
    query = text("""
        UPDATE Leihgaben
        SET Faelligkeitsdatum = :due_date
        WHERE LeihID = :loan_id
          AND Rueckgabedatum IS NULL
          AND Verleihdatum <= :due_date
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"loan_id": loan_id, "due_date": due_date},
        )
        return result.rowcount


# UPDATE: record a return
def return_book(loan_id, return_date):
    query = text("""
        UPDATE Leihgaben
        SET Rueckgabedatum = :return_date
        WHERE LeihID = :loan_id
          AND Rueckgabedatum IS NULL
          AND Verleihdatum <= :return_date
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"loan_id": loan_id, "return_date": return_date},
        )
        return result.rowcount


# DELETE: remove an incorrectly entered loan
def delete_loan(loan_id):
    query = text("""
        DELETE FROM Leihgaben
        WHERE LeihID = :loan_id
    """)

    with engine.begin() as connection:
        result = connection.execute(query, {"loan_id": loan_id})
        return result.rowcount

"""
def main():
    try:
        while True:
            print("\n--- Loans Menu ---")
            print("1. Show loans")
            print("2. Add loan")
            print("3. Change due date")
            print("4. Record return")
            print("5. Delete incorrect loan")
            print("0. Exit")

            choice = input("Choose an operation: ").strip()

            try:
                if choice == "0":
                    break

                elif choice == "1":
                    loans = read_loans()
                    if loans.empty:
                        print("No loans found.")
                    else:
                        print(loans.to_string(index=False, na_rep="-"))

                elif choice == "2":
                    book_id = int(input("BuchID: "))
                    friend_id = int(input("FreundID: "))
                    loan_date = date.fromisoformat(
                        input("Loan date (YYYY-MM-DD): ").strip()
                    )
                    due_date = date.fromisoformat(
                        input("Due date (YYYY-MM-DD): ").strip()
                    )

                    loan_id = create_loan(book_id, friend_id, loan_date, due_date)
                    print(f"Loan added. LeihID: {loan_id}")

                elif choice == "3":
                    loan_id = int(input("LeihID: "))
                    due_date = date.fromisoformat(
                        input("New due date (YYYY-MM-DD): ").strip()
                    )

                    if update_due_date(loan_id, due_date):
                        print("Due date saved.")
                    else:
                        print("Check that the loan is active and the date is valid.")

                elif choice == "4":
                    loan_id = int(input("LeihID: "))
                    entered_date = input(
                        "Return date (YYYY-MM-DD, Enter for today): "
                    ).strip()
                    return_date = (
                        date.fromisoformat(entered_date)
                        if entered_date
                        else date.today()
                    )

                    if return_book(loan_id, return_date):
                        print("Return recorded.")
                    else:
                        print("Check that the loan is active and the date is valid.")

                elif choice == "5":
                    loan_id = int(input("LeihID to delete: "))
                    confirmation = input("Type yes to delete: ").strip().lower()

                    if confirmation != "yes":
                        print("Deletion cancelled.")
                        continue

                    if delete_loan(loan_id):
                        print("Loan deleted.")
                    else:
                        print("Loan not found.")

                else:
                    print("Invalid selection.")

            except ValueError as error:
                print(f"Invalid input: {error}")

            except IntegrityError as error:
                if error.orig.args[0] == 1452:
                    print("Check that BuchID and FreundID exist.")
                else:
                    raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
"""