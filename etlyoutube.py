from dagster import job, op
from googleapiclient.discovery import build
import pandas as pd
import re
import sqlite3

# إعداد API YouTube
api_key = 'AIzaSyB-r1HHifD3VzsOrs4cYSdxF7OFttCK6yY'
youtube = build('youtube', 'v3', developerKey=api_key)

@op
def search_youtube(context):
    request = youtube.search().list(
        part='snippet',
        q='Data Engineering',  # كلمة البحث
        type='video'
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        videos.append({
            "title": item['snippet']['title'],
            "description": item['snippet']['description'],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        })

    return videos

@op
def clean_data(context, videos):
    df = pd.DataFrame(videos)
    df['description'] = df['description'].apply(lambda x: re.sub(r'<.*?>', '', x))  # إزالة HTML
    df['title'] = df['title'].apply(lambda x: x.strip().lower())
    df['description'] = df['description'].fillna('')
    return df

@op
def save_to_db(context, df):
    conn = sqlite3.connect('youtube_data.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            url TEXT
        )
    ''')

    for _, row in df.iterrows():
        cursor.execute(''' 
            INSERT INTO videos (title, description, url)
            VALUES (?, ?, ?)
        ''', (row['title'], row['description'], row['url']))

    conn.commit()
    conn.close()

@job
def etl_youtube_data():
    videos = search_youtube()
    cleaned_data = clean_data(videos)
    save_to_db(cleaned_data)

# تشغيل الـ Job
etl_youtube_data.execute_in_process()
