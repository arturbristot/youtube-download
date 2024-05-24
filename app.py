from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/processar-formulario', methods=['POST'])
def processar_formulario():
    url = request.form.get('url')
    format = request.form.get('format')
    
    if url and format:
        youtube = YouTube(url)
        title = youtube.title
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
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
