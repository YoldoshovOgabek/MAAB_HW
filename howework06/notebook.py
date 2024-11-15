from tabulate import tabulate
import time
import json

headers1 = ["ID", "Text", "Created", "Updated"]
table_type = "rounded_grid"

class Note:
    def __init__(self, note_id, text, created, updated=None):
        self.id = note_id
        self.text = text
        self.created = created
        self.updated = updated

    def __str__(self):
        return f"ID: {self.id}\nText: {self.text}\nCreated: {self.created}\nUpdated: {self.updated if self.updated else '---'}"


class NoteManager:
    def __init__(self):
        self.notes, self.next_id = self.load_notes()

    def save_notes(self):
        data = {"notes": [note.__dict__ for note in self.notes], "next_id": self.next_id}
        with open("notes.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_notes(self):
        try:
            with open("notes.json", "r") as file:
                data = json.load(file)
                notes = [Note(**note) for note in data.get("notes", [])]
                next_id = data.get("next_id", 1)
                return notes, next_id
        except FileNotFoundError:
            return [], 1 

    def find_note_by_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def show_all_notes(self):
        if self.notes:
            table = [
                [note.id, self.shorten_text(note.text), note.created, note.updated if note.updated else "---"]
                for note in self.notes
            ]
            print(tabulate(table, headers=headers1, tablefmt=table_type))
        else:
            print("No notes found")

    def show_note_details(self):
        note_id = int(input("Enter note ID: "))
        note = self.find_note_by_id(note_id)
        if note:
            print(note)
        else:
            print("Note not found")

    def create_note(self):
        text = input("Enter note's text: ")
        created = time.strftime("%Y-%m-%d %H:%M:%S")
        new_note = Note(self.next_id, text, created)
        self.notes.append(new_note)
        print("Note added")
        self.next_id += 1
        self.save_notes()

    def update_note(self):
        note_id = int(input("Enter note ID to update: "))
        note = self.find_note_by_id(note_id)
        if note:
            new_text = input("Enter new text: ")
            note.text = new_text
            note.updated = time.strftime("%Y-%m-%d %H:%M:%S")
            print("Note updated")
            self.save_notes()
        else:
            print("Note not found")

    def delete_note(self):
        note_id = int(input("Enter note ID to delete: "))
        note = self.find_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            print("Note deleted.")
            self.save_notes()
        else:
            print("Note not found.")

    @staticmethod
    def shorten_text(text, length=10):
        if len(text) > length:
            return text[:length-3] + "..." + text[len(text)-5:]
        else:
            return text

    @staticmethod
    def show_menu():
        print("----------------")
        print("| CHOOSE OPTION")
        print("| 1: SHOW ALL NOTES")
        print("| 2: SHOW NOTE DETAILS")
        print("| 3: CREATE NOTE")
        print("| 4: UPDATE NOTE")
        print("| 5: DELETE NOTE")
        print("| Q: QUIT THE APPLICATION")
        print("| M: SHOW MENU AGAIN")
        print("----------------")


def main():
    note_manager = NoteManager()
    note_manager.show_menu()
    
    while True:
        choice = input("Choice: ").strip().upper()
        if choice == "1":
            note_manager.show_all_notes()
        elif choice == "2":
            note_manager.show_note_details()
        elif choice == "3":
            note_manager.create_note()
        elif choice == "4":
            note_manager.update_note()
        elif choice == "5":
            note_manager.delete_note()
        elif choice == "Q":
            print("QUIT!")
            break
        elif choice == "M":
            note_manager.show_menu()
        else:
            print("Invalid, try again")


if __name__ == "__main__":
    main()
