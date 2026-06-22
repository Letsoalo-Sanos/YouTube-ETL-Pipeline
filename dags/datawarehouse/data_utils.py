from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

table = "yt_api"

def get_conn_cursor():
  hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt",database="elt_db")
  conn = hook.get_conn()
  cursor = conn.cursor(cursor_factory=RealDictCursor)
  return conn, cursor

def close_conn_cursor(conn, cursor):
  cursor.close()
  conn.close()

def create_schema(schema):

  conn, cursor = get_conn_cursor()

  schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"
  cursor.execute(schema_sql)
  conn.commit()

  close_conn_cursor(conn, cursor)

def create_table(schema):

  conn, cursor = get_conn_cursor()

  if schema == "staging":
    table_sql = f"""
    CREATE TABLE IF NOT EXISTS {schema}.{table} (
      video_id VARCHAR(20) PRIMARY KEY,
      "Video_Title" TEXT NOT NULL,
      "Upload_Date" TIMESTAMP NOT NULL,
      "Duration" VARCHAR(20) NOT NULL,
      "Video_Views" INTEGER,
      "Likes_Count" INTEGER,
      "Comments_Count" INTEGER
    );

    """

  else:
     table_sql = f"""
    CREATE TABLE IF NOT EXISTS {schema}.{table} (
      video_id VARCHAR(20) PRIMARY KEY,
      "Video_Title" TEXT NOT NULL,
      "Upload_Date" TIMESTAMP NOT NULL,
      "Duration" VARCHAR(20) NOT NULL,
      "Video_Views" INTEGER,
      "Likes_Count" INTEGER,
      "Comments_Count" INTEGER
    );

    """
     
  cursor.execute(table_sql)
  conn.commit()

  close_conn_cursor(conn, cursor)

def get_video_ids(cursor,schema):

  cursor.execute(f"SELECT video_id FROM {schema}.{table};")
  ids = cursor.fetchall()

  video_ids = [row["video_id"] for row in ids]

  return video_ids