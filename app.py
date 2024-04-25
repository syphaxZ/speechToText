from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import whisper 

model = whisper.load_model("medium")
print("modele uploded!")
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
        return jsonify({'error': 'No file found'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'])
        
        # Ensure the upload directory exists
        os.makedirs(upload_path, exist_ok=True)
        
        filepath = os.path.join(upload_path, filename)
        
        try:
            file.save(filepath)
        except Exception as e:
            app.logger.error(f'Failed to save file: {e}')
            return jsonify({'error': 'Failed to save file'}), 500
        
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Unsupported file format'}), 400
    
"""
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Vérifier si le fichier est présent dans la requête
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # Si l'utilisateur ne sélectionne pas de fichier, le navigateur
    # soumettra également un champ input vide sans nom de fichier
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Vous pouvez maintenant utiliser ce fichier directement pour le traitement
        # Ici nous lisons simplement le fichier audio
        # Assurez-vous que votre serveur accepte et peut traiter le format de fichier spécifique
        data, samplerate = sf.read(file.stream)
        # Ici, vous appelleriez votre fonction de transcription
        # result = model.transcribe(data, samplerate)

        # Réponse fictive pour l'exemple
        return jsonify({"status": "succès", "data": "transcription here"}), 200
"""
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    data = request.get_json()
    filename = data['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(filepath)
    transcription  = model.transcribe(filepath)  
    result = transcription["text"]
    print(result)
    return jsonify({'transcription': result})

if __name__ == '__main__':
    app.run(debug=True)
