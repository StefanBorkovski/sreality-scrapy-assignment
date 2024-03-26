import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

def create_connection() -> psycopg2.extensions.connection:
    """Connects to the database using predefined configuration in .env file.

    Returns:
        psycopg2.extensions.connection: postgres connection
    """
    return psycopg2.connect(
            host=os.environ['HOST'],
            port=os.environ['PORT'],
            database=os.environ['DB_NAME'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD']
            )

def load_apartments() -> list:
    """Query all entries from the apartments database.

    Returns:
        list: list of stored apartments
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('SELECT title, price, img_url FROM apartments;')
    apartments = cur.fetchall()
    cur.close()
    conn.close()
    return apartments

@app.route('/')
def render() -> str:
    """Renders the apartments input using the index.html file.

    Returns:
        str: rendered content
    """
    return render_template('index.html', apartments=load_apartments())

if __name__ == '__main__':
    # load environmental variables
    load_dotenv()
    # web app run
    app.run(debug=True, host='0.0.0.0')