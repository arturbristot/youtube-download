from flask import Flask, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/processar-formulario', methods=['POST'])

def download_file():
    # Substitua 'caminho/para/seu/arquivo/arquivo.zip' pelo caminho do seu arquivo
    path = './downloads/bristotlindo.mp3'
    # Substitua 'arquivo_para_download.zip' pelo nome que você deseja que o arquivo tenha ao ser baixado
    filename = 'musica.mp3'
    return send_file(path, as_attachment=True, download_name=filename)


def processar_formulario():
    url = request.form.get('url')
    if url:  # Verifica se a URL não é None ou vazia
        youtube = YouTube(url)
        audio = youtube.streams.filter(only_audio=True).first()
        audio.download('./downloads/', filename='bristotlindo.mp3')
        download_file()
    return render_template('index.html', url=url)

if __name__ == '__main__':
    app.run(debug=True)