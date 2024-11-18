import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    return psycopg2.connect(
        dbname="blog",
        user="postgres",
        password="absa",
        host="localhost",
        port=5432,
        cursor_factory=RealDictCursor,
    )


def get_posts(search=None):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            if search:
                cursor.execute(
                    """
                SELECT posts.id, title, description, date_post, username, image, comments  FROM posts INNER JOIN users ON posts.author_id=users.id WHERE title LIKE %s;
                """,
                    ("%" + search + "%",),
                )
            else:
                cursor.execute(
                    """
                SELECT posts.id, title, description, date_post, username, image, comments  FROM posts INNER JOIN users ON posts.author_id=users.id;
                """
                )
            posts = cursor.fetchall()
    return posts


def add_post(title, description, date_post, image):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO posts (title, description, date_post, image, author_id)
                VALUES (%s, %s, %s, %s, 1);
                """,
                (title, description, date_post, image),
            )
            connection.commit()


def change_post(id, title, description):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    UPDATE posts
                    SET title = %s, description = %s
                    WHERE id = %s;
                    """,
                (
                    title,
                    description,
                    id,
                ),
            )
            connection.commit()


def add_comment(id, comment):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    UPDATE posts
                    SET comments = comments || %s
                    WHERE id = %s;
                    """,
                (
                    [comment],
                    id,
                ),
            )
            connection.commit()


def delete_post(id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    DELETE FROM posts
                    WHERE id = %s;
                    """,
                (id,),
            )
            connection.commit()


def delete_comment(comment, id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    Update posts
                    SET comments = array_remove(comments, %s)
                    WHERE id = %s;
                    """,
                (
                    comment,
                    id,
                ),
            )
            connection.commit()


def change_comment(old_comment, new_comment, id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    Update posts
                    SET comments = array_replace(comments, %s, %s )
                    WHERE id = %s;
                    """,
                (
                    old_comment,
                    new_comment,
                    id,
                ),
            )
            connection.commit()


def get_post(id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT posts.id, title, description, date_post, username, image, comments  FROM posts INNER JOIN users ON posts.author_id=users.id
                WHERE posts.id = (%s);
                """,
                (id,),
            )
            post = cursor.fetchone()
            return post
