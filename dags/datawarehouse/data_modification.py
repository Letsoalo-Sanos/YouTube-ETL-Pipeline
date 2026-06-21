import logging

logger = logging.getLogger(__name__)
table = "yt_api"

def insert_rows(cursor,conn,schema,row):

    try:
        
        if schema == "stagging":
            video_id = "video_id"

            cursor.execute(
                f"""INSERT INTO {schema}.{table} (video_id, "Video_Title", "Upload_Date", "Duration", "Video_Views", "Likes_Count", "Comments_Count")
                VALUES (%(video_id)s, %(Video_Title)s, %(Upload_Date)s, %(Duration)s, %(Video_Views)s, %(Likes_Count)s, %(Comments_Count)s);
                """,row
            )
        else:
            video_id = "video_id"
            cursor.execute(
                f"""INSERT INTO {schema}.{table} (video_id, "Video_Title", "Upload_Date", "Duration", "Video_Views", "Likes_Count", "Comments_Count")
                VALUES (%(video_id)s, %(Video_Title)s, %(Upload_Date)s, %(Duration)s, %(Video_Views)s, %(Likes_Count)s, %(Comments_Count)s);
                """,row
            )

        conn.commit()

        logger.info(f"Inserted video_id: {row['video_id']} into {schema}.{table}")

    except Exception as e:
        logger.error(f"Error inserting video_id: {row['video_id']} into {schema}.{table} - {e}")
        raise e
    
def update_rows(cursor,conn,schema,row):
    
    try:
        # staging
        if schema == "staging":
            video_id = "video_id"
            upload_date = "publishedAt"
            video_title = "title"
            video_views = "viewCount"
            likes_count = "likeCount"
            comments_count = "commentCount"

        # core
        else:
            video_id = "video_id"
            upload_date = "Upload_Date"
            video_title = "Video_Title"
            video_views = "Video_Views"
            likes_count = "Likes_Count"
            comments_count = "Comments_Count"

        cursor.execute(
            f"""UPDATE {schema}.{table}
            SET "Video_Title" = %(Video_Title)s,
                "Video_Views" = %(Video_Views)s,
                "Likes_Count" = %(Likes_Count)s,
                "Comments_Count" = %(Comments_Count)s
            WHERE video_id = %(video_id)s AND "Upload_Date" = %(Upload_Date)s;
            """,row
        )

        conn.commit()

        logger.info(f"Updated video_id: {row['video_id']} in {schema}.{table}")

    except Exception as e:
        logger.error(f"Error updating video_id: {row['video_id']} in {schema}.{table} - {e}")
        raise e

def delete_rows(cursor,conn,schema,ids_to_delete):
    try:
        
        ids_to_delete = f"""({','.join(f"'{id}'" for id in ids_to_delete)})"""

        cursor.execute(
            f"""DELETE FROM {schema}.{table}
            WHERE video_id IN {ids_to_delete};
            """
        )

        conn.commit()
        logger.info(f"Deleted video_ids: {ids_to_delete} from {schema}.{table}")


    except Exception as e:
        logger.error(f"Error deleting video_ids: {ids_to_delete} from {schema}.{table} - {e}")
        raise e