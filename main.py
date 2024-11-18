import yt_dlp as youtube_dl
import os
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads/"

#

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def convert_youtu_be_link(url):
    if "youtu.be" in url:
        video_id = url.split('/')[-1].split('?')[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        return "Erro: URL não fornecida.", 400

    try:
        url = convert_youtu_be_link(url)

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Erro ao baixar o vídeo: {str(e)}", 500

if __name__ == '__main__':
    app.run()
