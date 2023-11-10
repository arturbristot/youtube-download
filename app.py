from flask import Flask, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/processar-formulario', methods=['POST'])

def processar_formulario():
    url = request.form.get('url')
    if url:
        youtube = YouTube(url)
        title = youtube.title
        audio = youtube.streams.filter(only_audio=True).first()
        audio.download('./downloads/', filename=f'{title}.mp3')
        path = f'./downloads/{title}.mp3'
        filename = f'{title}.mp3'
        return send_file(path, as_attachment=True, download_name=filename)
    
    return render_template('index.html', url=url)

if __name__ == '__main__':
    app.run(debug=True)
