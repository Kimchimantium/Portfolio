# Portfolio Website with Flask

This project is a portfolio website built with Flask, showcasing various projects and blog posts. It utilizes Flask extensions such as Flask-Bootstrap for styling, Flask-CKEditor for text editing, Flask-Login for user authentication, and Flask-Migrate for database migrations. The website features a dynamic blog where users can register, log in, create, edit, and delete posts, as well as comment on them.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or later installed
- pip for installing Python packages

## Setup and Installation

To set up the project for development on your local machine, follow these steps:

1. **Clone the repository**

    ```bash
    git clone https://github.com/Kimchimantium/Portfolio.git
    cd your-project-folder
    ```

2. **Create and activate a virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install required packages**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment variables**

    Create a `.env` file in the root directory of the project and add the following variables:

    ```plaintext
    SECRET_KEY=your_secret_key
    ADMIN_EMAIL=your_admin_email@example.com
    ```

    Replace `your_secret_key` and `your_admin_email@example.com` with your own secret key and admin email.

5. **Initialize the database**

    ```bash
    flask db upgrade
    ```

## Running the Application

To run the application on your local machine, execute:

```bash
flask run --port=9080
