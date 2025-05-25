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

    def articles(self):
        from lib.models.article import Article
        return Article.find_by_magazine(self)