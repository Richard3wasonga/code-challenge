from lib.db.connection import CONN, CURSOR

class Article:

    all = {}

    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr(self):
        return f"<Article id={self.id} title='{self.title}'>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if isinstance(new_title, str) and len(new_title.strip()):
            self._title = new_title.strip()
        else:
            raise ValueError("Title must be a non-empty string")

    @property
    def content(self):
        return self._content

    @content.setter
    def context(self, value):
        if len(value.strip()):
            self._content = value.strip()
        else:
            raise ValueError("Content must contain more than one characters")

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, author_id):
        if type(author_id) is int:
            self._author_id = author_id
        else:
            raise ValueError("author_id must be an integer")
    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, magazine_id):
        if type(magazine_id) is int:
            self._magazine_id = magazine_id
        else:
            raise ValueError("magazine_id must be an integer")

    def save(self):
        sql = """
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    