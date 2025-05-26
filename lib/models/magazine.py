from lib.db.connection import CONN, CURSOR

class Magazine:
    all = {}

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine id={self.id} name='{self.name}' category='{self.category}'>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and len(new_name.strip()):
            self._name = new_name.strip()
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and len(new_category.strip()):
            self._category = new_category.strip()

    def save(self):
        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM magazines
            WHERE name = ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls(row[1], row[2], row[0]) if row else None

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM magazines
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(row[1], row[2], row[0]) if row else None

    @classmethod
    def find_by_category(cls, category):
        sql = """
            SELECT *
            FROM magazines
            WHERE category = ?
        """
        rows = CURSOR.execute(sql, (category,)).fetchall()
        return [cls(row[1], row[2], row[0]) for row in rows]
    def authors(self):
        from lib.models.author import Author
        sql = """
            SELECT DISTINCT authors.*
            FROM authors
            INNER JOIN articles
            ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Author(row[1], row[0]) for row in rows]

    def article_counts(self):
        sql = """
            SELECT magazines.id, magazines.name, COUNT(articles.id) AS article_count
            FROM magazines
            LEFT JOIN articles
            ON magazines.id = articles.magazine_id
            GROUP BY magazines.id, magazines.name;
        """
        rows = CURSOR.execute(sql).fetchall()
        return rows
    @classmethod
    def magazine_with_many_authors(cls):
        sql = """
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            INNER JOIN articles
            ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
            HAVING COUNT(DISTINCT articles.author_id) >= 2;
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls(row[1], row[2], row[0]) for row in rows]

    def articles(self):
        from lib.models.article import Article
        sql = """
            SELECT * FROM articles
            WHERE magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Article(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    def contributors(self):
        from lib.models.author import Author
        sql = """
            SELECT DISTINCT authors.*
            FROM authors
            INNER JOIN articles
            ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Author(row[1], row[0]) for row in rows]

    def article_titles(self):
        sql = """
            SELECT title
            FROM articles
            WHERE magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [row[0] for row in rows]

    def contributing_authors(self):
        from lib.models.author import Author
        sql = """
            SELECT authors.*, COUNT(articles.id) AS article_count
            FROM authors
            INNER JOIN articles
            ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Author(row[1], row[0]) for row in rows]

   