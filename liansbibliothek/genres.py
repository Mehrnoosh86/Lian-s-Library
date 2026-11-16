import pandas as pd
from sqlalchemy import text #for preparing SQL command to run
from sqlalchemy.exc import IntegrityError #using to declare Error in Database
from database import engine #getting connection string from database


# READ
def read_genres():
    read_query = text("""
        SELECT GenreID, Name
        FROM Genres
        ORDER BY GenreID
    """)

    with engine.connect() as connection:#open a database connection and put it in 'connection'
        df = pd.read_sql(read_query, con=connection)#run read_sql function and store the result in df as dataframe

    return df


# CREATE
def create_genre(name):
    name = name.strip()#deleting extra spaces in input String

    if not name:#if input String is empty , show the error message
        raise ValueError("Genre name cannot be empty.")

    if len(name) > 50:#if the input String length is more than 50 characters, show error message
        raise ValueError("Genre name cannot exceed 50 characters.")

    new_genre = pd.DataFrame({ #for storing new row, we store new genre as a dataframe
        "Name": [name]
    })

    with engine.begin() as connection:
        new_genre.to_sql(#sending a new dataframe to MySQL 
            name="Genres",#name of target table
            con=connection,#useing the currect connection
            if_exists="append",#if the table exist, then add the dataframe to that
            index=False,
        )


# UPDATE
def update_genre(genre_id, new_name):
    new_name = new_name.strip()

    if not new_name:
        raise ValueError("Genre name cannot be empty.")

    if len(new_name) > 50:
        raise ValueError("Genre name cannot exceed 50 characters.")

    update_query = text("""
        UPDATE Genres
        SET Name = :new_name
        WHERE GenreID = :genre_id
    """)

    with engine.begin() as connection:
        result = connection.execute(#run the query and put the result in 'result'
            update_query,
            {
                "new_name": new_name,
                "genre_id": genre_id,
            },
        )

    return result.rowcount#return the reported final rows


# DELETE
def delete_genre(genre_id):
    delete_query = text("""
        DELETE FROM Genres
        WHERE GenreID = :genre_id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            delete_query,
            {"genre_id": genre_id},
        )

    return result.rowcount


# MENU
"""def main():
    try:
        while True:#making a menu to choose the CRUD functions
            print("\n--- Genres Menu ---")
            print("1. Show genres")
            print("2. Add genre")
            print("3. Edit genre")
            print("4. Delete genre")
            print("0. Exit")

            try:
                choice = int(input("Choose an operation: "))

                if choice == 0:
                    break

                elif choice == 1:
                    genres = read_genres()

                    if genres.empty:
                        print("No genres found.")
                    else:
                        print(genres.to_string(index=False))#converting Genres table to string for showing that

                elif choice == 2:
                    name = input("New genre name: ")

                    create_genre(name)

                    print("Genre added successfully.")

                elif choice == 3:
                    print(read_genres().to_string(index=False))

                    genre_id = int(input("GenreID to update: "))
                    new_name = input("New name: ")

                    count = update_genre(genre_id, new_name)

                    if count == 0:
                        print("Genre not found.")
                    else:
                        print("Genre updated successfully.")

                elif choice == 4:
                    print(read_genres().to_string(index=False))

                    genre_id = int(input("GenreID to delete: "))

                    confirmation = input(
                        "Type yes to delete this genre: "
                    ).strip().lower()

                    if confirmation == "yes":
                        count = delete_genre(genre_id)

                        if count == 0:
                            print("Genre not found.")
                        else:
                            print("Genre deleted successfully.")
                    else:
                        print("Deletion cancelled.")

                else:
                    print("Invalid selection.")

            except ValueError as error:
                print(f"Invalid input: {error}")

            except IntegrityError as error:
                error_code = error.orig.args[0]#extracting the error line number and related information in MySQL 

                if error_code == 1062:#limited running : related to duplicated genre
                    print("This genre name already exists.")

                elif error_code == 1451:#deleting the rows that it relat to other table
                    print(
                        "This genre is used by books. "
                        "Change their genre before deleting it."
                    )

                else:
                    raise

    finally:
        engine.dispose()#releasing the resources


if __name__ == "__main__":#checking the type of running. if we call the file in Terminal , we need to run main()
    main()"""