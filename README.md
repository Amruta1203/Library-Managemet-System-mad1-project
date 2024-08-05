# Library Management System

## Overview

The Library Management System is a multi-user web application designed to facilitate the management and access of e-books. This project leverages the Flask framework for the application code, Jinja2 templates combined with  for HTML and CSS generation and styling, and SQLite for data storage. The system is designed to operate locally using any IDE without the need for additional server setups for database and frontend management.

## Features

### Core Functionality

1. **User and Librarian Authentication:**
   - Separate login forms for users and librarians.
   - Simple HTML form-based login.

2. **User Functionalities:**
   - Login and registration capabilities.
   - View existing sections and e-books.
   - Request and return e-books.
   - Provide feedback for e-books.
   - Access e-books for a limited period (for 7 days).

3. **Librarian Functionalities:**
   - Issue and revoke e-books for users.
   - Add, edit, and remove sections and e-books.
   - Assign books to sections.
   - Monitor the status of e-books and their current users.

4. **Section and Book Management:**
   - Sections have ID, name, date created, and description.
   - Books have ID, name, content, author(s), date issued, and return date.
   - Recent additions and top-rated books are automatically displayed.

5. **Search Functionality:**
   - Search for sections and e-books by various criteria.

### Recommended Enhancements

- **Download E-books:**
  - Allow users to download e-books as PDFs for a fee.

- **API Integration:**
  - CRUD operations on e-books.
  - Additional APIs for generating graphs for the librarian dashboard.

- **Payment for the Books**
  - Sample payment gateway has been created for users who wish to buy the books.


## Evaluation

This project has been rigorously evaluated by esteemed professors from IIT Madras and industry professionals. It has received a perfect score of 100/100 (S grade), acknowledging its comprehensive implementation and adherence to the project requirements.

## Project Setup

1. **Frameworks and Tools:**
   - Flask for the backend.
   - Jinja2 for the frontend.
   - SQLite for the database.

2. **Running the Application:**
   - Ensure all dependencies are installed.
   - Run the Flask application locally.

## Conclusion

The Library Management System is a robust application designed to streamline e-book management and access for both users and librarians. Its evaluation by top academicians and industry experts underscores the quality and functionality of the system.

---

