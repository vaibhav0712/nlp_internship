import csv
import mysql.connector
from mysql.connector import Error
from typing import List
import detection


def create_tables(conn):
    try:
        cursor = conn.cursor()

        # Create master table (blog_posts)
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS blog_posts (
            blog_id INT AUTO_INCREMENT PRIMARY KEY,
            blog_title TEXT NOT NULL,
            blog_text TEXT NOT NULL
        )
        """
        )

        # Create organizations table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS organizations (
            org_id INT AUTO_INCREMENT PRIMARY KEY,
            org_name VARCHAR(255) NOT NULL,
            blog_id INT,
            FOREIGN KEY (blog_id) REFERENCES blog_posts(blog_id)
        )
        """
        )

        # Create categories table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS categories (
            cat_id INT AUTO_INCREMENT PRIMARY KEY,
            cat_name VARCHAR(255) NOT NULL,
            blog_id INT,
            FOREIGN KEY (blog_id) REFERENCES blog_posts(blog_id)
        )
        """
        )

        conn.commit()
    except Error as e:
        print(f"Error creating tables: {e}")


def insert_data(
    conn, title: str, text: str, organizations: List[str], categories: List[str]
):
    try:
        cursor = conn.cursor()

        # Insert into blog_posts
        cursor.execute(
            "INSERT INTO blog_posts (blog_title, blog_text) VALUES (%s, %s)",
            (title, text),
        )
        blog_id = cursor.lastrowid

        # Insert organizations
        for org in organizations:
            cursor.execute(
                "INSERT INTO organizations (org_name, blog_id) VALUES (%s, %s)",
                (org, blog_id),
            )

        # Insert categories
        for cat in categories:
            cursor.execute(
                "INSERT INTO categories (cat_name, blog_id) VALUES (%s, %s)",
                (cat, blog_id),
            )

        conn.commit()
    except Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()


def process_csv(csv_file: str, db_config: dict):
    try:
        conn = mysql.connector.connect(**db_config)
        create_tables(conn)

        with open(csv_file, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            count = 0
            for row in csv_reader:
                try:
                    title = row["title"]
                    text = row["text"]
                    organizations = detection.detect_organization(text)
                    categories = detection.classify_blog(text)
                    insert_data(conn, title, text, organizations, categories)
                    print(
                        "Data has been successfully processed and stored in the database.",
                        count,
                    )
                    count += 1
                except:
                    print("Error processing data", count)
                    count += 1
                    continue
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()


if __name__ == "__main__":
    csv_file = "../data/data_chunk/_9.csv"  # give chunk to model
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Vaibhav@712",
        "database": "blog_inferencing",
    }
    process_csv(csv_file, db_config)
