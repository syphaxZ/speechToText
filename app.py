from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder='templates')

# Dossier pour stocker les fichiers audio
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fonction pour vérifier l'extension du fichier
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    print("Index route is being called")
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier trouvé'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': 'Fichier téléchargé avec succès', 'filename': filename})
    else:
        return jsonify({'error': 'Format de fichier non pris en charge'})

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    data = request.get_json()
    filename = data['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Here you should call your transcription model, e.g.,
    transcription = your_transcription_function(filepath)  # Replace with your model call
    
    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    app.run(debug=True)
