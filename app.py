import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from flask_minify import Minify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import re
from htmlmin.main import minify
from csscompressor import compress as compress_css
from rjsmin import jsmin as compress_js
from scraper.scrape import tt_scrape  # Assuming the importing of your scraping logic

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize extensions
Compress(app)
Minify(app=app, html=True, js=True, cssless=True)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "5000 per hour"]
)

# Model for video downloads
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    download_date = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize the database
with app.app_context():
    db.create_all()

# Regex for URL validation
URL_REGEX = re.compile(
    r'^(https?:\/\/)?'
    r'((?:www\.|m\.)?tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com)'
    r'(:[0-9]{1,5})?'
    r'(\/[@\w\/.-]*)?'
    r'(\?[^\s]*)?$'
)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    rendered_template = render_template('index.html')
    minified_template = minify(rendered_template, remove_empty_space=True)
    minified_template = re.sub(
        r'<style>(.*?)<\/style>',
        lambda match: f"<style>{compress_css(match.group(1))}</style>",
        minified_template,
        flags=re.DOTALL
    )
    minified_template = re.sub(
        r'<script>(.*?)<\/script>',
        lambda match: f"<script>{compress_js(match.group(1))}</script>",
        minified_template,
        flags=re.DOTALL
    )
    return minified_template

@app.route('/download', methods=['GET'])
@limiter.limit("5000 per minute")
def download():
    tiktok_url = request.args.get('url')

    if not tiktok_url or not re.match(URL_REGEX, tiktok_url):
        logging.error('Invalid or missing URL parameter')
        return jsonify({'status': False, 'message': 'Invalid or missing URL parameter'}), 400

    try:
        data = tt_scrape(tiktok_url)
        # Assuming tt_scrape returns a dictionary with 'title' attribute when successful
        if data.get('status'):
            save_video_info(tiktok_url, data.get('title', 'No Title'))
            return jsonify(data)
        else:
            logging.warning('Failed to fetch video details')
            return jsonify({'status': False, 'message': 'Failed to fetch video details'}), 400
    except Exception as e:
        logging.error(f'Error scraping data: {e}')
        return jsonify({'status': False, 'message': 'Error scraping data'}), 500

# Helper function to save video info
def save_video_info(url, title):
    new_video = Video(url=url, title=title)
    db.session.add(new_video)
    db.session.commit()

@app.route('/videos')
def list_videos():
    videos = Video.query.all()
    return render_template('video_list.html', videos=videos)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
