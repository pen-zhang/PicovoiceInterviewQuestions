# PicovoiceInterviewQuestions

## Task 1

Assume we have a function get_book_info(isbn) that takes a string ISBN argument and retrieves a
struct/object containing the Title, Author, and Language of a book (each represented as a string) from a
database. Write a wrapper function that increases performance by keeping some of the database results in
memory for quick lookup.
To prevent memory from growing unbounded, we only want to store a maximum of N book records. At any
given time, we should be storing the N books that we accessed most recently. Assume that N can be a large
number when making decisions about choices of data structure(s) and algorithm(s).

- Use LRU cache to store the N book records. 

## Task 2

Use modern JavaScript and HTML5 to access information from the https://restcountries.eu/ API. The goal is
to display a list of all the capital cities for the country and all of its neighbouring countries. E.g. Searching for
“USA” will result in a list showing "Washington, D.C.", "Ottawa", and "Mexico City".

- Use the property "borders" in the returned country information to query the neighbouring countries
- To avoid making multiple N sequential calls to the API, use the code list to query the neighbouring countries instead

## Task 3

Implement a 5-star widget for an eCommerce site for users to record a product rating. The widget displays
a horizontal row of stars that are either outlined or black, according to the product rating, from left to right.
E.g. ★★★☆☆ = rating of 3.
Multiple 5-star widgets can be present on a single page. If a user has not rated a product, the widget will
have 5 outlined stars (☆☆☆☆☆). Each product on the page has a UUID.
Hovering over the Nth star will light up stars 1 to N with a grey colour (e.g. ★★★★☆). Clicking a star will
record the rating by sending a request to a web server with enough information to record the product and
the rating. After clicking, the widget will then display the rating the user submitted with black stars (e.g.
★★★★☆). Submitting the rating is handled without refreshing the page.

- Listen to  `mouseover` , `mouseleave`, `click` event to change the star
- Use `data-` attribute to mark the index of the hovered star which is used in a loop to change the stars
- TO DO: use REACT or VUE to rewrite

