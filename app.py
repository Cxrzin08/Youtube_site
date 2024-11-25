import os
from flask import Flask, render_template, request, send_file
import yt_dlp as youtube_dl

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
        url = convert_youtu_be_link(url)

        # Caminho do arquivo de cookies (certifique-se de que o arquivo cookies.txt está no mesmo diretório do script)
        cookies_file = os.path.join(os.getcwd(), 'cookies.txt')

        # Verifique se o arquivo cookies.txt existe
        if not os.path.exists(cookies_file):
            return "Erro: arquivo cookies.txt não encontrado.", 400

        # Configuração para o yt-dlp com cookies
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'cookies': cookies_file,  # Usando o arquivo de cookies
        }

        # Download do vídeo
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

        # Retorna o arquivo para o cliente
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Erro ao baixar o vídeo: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
