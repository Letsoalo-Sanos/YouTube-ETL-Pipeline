from airflow.providers.postgres.hooks.postgres import PostgresHook
from pyscopg2.extras import RealDictCursor

def get_conn_cursor():
  hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt",database="elt_db")
  conn = hook.get_conn()
  cursor = conn.cursor(cursor_factory=RealDictCursor)
  return conn, cursor

def close_conn_cursor(conn, cursor):
  cursor.close()
  conn.close()
