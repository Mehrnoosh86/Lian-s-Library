import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import engine


def validate_location_name(name):
    name = name.strip()

    if not name:
        raise ValueError("Location name cannot be empty.")

    if len(name) > 100:
        raise ValueError("Location name cannot exceed 100 characters.")

    return name


# READ
def read_locations():
    query = text("""
        SELECT StandortID, Bezeichnung
        FROM Standorte
        ORDER BY StandortID
    """)

    with engine.connect() as connection:
        return pd.read_sql(query, con=connection)


# CREATE
def create_location(name):
    name = validate_location_name(name)
    new_location = pd.DataFrame({"Bezeichnung": [name]})

    with engine.begin() as connection:
        new_location.to_sql(
            name="Standorte",
            con=connection,
            if_exists="append",
            index=False,
        )


# UPDATE
def update_location(location_id, new_name):
    new_name = validate_location_name(new_name)

    query = text("""
        UPDATE Standorte
        SET Bezeichnung = :new_name
        WHERE StandortID = :location_id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"new_name": new_name, "location_id": location_id},
        )

    return result.rowcount


# DELETE
def delete_location(location_id):
    query = text("""
        DELETE FROM Standorte
        WHERE StandortID = :location_id
    """)

    with engine.begin() as connection:
        result = connection.execute(query, {"location_id": location_id})

    return result.rowcount


"""def main():
    try:
        while True:
            print("\n--- Locations Menu ---")
            print("1. Show locations")
            print("2. Add location")
            print("3. Edit location name")
            print("4. Delete location")
            print("0. Exit")

            try:
                choice = int(input("Choose an operation: "))

                if choice == 0:
                    break

                elif choice == 1:
                    locations = read_locations()
                    if locations.empty:
                        print("No locations found.")
                    else:
                        print(locations.to_string(index=False))

                elif choice == 2:
                    name = input("New location name: ")
                    create_location(name)
                    print("Location added successfully.")

                elif choice == 3:
                    print(read_locations().to_string(index=False))
                    location_id = int(input("StandortID to update: "))
                    new_name = input("New name: ")

                    count = update_location(location_id, new_name)
                    if count == 0:
                        print("Location not found.")
                    else:
                        print("Location name saved.")

                elif choice == 4:
                    print(read_locations().to_string(index=False))
                    location_id = int(input("StandortID to delete: "))
                    confirmation = input("Type yes to delete: ").strip().lower()

                    if confirmation != "yes":
                        print("Deletion cancelled.")
                        continue

                    count = delete_location(location_id)
                    if count == 0:
                        print("Location not found.")
                    else:
                        print("Location deleted successfully.")

                else:
                    print("Invalid selection.")

            except ValueError as error:
                print(f"Invalid input: {error}")

            except IntegrityError as error:
                error_code = error.orig.args[0]

                if error_code == 1062:
                    print("This location name already exists.")
                elif error_code == 1451:
                    print(
                        "Move the books to another location before deleting this one."
                    )
                else:
                    raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
"""