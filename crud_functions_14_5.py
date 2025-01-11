import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price TEXT NOT NULL
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
        )
    ''')

    connection.commit()


def check_and_populate_products():
    cursor.execute('SELECT COUNT(*) FROM Products')
    count = cursor.fetchone()[0]
    if count == 0:
        for i in range(1, 5):
            cursor.execute(
                'INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                (f'Продукт {i}', f'Описание {i}', f'{i*100}')
            )
    else:
        pass

    connection.commit()

# def populate_products():
#     cursor.executescript('''
#         INSERT INTO Products (title, description, price) VALUES (
#             "EcoGreen Multi",
#             "Мультивитамины без железа, в капсулах, 180 шт.",
#             40);
#         INSERT INTO Products (title, description, price) VALUES (
#             "Magnesium Glycinate",
#             "Пищевая добавка «Магния глицинат» 100 мг, 180 шт.",
#             32);
#         INSERT INTO Products (title, description, price) VALUES (
#             "Omega-3",
#             "Капсулы «Омега-3» 1000 мг, 200 шт.",
#             20);
#         INSERT INTO Products (title, description, price) VALUES (
#             "PQQ Energy",
#             "Пирролохинолинхинон, 30 шт.",
#             30);
#     ''')
#     connection.commit()

def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    return products


def add_user(username, email, age, balance=1000):
    cursor.execute(
        'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
        (username, email, age, balance))
    connection.commit()


def is_included(username):
    return True \
        if cursor.execute('SELECT COUNT(*) from Users WHERE username = ?',
                          (username, )).fetchone()[0] \
        else False


def products_is_empty():
    return not cursor.execute('SELECT COUNT(*) from Products').fetchone()[0]


if __name__ == '__main__':
    initiate_db()
    if products_is_empty():
        check_and_populate_products()
    connection.close()