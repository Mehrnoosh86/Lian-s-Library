import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import engine


# READ
def read_friends():
    query = text("""
        SELECT FreundID, Vorname, Nachname, Telefon, Email
        FROM Freunde
        ORDER BY FreundID
    """)

    with engine.connect() as connection:
        return pd.read_sql(query, con=connection)


# Check the input for both create and update.
def friend_values(first_name, last_name, phone="", email=""):
    first_name = first_name.strip()
    last_name = last_name.strip()
    phone = phone.strip()
    email = email.strip()

    if not first_name or not last_name:
        raise ValueError("First name and last name are required.")

    if len(first_name) > 100 or len(last_name) > 100:
        raise ValueError("Each name can have at most 100 characters.")

    if len(phone) > 30 or len(email) > 255:
        raise ValueError("Phone or email is too long.")

    return {
        "Vorname": first_name,
        "Nachname": last_name,
        "Telefon": phone or None,
        "Email": email or None,
    }


# CREATE
def create_friend(first_name, last_name, phone="", email=""):
    values = friend_values(first_name, last_name, phone, email)
    new_friend = pd.DataFrame([values])

    with engine.begin() as connection:
        new_friend.to_sql(
            name="Freunde",
            con=connection,
            if_exists="append",
            index=False,
        )


# UPDATE
def update_friend(friend_id, first_name, last_name, phone="", email=""):
    values = friend_values(first_name, last_name, phone, email)
    values["friend_id"] = friend_id

    query = text("""
        UPDATE Freunde
        SET Vorname = :Vorname,
            Nachname = :Nachname,
            Telefon = :Telefon,
            Email = :Email
        WHERE FreundID = :friend_id
    """)

    with engine.begin() as connection:
        result = connection.execute(query, values)

    return result.rowcount


# DELETE
def delete_friend(friend_id):
    query = text("""
        DELETE FROM Freunde
        WHERE FreundID = :friend_id
    """)

    with engine.begin() as connection:
        result = connection.execute(query, {"friend_id": friend_id})

    return result.rowcount


"""def main():
    try:
        while True:
            print("\n--- Friends Menu ---")
            print("1. Show friends")
            print("2. Add friend")
            print("3. Edit friend")
            print("4. Delete friend")
            print("0. Exit")

            try:
                choice = int(input("Choose an operation: "))

                if choice == 0:
                    break

                elif choice == 1:
                    friends = read_friends()
                    if friends.empty:
                        print("No friends found.")
                    else:
                        print(friends.to_string(index=False))

                elif choice in (2, 3):
                    if choice == 3:
                        print(read_friends().to_string(index=False))
                        friend_id = int(input("FreundID to update: "))
                        print("Enter all four fields. Empty phone or email clears it.")

                    first_name = input("First name: ")
                    last_name = input("Last name: ")
                    phone = input("Phone (optional): ")
                    email = input("Email (optional): ")

                    if choice == 2:
                        create_friend(first_name, last_name, phone, email)
                        print("Friend added successfully.")
                    else:
                        count = update_friend(
                            friend_id, first_name, last_name, phone, email
                        )
                        if count == 0:
                            print("Friend not found.")
                        else:
                            print("Friend details saved.")

                elif choice == 4:
                    print(read_friends().to_string(index=False))
                    friend_id = int(input("FreundID to delete: "))
                    confirmation = input("Type yes to delete: ").strip().lower()

                    if confirmation != "yes":
                        print("Deletion cancelled.")
                        continue

                    count = delete_friend(friend_id)
                    if count == 0:
                        print("Friend not found.")
                    else:
                        print("Friend deleted successfully.")

                else:
                    print("Invalid selection.")

            except ValueError as error:
                print(f"Invalid input: {error}")

            except IntegrityError as error:
                if error.orig.args[0] == 1451:
                    print("This friend has a loan history and cannot be deleted.")
                else:
                    raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
"""