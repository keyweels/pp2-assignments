import csv
import psycopg2
from config import get_config


def get_connection():
    config = get_config()
    return psycopg2.connect(**config)


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)

    conn.commit()
    print("Table created successfully")

    cur.close()
    conn.close()


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    print("Inserted successfully")

    cur.close()
    conn.close()


def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row["name"], row["phone"])
            )

    conn.commit()
    print("CSV data inserted")

    cur.close()
    conn.close()


def update_contact():
    choice = input("Update name or phone? (name/phone): ").strip().lower()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "phone":
        old_name = input("Enter the name of contact to update: ")
        new_phone = input("Enter new phone: ")
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE name = %s",
            (new_phone, old_name)
        )
        conn.commit()
        print("Phone updated successfully")

    elif choice == "name":
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")
        cur.execute(
            "UPDATE phonebook SET name = %s WHERE name = %s",
            (new_name, old_name)
        )
        conn.commit()
        print("Name updated successfully")

    else:
        print("Invalid choice")

    cur.close()
    conn.close()


def query_by_name():
    name = input("Enter name to search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE name = %s",
        (name,)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found")

    cur.close()
    conn.close()


def query_by_phone_prefix():
    prefix = input("Enter phone prefix: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + "%",)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found")

    cur.close()
    conn.close()


def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("PhoneBook is empty")

    cur.close()
    conn.close()


def delete_contact():
    choice = input("Delete by name or phone? (name/phone): ").strip().lower()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "name":
        name = input("Enter name to delete: ")
        cur.execute(
            "DELETE FROM phonebook WHERE name = %s",
            (name,)
        )
        conn.commit()
        print("Contact deleted successfully")

    elif choice == "phone":
        phone = input("Enter phone to delete: ")
        cur.execute(
            "DELETE FROM phonebook WHERE phone = %s",
            (phone,)
        )
        conn.commit()
        print("Contact deleted successfully")

    else:
        print("Invalid choice")

    cur.close()
    conn.close()


def menu():
    while True:
        print("\nPhoneBook Menu")
        print("1. Create table")
        print("2. Insert from console")
        print("3. Insert from CSV")
        print("4. Update contact")
        print("5. Query by name")
        print("6. Query by phone prefix")
        print("7. Delete contact")
        print("8. Show all contacts")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_by_name()
        elif choice == "6":
            query_by_phone_prefix()
        elif choice == "7":
            delete_contact()
        elif choice == "8":
            show_all_contacts()
        elif choice == "0":
            print("Goodbye")
            break
        else:
            print("Invalid choice")


menu()