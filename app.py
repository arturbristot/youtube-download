from flask import Flask, render_template, request, send_file
from pytube import YouTube, Playlist
import os

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/processar-formulario', methods=['POST'])
def processar_formulario():
    url = request.form.get('url')
    format = request.form.get('format')
    
    def safe_filename(filename):
        return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

    if url and format:
        try:
            if 'playlist' in format.lower():  # Verifica se é pedido de playlist
                playlist = Playlist(url)
                for video in playlist.videos:
                    title = safe_filename(video.title)
                    if format.lower() == 'playlist mp3':
                        audio = video.streams.filter(only_audio=True).first()
                        audio.download(output_path='./downloads/', filename=f'{title}.mp3')
                    elif format.lower() == 'playlist mp4':
                        video_stream = video.streams.get_highest_resolution()
                        video_stream.download(output_path='./downloads/', filename=f'{title}.mp4')
            else:
                youtube = YouTube(url)
                title = safe_filename(youtube.title)
                path = f'./downloads/{title}.{format}'

                if format == 'mp3':
                    audio = youtube.streams.filter(only_audio=True).first()
                    audio.download(output_path='./downloads/', filename=f'{title}.mp3')
                elif format == 'mp4':
                    video = youtube.streams.get_highest_resolution()
                    video.download(output_path='./downloads/', filename=f'{title}.mp4')
                
                if os.path.exists(path):
                    return send_file(path, as_attachment=True, download_name=f'{title}.{format}')
                else:
                    return f"Erro ao baixar o arquivo em formato {format}."
        except Exception as e:
            return f"Ocorreu um erro: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
