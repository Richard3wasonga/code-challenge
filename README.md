# code-challenge

# **Magazine-Publishing-System

This is python application that models a publishing system with three main components:`AUthors`, `Magazines` and `Articles`.It demonstrates Object-Oriented programming (OOP) consepts such as encapsulation, relationships and data presistence via SQLITE.

## **Instalatin**

GITHUB REPOSITORY: [ magazine-publishing-system](https://github.com/Richard3wasonga/code-challenge)

1. Clone this repository:
   ```bash
   git clone https://github.com/Richard3wasonga/code-challenge 
   ```

2. Navigate to the project directory:
  ```bash
  cd code-challenge
  ```

3. Install dependencies and create virtual environment:
   ```bash
   pipenv install
   ```

4. Enter virtual environment:
   ```bash
   pipenv shell
   ```

---

## **File Overview**

This system is based on three main classes:

### **Author.py**

Represents a magazine article with name and methods to manage articles.

### **Author Methods**

- `articles()`: Returns all articles written by the author.

- `magazines()`: Returns magazines the author has contributed to.

- `add_article(magazine, title, content)`: Create and save a new article for the author.

- `topic_areas()`: Lists unique categories the author writes in.

- `Author.most_active_author()`: Return the author with the most articles published.

```python

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

    def add_article(self, magazine, title, content="Default content"):
        from lib.models.article import Article
        article = Article(title, content, self.id, magazine.id)
        article.save()
        return article

    def topic_areas(self):
        sql = """
            SELECT DISTINCT magazines.category
            FROM magazines
            INNER JOIN articles
            ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [row[0] for row in rows]
        
```

---

### **Magazine.py**

Represent a publication with a name and category.

### **Magazine Methods**

- `articles()`: Return all articles published in the magazine.

- `contributors()`: Returns a list of unique authors who contributed to the magazine.

- `article_titles()`: Returns titles of all articles published in the magazine.

- `contributing_authors()`: Authors with more than 2 articles in the magazine.

- `Magazine.top_publisher()`: Returns the magazine with the most published articles.

```python

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

    @classmethod
    def top_publisher(cls):
        sql = """
            SELECT magazines.id, magazines.name, magazines.category, COUNT(articles.id) AS article_count
            FROM magazines
            LEFT JOIN articles
            ON magazines.id = articles.magazine_id
            GROUP BY magazines.id, magazines.name, magazines.category
            ORDER BY article_count DESC
            LIMIT 1
        """
        row = CURSOR.execute(sql).fetchone()
        return cls(row[1], row[2], row[0]) if row else None

```
---

### **Article.py**

Represents a piece of writing linked to an author to a magazine with title and content.

### **Article Methods**

- `get_author()`: Return the author of the article.

- `get_magazine()`: Returns the magazine the article is published in.

- `Article.find_by_id(id)`: Finds an article by its ID.

- `Article.find_by_title(title)`: Return articles with the given title.

- `Article.find_by_author(author_id)`: Returns articles by a given author.

- `Article.find_by_magazine(magazine_id)`: Return articles in specific magazine.

```python

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

```
---


## **How to use the system**

1. Create customers and coffees:
   ```python
   alice = Author.create("Alice")
   vogue = Magazine.create("Vogue", "Fashion")
   ```
2. Add articles:
   ```python
   article1 = alice.add_article(vogue, "Style Tips", "Content about style")
   ```
3. Retrieve data:

   ```python
  alice.articles()           # Articles by Alice
  alice.magazines()          # Magazines Alice has contributed to
  vogue.article_titles()     # Titles published in Vogue
  Magazine.top_publisher()   # Most published magazine
   ```
---

## **Important Notes**

- **Data validation**: Ensures string lengths and types are respected.

- **Encapsulation**: Internal state is managed via property setters and getters.

- **SQL Integration**: Uses SQLITE for storing and querying persistent data.

- **Circlar Imports**: Avoided by placing imports inside methods where necessary.

---

## **Features Overview**

- Tracks all instances with all class variable and SQL mapping.

- Prevents invalid entries using custom validators.

- Author,Article and Magazine relatinship with real SQL storage.

- Find top contributors and publishers by quering the database

---

## **Authors**
- Richard Wasonga - [GitHub Profile](https://github.com/Richard3wasonga)

## **Contributors**
- Bob Oyier - [GitHub Profile](https://github.com/oyieroyier)

---

## **License**

This project is open-source and available under the MIT License.

