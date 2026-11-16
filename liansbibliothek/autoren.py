import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from database import engine


def author_values(first_name, last_name):
    first_name = first_name.strip()
    last_name = last_name.strip()

    if not first_name or not last_name:
        raise ValueError("First name and last name are required.")

    if len(first_name) > 100 or len(last_name) > 100:
        raise ValueError("Each name can have at most 100 characters.")

    return {"Vorname": first_name, "Nachname": last_name}


# READ
def read_authors():
    query = text("""
        SELECT AutorID, Vorname, Nachname
        FROM Autoren
        ORDER BY Nachname, Vorname, AutorID
    """)

    with engine.connect() as connection:
        return pd.read_sql(query, con=connection)


# CREATE
def create_author(first_name, last_name):
    values = author_values(first_name, last_name)
    new_author = pd.DataFrame([values])

    with engine.begin() as connection:
        new_author.to_sql(
            name="Autoren",
            con=connection,
            if_exists="append",
            index=False,
        )


# UPDATE
def update_author(author_id, first_name, last_name):
    values = author_values(first_name, last_name)
    values["author_id"] = author_id

    query = text("""
        UPDATE Autoren
        SET Vorname = :Vorname,
            Nachname = :Nachname
        WHERE AutorID = :author_id
    """)

    with engine.begin() as connection:
        result = connection.execute(query, values)
        return result.rowcount


# DELETE
def delete_author(author_id):
    query = text("""
        DELETE FROM Autoren
        WHERE AutorID = :author_id
    """)

    with engine.begin() as connection:
        result = connection.execute(query, {"author_id": author_id})
        return result.rowcount


"""def main():
    try:
        while True:
            print("\n--- Authors Menu ---")
            print("1. Show authors")
            print("2. Add author")
            print("3. Edit author")
            print("4. Delete author")
            print("0. Exit")

            choice = input("Choose an operation: ").strip()

            try:
                if choice == "0":
                    break

                elif choice == "1":
                    authors = read_authors()
                    if authors.empty:
                        print("No authors found.")
                    else:
                        print(authors.to_string(index=False))

                elif choice == "2":
                    first_name = input("First name: ")
                    last_name = input("Last name: ")
                    create_author(first_name, last_name)
                    print("Author added.")

                elif choice == "3":
                    print(read_authors().to_string(index=False))
                    author_id = int(input("AutorID to update: "))
                    first_name = input("First name: ")
                    last_name = input("Last name: ")

                    if update_author(author_id, first_name, last_name):
                        print("Author details saved.")
                    else:
                        print("Author not found.")

                elif choice == "4":
                    print(read_authors().to_string(index=False))
                    author_id = int(input("AutorID to delete: "))
                    confirmation = (
                        input(
                            "This also removes the author's links to books. "
                            "Type yes to delete: "
                        )
                        .strip()
                        .lower()
                    )

                    if confirmation == "yes":
                        if delete_author(author_id):
                            print("Author deleted.")
                        else:
                            print("Author not found.")
                    else:
                        print("Deletion cancelled.")

                else:
                    print("Invalid selection.")

            except ValueError as error:
                print(f"Invalid input: {error}")

            except IntegrityError as error:
                if error.orig.args[0] == 1062:
                    print("An author with this first and last name already exists.")
                else:
                    raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
"""