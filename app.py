import yt_dlp as youtube_dl
import os
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads/"

# Cria a pasta de downloads caso não exista
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def convert_youtu_be_link(url):
    """Converte links encurtados de YouTube para o formato completo."""
    if "youtu.be" in url:
        video_id = url.split('/')[-1].split('?')[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

@app.route('/')
def index():
    """Renderiza a página inicial."""
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    """Faz o download do vídeo a partir da URL fornecida."""
    url = request.form.get('url')
    if not url:
        return "Erro: URL não fornecida.", 400

    try:
        # Converte o link se necessário
        url = convert_youtu_be_link(url)

        # Configurações do yt_dlp
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }

        # Realiza o download
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

        # Envia o arquivo baixado ao usuário
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Erro ao baixar o vídeo: {str(e)}", 500

if __name__ == '__main__':
    # Define a porta a partir da variável de ambiente ou usa 5000 como padrão
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True)
