'''
Assume we have a function get_book_info(isbn) that takes a string ISBN argument and retrieves a
struct/object containing the Title, Author, and Language of a book (each represented as a string) from a
database. Write a wrapper function that increases performance by keeping some of the database results in
memory for quick lookup.
To prevent memory from growing unbounded, we only want to store a maximum of N book records. At any
given time, we should be storing the N books that we accessed most recently. Assume that N can be a large
number when making decisions about choices of data structure(s) and algorithm(s).
'''

# implement the LRU cache to store the book records for quick lookup
# if there is no local data, connect to mysql database to query the book by isbn,
# and select the book info "Title, Author, Language", then store them in cache

# pip install mysql-connector-python
from mysql.connector import connect, Error


class Book:
    def __init__(self, title="", author="", language="", isbn=""):
        self.title = title
        self.author = author
        self.language = language
        self.isbn = isbn

    def __str__(self):
        return f"\nTitle:{self.title}\nAuthor:{self.author}\nLanguage:{self.language}\nISBN:{self.isbn}\n"

# LRU cache:
# use a doubly linked list to store the isbn and book object
# the head stores the most recectly accessed book
# the tail stores the least recently accessed book
# use a dictionary to store the book isbn and the node containing the book infomation


class DoublyLinkedNode:
    def __init__(self, isbn="", book=None):
        self.isbn = isbn
        self.book = book
        self.pre = None
        self.next = None


class LocalBookCache:
    def __init__(self, capacity):
        self.book_records = {}
        self.head = DoublyLinkedNode()
        self.tail = DoublyLinkedNode()
        self.head.next = self.tail
        self.tail.pre = self.head
        self.capacity = capacity
        self.size = 0

    def get(self, isbn):
        # if the book isbn is not found in cache, return not found
        if isbn not in self.book_records:
            return False, None

        # otherwise, move the book record to the head and return the book information in the book_records
        node = self.book_records[isbn]
        self.move_to_head(node)
        return True, node.book

    def put(self, isbn, book):
        # store the new book information in the book_records, and move the isbn in the query_history to the head
        node = DoublyLinkedNode(isbn, book)
        self.book_records[isbn] = node
        self.add_to_head(node)
        self.size += 1
        # check whether the capacity of the cache is full
        # if the size is over the capacity, we remove the tail node and corresponding record in book_records
        if self.size > self.capacity:
            removed = self.remove_tail()
            self.book_records.pop(removed.isbn)
            self.size -= 1

    def add_to_head(self, node):
        node.pre = self.head
        node.next = self.head.next
        self.head.next.pre = node
        self.head.next = node

    def remove_node(self, node):
        node.pre.next = node.next
        node.next.pre = node.pre

    def move_to_head(self, node):
        self.remove_node(node)
        self.add_to_head(node)

    def remove_tail(self):
        node = self.tail.pre
        self.remove_node(node)
        return node


# n is the capacity of local cache
# initialize LRU cache of local book records
n = 3
local_book_records = LocalBookCache(n)


def get_book_info(isbn):
    # if the input isbn is in the local cache, return the result from local
    # else query the specific book information from database
    found_in_cache, book = local_book_records.get(isbn)
    if not found_in_cache:
        found_in_database, new_book = retrieve_book_from_database(isbn)
        # if the isbn exists in databse, store the book locally and print the book information
        if found_in_database:
            local_book_records.put(new_book.isbn, new_book)
        print(new_book)
    else:
        print(book)


# establish the connection to the database and retrieve the specific book information
def retrieve_book_from_database(isbn):
    host = ""
    user = ""
    password = ""
    database = ""
    table = ""
    try:
        db_connection = connect(host=host, user=user, password=password, database=database)
    except Error as e:
        print(e)
        return False, "Failed connect to database"

    select_book_query = f'SELECT title, author, language FROM {table} WHERE isbn = {isbn}'
    with db_connection.cursor() as cursor:
        cursor.execute(select_book_query)
        if not cursor.rowcount:
            return False, Book("Not Found", "", "", isbn)
        result = cursor.fetchall()
        title, author, language = result[0][0:3]
        return True, Book(title, author, language, isbn)


if __name__ == "__main__":
    print("Test")
    book1 = Book("NAUGHTY GAY ADULT BEDTIME STORIES",
                 "Thele, Dale", "Engligh", "978-0-578-93197-5")
    book2 = Book("MY POPZ AND THE LESSONS HE TAUGHT ME",
                 "Johnson, Cameron", "Engligh", "978-1-7923-7037-3")
    book3 = Book("NM CAR CLUBS", "Sena, Art", "English", "978-1-7923-7034-2")
    book4 = Book("TREASURES OF WISDOM", "Brown, Ron", "English", "978-1-7923-7031-1")
    
    local_book_records.put(book1.isbn, book1)
    local_book_records.put(book2.isbn, book2)
    local_book_records.put(book3.isbn, book3)
    # cache [book3, book2, book1]
    get_book_info(book1.isbn)
    get_book_info(book2.isbn)
    get_book_info(book3.isbn)
    
    local_book_records.put(book4.isbn, book4)
    # cache [book4, book3, book2]
    get_book_info(book4.isbn)
    get_book_info(book1.isbn) # not found
    
    get_book_info(book2.isbn)
    # cache [book2, book4, book3]    
    local_book_records.put(book1.isbn,book1)
    # cache [book1, book2, book4]
    get_book_info(book3.isbn) # not found

