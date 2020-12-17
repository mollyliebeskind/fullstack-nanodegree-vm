# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  conn = psycopg2.connect("dbname=forum")
  cursor = conn.cursor()
  cursor.execute("SELECT content, time FROM posts order by time desc;")
  results = cursor.fetchall()
  conn.close()
  return results

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""

  clean_content = bleach.clean(content)

  conn = psycopg2.connect("dbname=forum")
  cursor = conn.cursor()
  cursor.execute("INSERT INTO posts (content) VALUES (%s);", (clean_content,))
  conn.commit()
  conn.close()


