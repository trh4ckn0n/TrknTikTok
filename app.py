import streamlit as st
import re
import logging
from datetime import datetime
import sqlite3

# Define URL_REGEX at the top level of the script
URL_REGEX = re.compile(
    r'^(https?:\/\/)?'
    r'((?:www\.|m\.)?tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com)'
    r'(:[0-9]{1,5})?'
    r'(\/[@\w\/.-]*)?'
    r'(\?[^\s]*)?$'
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize database
def init_db():
    conn = sqlite3.connect('videos.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS videos
                    (id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    download_date TIMESTAMP);''')
    return conn

# Save video info function
def save_video_info(conn, url, title):
    conn.execute("INSERT INTO videos (url, title, download_date) VALUES (?, ?, ?)",
                 (url, title, datetime.utcnow()))
    conn.commit()

# Function to process the video download
def process_download(tiktok_url):
    if not tiktok_url or not re.match(URL_REGEX, tiktok_url):
        st.error('Invalid or missing URL parameter')
        return None

    try:
        # Make sure tt_scrape function is correctly imported and available in your script
        data = tt_scrape(tiktok_url)
        if data.get('status'):
            conn = init_db()
            save_video_info(conn, tiktok_url, data.get('title', 'No Title'))
            conn.close()
            return data
        else:
            st.warning('Failed to fetch video details')
            return None
    except Exception as e:
        logging.error(f'Error scraping data: {e}')
        st.error('Error scraping data')
        return None

# UI setup
st.title("TikTokPy Streamlit App")
tiktok_url = st.text_input("Enter TikTok URL:")
if st.button("Download"):
    data = process_download(tiktok_url)
    if data:
        st.success(f"Video '{data.get('title')}' fetched successfully!")
        st.image(data.get('thumbnail_url'))  # Ensure tt_scrape provides a valid thumbnail URL
        st.write("Download Options: ")
        st.download_button("Download Video", data.get('video_link'))   # Ensure correct download link handling
        st.download_button("Download Audio", data.get('audio_link'))   # Ensure correct download link handling

# Display past downloads
if st.checkbox("Show Past Downloads"):
    conn = init_db()
    downloads = conn.execute("SELECT title, url, download_date FROM videos").fetchall()
    conn.close()
    for download in downloads:
        st.write(f"{download[0]} - {download[1]} - Downloaded on {download[2]}")
