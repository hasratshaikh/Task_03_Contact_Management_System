import json
import re
from pathlib import Path

DATA_FILE = Path(__file__).parent / "contacts.json"


def load_contacts():
    if not DATA_FILE.exists():
        save_contacts([])
        return []

    try:
        content = DATA_FILE.read_text(encoding="utf-8").strip()

        if not content:
            save_contacts([])
            return []

        contacts = json.loads(content)

        if not isinstance(contacts, list):
            print("Invalid contacts file format.")
            return None

        return contacts

    except (json.JSONDecodeError, OSError) as error:
        print(f"Error loading contacts: {error}")
        return None


def save_contacts(contacts):
    try:
        DATA_FILE.write_text(
            json.dumps(contacts, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        return True

    except OSError as error:
        print(f"Error saving contacts: {error}")
        return False


def validate_email(email):
    if not email:
        return True

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def find_contact(contacts, phone):
    for contact in contacts:
        if contact.get("phone") == phone:
            return contact

    return None


def add_contact():
    contacts = load_contacts()

    if contacts is None:
        return

    print("\n--- Add Contact ---")

    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email (optional): ").strip()

    if not name or not phone:
        print("Name and phone number are required.")
        return

    if find_contact(contacts, phone):
        print("This phone number already exists.")
        return

    if not validate_email(email):
        print("Invalid email address.")
        return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email
    })

    if save_contacts(contacts):
        print("Contact added successfully!")


def view_contacts():
    contacts = load_contacts()

    if contacts is None:
        return

    print("\n--- All Contacts ---")

    if not contacts:
        print("No contacts found.")
        return

    for index, contact in enumerate(contacts, start=1):
        print(f"\nContact {index}")
        print(f"Name  : {contact.get('name', '')}")
        print(f"Phone : {contact.get('phone', '')}")
        print(f"Email : {contact.get('email', '') or 'Not provided'}")


def search_contact():
    contacts = load_contacts()

    if contacts is None:
        return

    query = input("Enter name or phone to search: ").strip().lower()

    if not query:
        print("Search cannot be empty.")
        return

    results = [
        contact for contact in contacts
        if query in contact.get("name", "").lower()
        or query in contact.get("phone", "").lower()
    ]

    if not results:
        print("No matching contacts found.")
        return

    for contact in results:
        print(f"\nName  : {contact.get('name', '')}")
        print(f"Phone : {contact.get('phone', '')}")
        print(f"Email : {contact.get('email', '') or 'Not provided'}")


def update_contact():
    contacts = load_contacts()

    if contacts is None:
        return

    phone = input("Enter current phone number: ").strip()
    contact = find_contact(contacts, phone)

    if contact is None:
        print("Contact not found.")
        return

    print("Leave fields empty to keep current values.")

    name = input(f"New name [{contact['name']}]: ").strip()
    new_phone = input(f"New phone [{contact['phone']}]: ").strip()
    email = input(f"New email [{contact.get('email', '')}]: ").strip()

    final_phone = new_phone or contact["phone"]
    duplicate = find_contact(contacts, final_phone)

    if duplicate is not None and duplicate is not contact:
        print("This phone number already exists.")
        return

    if email and not validate_email(email):
        print("Invalid email address.")
        return

    if name:
        contact["name"] = name

    if new_phone:
        contact["phone"] = new_phone

    if email:
        contact["email"] = email

    if save_contacts(contacts):
        print("Contact updated successfully!")


def delete_contact():
    contacts = load_contacts()

    if contacts is None:
        return

    phone = input("Enter phone number to delete: ").strip()
    contact = find_contact(contacts, phone)

    if contact is None:
        print("Contact not found.")
        return

    confirm = input(
        f"Delete {contact['name']}? (yes/no): "
    ).strip().lower()

    if confirm not in ("yes", "y"):
        print("Deletion cancelled.")
        return

    contacts.remove(contact)

    if save_contacts(contacts):
        print("Contact deleted successfully!")


def main():
    while True:
        print("\n" + "=" * 40)
        print("      CONTACT MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Thank you for using Contact Management System!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
