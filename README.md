# YahooWebScrapeTest

Welcome to the this Basic Yahoo WebScraping Tool.
With this tool you can see recent stock prices given a companies
corresponding stock symbol.

A basic text-based UI has been implemented because this is quite a
application, but of course this could be extended to either a webapp
using dash or django, or a desktop application using tkinter, etc.

## src/webscrape.py
This is where the bulk of the application lies.  It just uses a few 
libraries, the most notable being requests, BeautifulSoup, and 
pandas (see requirements.txt for the full list).  A custom exception 
for the class was also created to better handle various exceptions 
that could then be passed to the frontend UI if given bad inputs.

## src/txt_ui.py
This is where the frontend lies.  It is a pretty simple application
style program with text inputs from command line user.

## src/main.py
This is just a very simple script for running the application.

## test/webscrape_test.py
There are three testcases that I wrote for this simple application.
Two were for testing exceptions (the custom exception and an index 
error exception that was possible in one of the functions)
One was for testing the correct instantiations of the backend.