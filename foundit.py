import mysql.connector
from mysql.connector import Error


# Connect Python to MySQL
def connect_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="...",
            database="foundit_db"
        )

        if connection.is_connected():
            print("Connected to FoundIt database!")
            return connection

    except Error as e:
        print("Database connection error:", e)

    return None


# Get and validate a record ID
def get_item_id():
    while True:
        try:
            item_id = int(input("Enter item ID: "))
            if item_id > 0:
                return item_id
            print("ID must be greater than zero.")
        except ValueError:
            print("Please enter a valid number.")


# CREATE: Add a new item
def add_item(cursor, connection):
    item_name = input("Item name: ").strip()
    if not item_name:
        print("Item name cannot be empty.")
        return

    description = input("Description: ").strip()
    item_type = input("Type (Lost/Found): ").strip().title()

    if item_type not in ("Lost", "Found"):
        print("Type must be Lost or Found.")
        return

    location = input("Location: ").strip()
    if not location:
        print("Location cannot be empty.")
        return

    sql = """
        INSERT INTO items
        (item_name, description, item_type, location)
        VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (item_name, description, item_type, location))
        connection.commit()
        print("Item added successfully!")

    except Error as e:
        connection.rollback()
        print("Error adding item:", e)


# READ: Display all items
def view_items(cursor):
    try:
        cursor.execute("SELECT * FROM items ORDER BY item_id")
        records = cursor.fetchall()

        if not records:
            print("No items found.")
            return

        print("\n--- FOUND IT RECORDS ---")

        for item in records:
            print("-" * 35)
            print("ID:", item["item_id"])
            print("Name:", item["item_name"])
            print("Description:", item["description"])
            print("Type:", item["item_type"])
            print("Location:", item["location"])
            print("Date:", item["date_reported"])
            print("Status:", item["status"])

        print("-" * 35)

    except Error as e:
        print("Error viewing items:", e)


# UPDATE: Modify an existing item
def update_item(cursor, connection):
    item_id = get_item_id()

    cursor.execute("SELECT item_id FROM items WHERE item_id = %s", (item_id,))

    if cursor.fetchone() is None:
        print("Item ID not found.")
        return

    print("Leave a field blank to keep its current value.")
    item_name = input("New item name: ").strip()
    location = input("New location: ").strip()
    status = input("New status (Pending/Claimed/Returned): ").strip().title()

    if not item_name and not location and not status:
        print("No changes entered.")
        return

    if status and status not in ("Pending", "Claimed", "Returned"):
        print("Invalid status.")
        return

    try:
        if item_name:
            cursor.execute(
                "UPDATE items SET item_name = %s WHERE item_id = %s",
                (item_name, item_id)
            )

        if location:
            cursor.execute(
                "UPDATE items SET location = %s WHERE item_id = %s",
                (location, item_id)
            )

        if status:
            cursor.execute(
                "UPDATE items SET status = %s WHERE item_id = %s",
                (status, item_id)
            )

        connection.commit()
        print("Item updated successfully!")

    except Error as e:
        connection.rollback()
        print("Error updating item:", e)


# DELETE: Remove an item after confirmation
def delete_item(cursor, connection):
    item_id = get_item_id()

    cursor.execute("SELECT item_name FROM items WHERE item_id = %s", (item_id,))
    item = cursor.fetchone()

    if item is None:
        print("Item ID not found.")
        return

    print("Item:", item["item_name"])
    confirm = input("Delete this item? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Deletion cancelled.")
        return

    try:
        cursor.execute("DELETE FROM items WHERE item_id = %s", (item_id,))
        connection.commit()
        print("Item deleted successfully!")

    except Error as e:
        connection.rollback()
        print("Error deleting item:", e)


# MAIN PROGRAM
def main():
    connection = connect_database()

    if connection is None:
        print("Please check your MySQL settings.")
        return

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        while True:
            print("\n===== FOUNDIT SYSTEM =====")
            print("1. Add Item")
            print("2. View Items")
            print("3. Update Item")
            print("4. Delete Item")
            print("5. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                add_item(cursor, connection)
            elif choice == "2":
                view_items(cursor)
            elif choice == "3":
                update_item(cursor, connection)
            elif choice == "4":
                delete_item(cursor, connection)
            elif choice == "5":
                print("Thank you for using FoundIt!")
                break
            else:
                print("Invalid choice. Enter 1 to 5.")

    except Error as e:
        print("Program error:", e)

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
