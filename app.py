from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import whisper 

model = whisper.load_model("medium")
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

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    data = request.get_json()
    filename = data['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Here you should call your transcription model, e.g.,
    transcription  = model.transcribe(filepath)  # Replace with your model call
    
    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    app.run(debug=True)
