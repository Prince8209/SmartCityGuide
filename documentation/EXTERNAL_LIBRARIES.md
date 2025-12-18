# External Libraries & Dependencies

This document lists all external libraries used in the Smart City Guide project and explains **why** they are necessary.

## 1. Backend Dependencies

These are Python packages listed in `requirements.txt`.

| Library | Version | Why is it used? |
| :--- | :--- | :--- |
| **`Flask`** | 3.0.0 | **The Web Framework**. It handles the HTTP requests, routing, and overall structure of the backend application. Used because it's lightweight and flexible. |
| **`Flask-CORS`** | 4.0.0 | **Cross-Origin Resource Sharing**. Allows the Frontend (running on a browser) to make API requests to the Backend. Without this, the browser would block the connection for security reasons. |
| **`Flask-SQLAlchemy`**| 3.1.1 | **Database ORM**. Allows us to interact with the database using Python classes (`User`, `City`) instead of writing raw SQL queries. It simplifies database operations. |
| **`PyJWT`** | 2.8.0 | **Authentication**. Used to generate and verify **JSON Web Tokens (JWT)**. When a user logs in, we give them a token. |
| **`python-dotenv`** | 1.0.0 | **Configuration**. Loads secret keys and database credentials from the `.env` file into environment variables, keeping sensitive data out of the code. |
| **`pymysql`** | 1.1.0 | **Database Driver**. The actual connector that allows Python to talk to the MySQL database server. |
| **`Werkzeug`** | 3.0.1 | **Utilities**. A dependency of Flask. It handles the low-level WSGI (Web Server Gateway Interface) details. |
| **`cryptography`** | 41.0.7 | **Security**. Provides cryptographic primitives, often required by `PyJWT` or `pymysql` for secure connections. |

## 2. Frontend Dependencies

These are libraries included in the HTML files.

| Library | Type | Why is it used? |
| :--- | :--- | :--- |
| **Font Awesome** | CSS/Icon Font | **Icons**. Used for all the icons you see (e.g., user profile `<i class="fas fa-user"></i>`, city buildings `<i class="fas fa-city"></i>`). It allows for scalable, vector icons. |
| **Google Fonts** | Font | **Typography**. Used to give the website a modern and clean look, distinct from standard system fonts. |

*Note: The Frontend is primarily built with **Vanilla JavaScript**, meaning it does not rely on heavy frameworks like React, Vue, or jQuery.*
