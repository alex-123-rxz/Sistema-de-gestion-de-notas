import sqlite3
import os
from datetime import datetime

class NoteManager:
    def __init__(self):
        self.conn = sqlite3.connect('notes.db')
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_note(self, title, content):
        self.cursor.execute(
            'INSERT INTO notes (title, content) VALUES (?, ?)',
            (title, content)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_notes(self):
        self.cursor.execute('SELECT * FROM notes ORDER BY updated_at DESC')
        return self.cursor.fetchall()

    def get_note(self, note_id):
        self.cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
        return self.cursor.fetchone()

    def update_note(self, note_id, title, content):
        self.cursor.execute(
            'UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (title, content, note_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_note(self, note_id):
        self.cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.conn.close()

def main():
    note_manager = NoteManager()
    
    while True:
        print("\n=== Note Management System ===")
        print("1. Create new note")
        print("2. List all notes")
        print("3. View note")
        print("4. Update note")
        print("5. Delete note")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            title = input("Enter note title: ")
            content = input("Enter note content: ")
            note_id = note_manager.create_note(title, content)
            print(f"Note created successfully with ID: {note_id}")

        elif choice == '2':
            notes = note_manager.get_all_notes()
            if not notes:
                print("No notes found.")
            else:
                print("\nAll Notes:")
                for note in notes:
                    print(f"ID: {note[0]}, Title: {note[1]}, Created: {note[3]}")

        elif choice == '3':
            note_id = input("Enter note ID: ")
            note = note_manager.get_note(int(note_id))
            if note:
                print(f"\nTitle: {note[1]}")
                print(f"Content: {note[2]}")
                print(f"Created: {note[3]}")
                print(f"Updated: {note[4]}")
            else:
                print("Note not found.")

        elif choice == '4':
            note_id = input("Enter note ID: ")
            note = note_manager.get_note(int(note_id))
            if note:
                title = input("Enter new title (press Enter to keep current): ")
                content = input("Enter new content (press Enter to keep current): ")
                title = title or note[1]
                content = content or note[2]
                if note_manager.update_note(int(note_id), title, content):
                    print("Note updated successfully.")
                else:
                    print("Failed to update note.")
            else:
                print("Note not found.")

        elif choice == '5':
            note_id = input("Enter note ID: ")
            if note_manager.delete_note(int(note_id)):
                print("Note deleted successfully.")
            else:
                print("Note not found.")

        elif choice == '6':
            note_manager.close()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()