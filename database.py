import sqlite3


class database:

    #   initializations
    def __init__(self, dbname="student_asst.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    #   if table doesn't exist, then it creates one, and some indexes, too.
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (owner_chat_id text, url text, store text, name text, product_or_course tinyint, value text)"
        owner_index = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner_chat_id ASC)"
        url_index = "CREATE INDEX IF NOT EXISTS urlIndex ON items (url ASC)"
        self.conn.execute(stmt)
        self.conn.execute(owner_index)
        self.conn.execute(url_index)
        self.conn.commit()
    
    #   adds a course or a product to db
    def add_item(self, owner, url, store, name, productOrCourse, value):
        stmt = "INSERT INTO items (owner_chat_id, url, store, name, product_or_course, value) VALUES (?,?,?,?,?,?)"
        args = (owner, url, store, name, productOrCourse, value, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    #   deletes a course from db
    def delete_course(self, owner, url):
        stmt = "DELETE FROM items WHERE owner_chat_id = (?) AND url = (?)"
        args = (owner, url, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    #   deletes product from db
    def delete_product(self, owner, store, name):
        stmt = "DELETE FROM items WHERE owner_chat_id = (?) AND store = (?) AND name = (?)"
        args = (owner, store, name )
        self.conn.execute(stmt, args)
        self.conn.commit()

    #   returns all the courses or all the products according to the indicator
    def get_items(self, owner, indicator):
        if indicator == 1:
            stmt = "SELECT url FROM items WHERE owner_chat_id = (?) AND product_or_course = (?)"
            args = (owner, indicator, )
            return [x[0] for x in self.conn.execute(stmt, args)]
        else:
            stmt = "SELECT store, name FROM items WHERE owner_chat_id = (?) AND product_or_course = (?)"
            args = (owner, indicator, )
            return [x for x in self.conn.execute(stmt, args)]

    #   returns the last modification date of a course website from db
    def get_date(self, owner, url):
        stmt = "SELECT value FROM items WHERE owner_chat_id = (?) AND url = (?)"
        args = (owner, url, )
        return [x[0] for x in self.conn.execute(stmt, args)]
    
    #   returns the price of a product from db
    def get_price(self, owner, store, name):
        stmt = "SELECT value FROM items WHERE owner_chat_id = (?) AND store = (?) AND name = (?)"
        args = (owner, store, name, )
        return [x[0] for x in self.conn.execute(stmt, args)]
    
    #   updates the date of a course website, or the price of a product
    def update_value(self, new_value, owner, url):
        stmt = "UPDATE items SET value = (?) WHERE owner_chat_id = (?) AND url = (?)"
        args = (new_value, owner, url, )
        if "http" in url:
            self.conn.execute(stmt, args)
        self.conn.commit()
    
    #   returns the url of a product by using its name, and store
    def get_url(self, owner, store, name):
        stmt = "SELECT url FROM items WHERE owner_chat_id = (?) AND store = (?) AND name = (?)"
        args = (owner, store, name)
        return [x[0] for x in self.conn.execute(stmt, args)]
