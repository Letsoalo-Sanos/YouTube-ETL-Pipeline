from datawarehouse.data_utils import get_conn_cursor, close_conn_cursor, create_schema, create_table,get_video_ids
from datawarehouse.data_modification import insert_rows, update_rows, delete_rows
from datawarehouse.data_loading import load_data
from datawarehouse.data_transformation import transform_data


import logging
from airflow.decorators import task

logger = logging.getLogger(__name__)
table = "yt_api"


def normalize_staging_row(row):
    return {
        "video_id": row.get("video_id"),
        "Video_Title": row.get("title", row.get("Video_Title")),
        "Upload_Date": row.get("publishedAt", row.get("Upload_Date")),
        "Duration": row.get("duration", row.get("Duration")),
        "Video_Views": row.get("viewCount", row.get("Video_Views")),
        "Likes_Count": row.get("likeCount", row.get("Likes_Count")),
        "Comments_Count": row.get("commentCount", row.get("Comments_Count")),
    }

@task
def staging_table():

    schema = "staging"

    conn, cursor = None, None

    try:
        conn, cursor = get_conn_cursor()

        YouTube_Data = load_data()

        create_schema(schema)
        create_table(schema)

        table_ids = get_video_ids(cursor,schema)

        for raw_row in YouTube_Data:
            row = normalize_staging_row(raw_row)

            if len(table_ids) == 0:
                insert_rows(cursor,conn,schema,row)

            else:
                if row['video_id'] in table_ids:
                    update_rows(cursor,conn,schema,row)
                else:
                    insert_rows(cursor,conn,schema,row)

        ids_in_json = {row['video_id'] for row in YouTube_Data}
        ids_in_delete = set(table_ids) - ids_in_json

        if ids_in_delete:
            delete_rows(cursor,conn,schema,ids_in_delete)

        logger.info(f"{schema} table update completed")
        
    except Exception as e:
        logger.error(f"An error occurred during the update of {schema} table: {e}")
        raise
    
    finally:
         if cursor and conn:
            close_conn_cursor(conn, cursor)
           
           
@task
def core_table():
   
    schema = 'core'
   
    conn, cursor = None, None
   
    try:
        conn, cursor = get_conn_cursor()
       
        create_schema(schema)
        create_table(schema)
       
       
        table_ids = get_video_ids(cursor, schema)
        current_video_ids = set()
       
        cursor.execute(f"SELECT video_id FROM {schema}.{table};")
        rows = cursor.fetchall()
       
        for row in rows:
            current_video_ids.add(row['video_id'])
           
            if len(table_ids) == 0:
                transformed_row = transform_data(row)
                insert_rows(cursor, conn, schema, transformed_row)
            else:
                transformed_row= transform_data(row)
               
                if transformed_row['video_id'] in table_ids:
                    update_rows(cursor, conn, schema, transformed_row)
                else:
                    insert_rows(cursor, conn, schema, transformed_row)
                   
                   
            ids_to_delete = set(table_ids)-current_video_ids
           
           
            if ids_to_delete:
                delete_rows(cursor, conn, schema, ids_to_delete)
            logger.info(f"{schema} table update completed")
       
    except Exception as e:
        logger.error(f"Error occurred while updating core table {schema}.{table}: {e}")
        raise
   
    finally:
        if cursor and conn:
            close_conn_cursor(conn, cursor)
        
      
    

