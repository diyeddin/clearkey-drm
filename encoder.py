import os
import sys
import uuid
import psycopg2


def encode_video(video_name, output_name):
    kid = uuid.uuid4()
    key = uuid.uuid4()
    encoding = {"kid":kid, "key":key}

    command = f"packager in={video_name},stream=audio,output={output_name}_audio.mp4,playlist_name={output_name}_audio.m3u8,drm_label=AUDIO in={video_name},stream=video,output={output_name}_video.mp4,playlist_name={output_name}_video.m3u8,drm_label=VIDEO --enable_raw_key_encryption --keys label=AUDIO:key_id={kid.hex}:key={key.hex},label=VIDEO:key_id={kid.hex}:key={key.hex} --hls_master_playlist_output {output_name}_master.m3u8"
    os.system(command)

    return encoding


def insert_value(db, cols, values):
    connection = psycopg2.connect(database=db["database"],
                                  host=db["host"],
                                  user=db["user"],
                                  password=db["password"],
                                  port=db["port"])

    cursor = connection.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS clear_key_decodeds (type VARCHAR, id BYTEA, value BYTEA)')
    print("table created successfully")
    
    sql = f"INSERT INTO clear_key_decodeds({cols[0]}, {cols[1]}, {cols[2]}) VALUES('{values[0]}', '{values[1]}', '{values[2]}')"
    cursor.execute(sql)
    print("row inserted successfully")
    
    connection.commit()
    cursor.close()
    connection.close()


def fetch_data(db, col, criteria):
    connection = psycopg2.connect(database=db["database"],
                                  host=db["host"],
                                  user=db["user"],
                                  password=db["password"],
                                  port=db["port"])
    cursor = connection.cursor()
    sql = f"SELECT * FROM clear_key_decodeds WHERE {col}='{criteria}'"
    cursor.execute(sql)

    row = cursor.fetchone()
    print(row)
    
    connection.commit()
    cursor.close()
    connection.close()

def drop_table(db, table):
    connection = psycopg2.connect(database=db["database"],
                                  host=db["host"],
                                  user=db["user"],
                                  password=db["password"],
                                  port=db["port"])
    
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE {table}')

    print(f"table: {table} dropped")

    connection.commit()
    cursor.close()
    connection.close()


def delete_entries(db, table):
    connection = psycopg2.connect(database=db["database"],
                                  host=db["host"],
                                  user=db["user"],
                                  password=db["password"],
                                  port=db["port"])
    
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM {table}')

    print(f"deleted all entries from {table}")

    connection.commit()
    cursor.close()
    connection.close()


def connect_db(db):
    pass

if __name__=='__main__':
    video_name = sys.argv[1]
    output_name = sys.argv[2]
    db_config = {"database":"postgres",
             "host":"127.0.0.1",
             "user":"postgres",
             "password":"postgres",
             "port":"5433"}
    
    encoding = encode_video(video_name, output_name)
    print("video encoding:", encoding)
    insert_value(db_config, ["type", "id", "value"], ("oct", encoding["kid"], encoding["key"]))
    fetch_data(db_config, "id", encoding["kid"])
