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

from mysql.connector import connect
from collections import deque


class Book:
    def __init__(self, title="", author="", language="", isbn=""):
        self.title = title
        self.author = author
        self.language = language
        self.isbn = isbn

    def __str__(self):
        return f"Title:{self.title}\nAuthor:{self.author}\nLanguage:{self.language}\nISBN:{self.isbn}"

# LRU cache:
# use a doubly ended queue to store the isbn of books which we accessed most recently
# the head stores the most recectly accessed book
# the tail stores the least recently accessed book
# use a dictionary to store the key-value of the isbn and book object


class LocalBookCache:
    def __init__(self, capacity):
        self.book_records = {}
        self.query_history = deque([], capacity)
        self.capacity = capacity

    def get(self, isbn):
        # if the book isbn is not found in cache, return not found
        if isbn not in self.book_records:
            return False, Book("Not Found", "", "", isbn)
        # otherwise, move the book history to the head and return the book information in the book_records
        self.query_history.remove(isbn)
        self.query_history.appendleft(isbn)
        return True, self.book_records[isbn]

    def put(self, isbn, book):
        # if the book isbn is not found in cache,
        # store the new book information in the book_records, and move the isbn in the query_history to the head
        # otherwise, we only move the isbn in the query_history to the head
        if isbn not in self.book_records:
            self.book_records[isbn] = book

            # check whether the capacity of the deque of query_history is full
            # if it reaches the max length, we remove the tail element and corresponding record in book_records
            if len(self.query_history) == self.capacity:
                removed_isbn = self.query_history.pop()
                self.book_records.pop(removed_isbn)
        else:
            self.query_history.remove(isbn)
        self.query_history.appendleft(isbn)


# n is the capacity of local cache
# initialize LRU cache of local book records
n = 100
local_book_records = LocalBookCache(n)


def get_book_info(isbn):
    # if the input isbn is in the local cache, return the result from local
    # else query the specific book information from database
    found_in_cache, book = local_book_records.get(isbn)
    if not found_in_cache:
        found_in_database, new_book = retrieve_book_from_database(isbn)
        # if the isbn exists in databse, store the book locally and print the book information
        if found_in_database:
            LocalBookCache.put(new_book.isbn, new_book)
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
    db_connection = connect(host, user, password, database)
    select_book_query = f'SELECT title, author, language FROM {table} WHERE isbn = {isbn}'
    with db_connection.cursor() as cursor:
        cursor.execute(select_book_query)
        if not cursor.rowcount:
            return False, Book("Not Found", "", "", isbn)
        result = cursor.fetchall()
        title, author, language = result[0][0:3]
        return True, Book(title, author, language, isbn)
