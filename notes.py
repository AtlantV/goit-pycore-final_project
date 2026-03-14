"""
Notes — моделі даних для нотаток
================================
Містить класи для роботи з нотатками та керування ними.
"""

from collections import UserDict
from datetime import datetime


class Tag:
    """Клас для зберігання тегу."""
    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tag must be a non-empty string")
        self.value = value.strip().lower()

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.value == other.value
        return self.value == str(other).lower()


class Note:
    """Клас для зберігання нотатки."""
    def __init__(self, title, text, note_id=None):
        self.id = note_id or self._generate_id()
        self.title = title
        self.text = text
        self.tags = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @staticmethod
    def _generate_id():
        """Генерує унікальний ID на основі часу."""
        return int(datetime.now().timestamp() * 1000000)

    def add_tag(self, tag_value):
        """Додає тег до нотатки."""
        tag = Tag(tag_value)
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag_value):
        """Видаляє тег з нотатки."""
        tag = Tag(tag_value)
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

    def edit(self, title=None, text=None):
        """Редагує нотатку."""
        if title:
            self.title = title
        if text:
            self.text = text
        self.updated_at = datetime.now()

    def has_tag(self, tag_value):
        """Перевіряє наявність тегу в нотатці."""
        tag = Tag(tag_value)
        return tag in self.tags

    def __str__(self):
        tags_str = f" [T: {', '.join(str(tag) for tag in self.tags)}]" if self.tags else ""
        return f"[{self.id}] {self.title}{tags_str}\n{self.text}\nСтворено: {self.created_at.strftime('%d.%m.%Y %H:%M')}"


class NotesBook(UserDict):
    """Клас для зберігання нотаток та керування ними."""

    def add_note(self, note):
        """Додає нотатку до книги."""
        self.data[note.id] = note
        return note

    def find(self, note_id):
        """Знаходить нотатку за ID."""
        return self.data.get(note_id)

    def delete(self, note_id):
        """Видаляє нотатку за ID."""
        if note_id in self.data:
            del self.data[note_id]
            return True
        return False

    def search_by_text(self, query):
        """Пошук нотаток за текстом (в назві або змісті)."""
        query_lower = query.lower()
        results = []
        for note in self.data.values():
            if (query_lower in note.title.lower() or 
                query_lower in note.text.lower()):
                results.append(note)
        return results

    def search_by_tag(self, tag_value):
        """Пошук нотаток за тегом."""
        results = []
        for note in self.data.values():
            if note.has_tag(tag_value):
                results.append(note)
        return results

    def get_all_tags(self):
        """Повертає список всіх унікальних тегів."""
        tags = set()
        for note in self.data.values():
            for tag in note.tags:
                tags.add(str(tag))
        return sorted(list(tags))

    def get_notes_sorted_by_date(self, reverse=False):
        """Повертає нотатки відсортовані за датою."""
        return sorted(
            self.data.values(),
            key=lambda note: note.created_at,
            reverse=reverse
        )

    def __str__(self):
        if not self.data:
            return "Нотаток не знайдено."
        return "\n" + "\n".join("-" * 50 + "\n" + str(note) for note in self.data.values())
