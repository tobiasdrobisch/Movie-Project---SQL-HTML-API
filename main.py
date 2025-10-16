from core.movie_manager import MovieDatabase

def main():
    """
    Entry point of the program.
    Displays a menu and handles user input.
    """
    database = MovieDatabase()
    print("\n********** My Movies Database **********\n")

    while True:
        print(
            "\nMenu:\n"
            "0. Exit\n"
            "1. List movies\n"
            "2. Add movie\n"
            "3. Delete movie\n"
            "4. Update movie\n"
            "5. Show stats\n"
            "6. Random movie\n"
            "7. Search movie\n"
            "8. Movies sorted by rating\n"
            "9. Generate website\n"
        )

        try:
            choice = int(input("Enter choice (0-9): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        print()  # Empty line for better spacing

        if choice == 0:
            print("Bye!")
            break
        elif choice == 1:
            database.list_movies()
        elif choice == 2:
            database.add_movie()
        elif choice == 3:
            database.delete_movie()
        elif choice == 4:
            database.update_movie()
        elif choice == 5:
            database.show_stats()
        elif choice == 6:
            database.random_movie()
        elif choice == 7:
            database.search_movie()
        elif choice == 8:
            database.movies_sorted_by_rating()
        elif choice == 9:
            database.generate_website()
        else:
            print("Invalid choice. Please enter a number between 0 and 9.")


if __name__ == "__main__":
    main()
