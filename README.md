# scrapes_kaufland_website

Program to Automatically Extract Selected Information from a Kaufland Website
This program allows users to automatically extract specific information from a Kaufland website. The user provides only the webpage URL and the XPath, which can be easily copied from the browser.

Features:
Command-line input using click: The program utilizes the click library for user-friendly input of the URL and XPath.
Modular structure: The code is divided into functions for better organization and easier testing.
Testing: Includes several tests, starting with a "happy path" for the simplest cases, followed by edge case tests.
Text cleanup: When extracting text from the HTML, the program removes leading and trailing whitespace and replaces newline characters with spaces.
Output format: Each extracted HTML element is displayed on a separate line.
Documentation with docstrings: The code is documented with clear docstrings, providing useful details about functionality and usage.
This program is designed to simplify data extraction from web pages, ensuring accuracy and ease of use.
