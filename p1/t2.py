import sqlite3


def get_connect():
    connect = sqlite3.connect("bookshop.db")
    return connect


def get_cursor(connect):
    return connect.cursor()


def fill_author_table(cursor):
    sql = """INSERT INTO author (name) VALUES
        ('Ivan'), ('Petr'), ('Victor')
    """
    cursor.execute(sql)


def create_book_table(cursor):
    sql = "CREATE TABLE book(id, name, pages, author_id)"


def main_add_authors():
    try:
        connect = get_connect()
        cursor = get_cursor(connect)
        fill_author_table(cursor)
        connect.commit()
        print("Successfull added authors")
    except AttributeError:
        print("AttributeError raised")
        connect.rollback()


if __name__ == "__main__":
    main_add_authors()
