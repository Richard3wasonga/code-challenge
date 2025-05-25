from lib.db.connection import CONN, CURSOR

class Author:
    all = {}
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and len(new_name.strip()):
            self._name = new_name.strip()
        else:
            raise ValueError("Name must be a non-empty string")

    def save(self):
        sql = """
            INSERT INTO authors (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name):
        author = cls(name)
        author.save()
        return author

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM authors
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(row[1], row[0]) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM authors
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls(row[1], row[0]) if row else None

    def articles(self):
        from lib.models.article import Article
        sql = """
            SELECT * FROM articles
            WHERE author_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Article(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine
        sql = """
            SELECT DISTICT magazines.*
            FROM magazines
            INNER JOIN articles
            ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Magazine(row[1], row[2], row[0]) for row in rows]

    @classmethod
    def most_active_author(cls):
        sql = """
            SELECT author.id, authors.name, COUNT(articles.id) AS article_count
            FROM authors
            INNER JOIN articles
            ON authors.id = articles.author_id
            GROUP BY authors.id, authors.name
            ORDER BY article_count DESC
            LIMIT 1;
        """
        row = CURSOR.execute(sql).fetchone()
        return cls(row[1], row[0]) if row else None
        
