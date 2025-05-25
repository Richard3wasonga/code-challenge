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
    def content(self, value):
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

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM articles
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(row[1], row[2], row[3], row[4], row[0]) if row else None

    @classmethod
    def find_by_title(cls, title):
        sql = """
            SELECT *
            FROM articles
            WHERE title = ?
        """
        rows = CURSOR.execute(sql, (title,)).fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    @classmethod
    def find_by_author(cls, author_id):
        sql = """
            SELECT *
            FROM articles
            WHERE author_id = ?
        """
        rows = CURSOR.execute(sql, (author_id,)).fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        sql = """
            SELECT *
            FROM articles
            WHERE magazine_id = ?
        """
        rows = CURSOR.execute(sql, (magazine_id,)).fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    def get_author(self):
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def get_margazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)

    