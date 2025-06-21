import sqlite3
#create a connection to the SQLIte database
def create_connection():
    conn=sqlite3.connect('budget_app.db')
    return conn
# create a user table
def create_user_table():
    conn = create_connection()
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_table(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    
#create  new user in database  
def create_user(username,password):
      conn = create_connection()
      c=conn.cursor()
      c.execute('INSERT INTO user_table (username,password) VALUES (?,?)',(username,password))
      conn.commit()
      conn.close()
      
def authenticate_user(username,password):
    conn = create_connection()
    c=conn.cursor()
    c.execute('SELECT * FROM user_table WHERE username = ? AND password = ?',(username,password))
    user = c.fetchone()
    conn.close()
    return user

def create_categories_table():
     conn = create_connection()
     c=conn.cursor()
     c.execute('''CREATE TABLE IF NOT EXISTS categories_table(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         user_id INTEGER,
         category_name TEXT NOT NULL,
         category_type TEXT NOT NULL CHECK(category_type IN('expense','income','savings')),
         FOREIGN KEY (user_id) REFERENCES user_table(id))''')
     conn.commit()
     conn.close()
         
create_connection()
create_categories_table()

    