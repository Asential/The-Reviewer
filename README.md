# Project 1

Web Programming with Python and JavaScript

[Website Showcase](https://www.youtube.com/watch?v=NlLtqCLHGNk&ab_channel=FilosophicalFellow)

Hello, I have made the book review site 'The Reviewer' with a Black-Gold Minimalistic theme.
	
	Index - Main page for logged out users.
	Home - Main page for logged in users.
	Login - Login page for logging in.
	Sign Up - Sign up page for signing up.
	Books - Page for searching the database of books.
	Search - Page for displaying the search results.
	Profile - Page to display all the reviews written by the user.
	Review - Page to display the information of book along with all the reviews of it written by the users.
	Logout - Logs the user out.

I have completed the requirements as follows:
	
	1. Users can register by filling in their Username, Email and Password on Login Page.
	2. Users can then Login using their credentials(Username and Password) on Signup Page.
	3. Users can Logout if they have logged in by clicking on the Logout button on navbar.
	4. All the books have been imported onto the database as directed.
	5. Users can search list of books on the Books page using alphabets/numbers/words. These can be year, author, title, ISBN also. I have used % % so as to match closests result.
	6. The Book page(named Review) displays the Title, Author, Year, ISBN, GoodReads API data and all the reviews submitted using the website.
	7. Users can submit a single review on each book with a text component and a rating ranging from 1 to 5 in form of stars. They won't be able to submit more than one review per book.
	8. As mentioned in 6, Goodreads data is diplayed(i.e. Rating, ISBN, Rating count, Review count)
	9. On the webistes /api/<isbn> route, the JSON data is displayed for the correct ISBN and a 404 Error is displayed on other cases.
	10. Almost all of the database commands are raw SQL Commands except one in login manager as I could get it to work without db.query()
	11. No other packages are installed.

Here are the details of files in the project:
	
	1. Each HTML file is extended from template.html. All the HTML File contain Nav-bar element except template.html and 404.html
	2. Various CSS properties have been used which are in index.css (They are a mess).
	3. searchbar.css contains the css for the animated search bar on Books page.
	4. stars.css contains the css for animated star rating system.
	5. search.py contains two search functions, one for full search and one for just ISBN.
	6. model.py contains various Classes and one function for star rating system.
	7. api.py contains the function for importing Goodreads data.
	8. fonts folder contains the particular fonts which are used on the website.

I hope I have matched all the requirments!

Thank You
-Asential
