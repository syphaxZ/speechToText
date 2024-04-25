let mediaRecorder;
let audioChunks = [];

document.addEventListener('DOMContentLoaded', () => {
    const recordButton = document.getElementById('record');
    const audioElement = document.querySelector('audio');

    recordButton.addEventListener('click', () => {
        if (!mediaRecorder || mediaRecorder.state === 'inactive') {
            navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks);
                    const audioUrl = URL.createObjectURL(audioBlob);
                    audioElement.src = audioUrl;
                    audioElement.play();
                    audioChunks = [];
                };
                mediaRecorder.start();
                recordButton.innerText = 'Arrêter';
            })
            .catch(e => {
                console.error('Erreur:', e);
            });
        } else if (mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            recordButton.innerText = 'Enregistrer';
        }
    });
});

document.getElementById('upload').addEventListener('click', function() {
    var formData = new FormData();
    // Supposons que vous avez un input de type file pour uploader le fichier audio
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    formData.append('file', file);

    fetch('/transcribe', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            console.error('Erreur de transcription:', data.error);
        } else {
            console.log('Transcription réussie:', data.transcription);
            document.getElementById('result').textContent = data.transcription;  // Afficher le résultat
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
});

document.querySelectorAll('.delete').forEach(button => {
    button.addEventListener('click', () => {
        const transcriptionDiv = button.previousElementSibling; // Sélectionner le div précédent le bouton
        transcriptionDiv.textContent = ''; // Vider le contenu du div
    });
});

document.querySelectorAll('.delete').forEach(button => {
    button.addEventListener('click', () => {
        const targetId = button.getAttribute('data-target');
        const targetDiv = document.getElementById(targetId); // Use the ID from the data-target attribute
        targetDiv.textContent = ''; // Clear the content of the targeted div
    });
});

// ... previous code for mediaRecorder setup

mediaRecorder.onstop = () => {
    audioBlob = new Blob(audioChunks, {type: 'audio/wav'});
    const audioUrl = URL.createObjectURL(audioBlob);
    audioElement.src = audioUrl;
    audioElement.play();
    audioChunks = [];

    // Prepare the FormData with the audio blob
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');

    // Send the FormData to the Flask server
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            console.error('Erreur lors du chargement:', data.error);
        } else {
            console.log('Chargement réussi:', data.message);
            // Now you can call the transcription model if you want to do it immediately
            fetchTranscription(data.filename);
        }
    })
    .catch(error => {
        console.error('Erreur lors du chargement:', error);
    });
};

// Function to fetch transcription from server
function fetchTranscription(filename) {
    fetch('/transcribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: filename })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Erreur de transcription:', data.error);
        } else {
            document.getElementById('transcription-result').textContent = data.transcription; // Afficher le résultat de la transcription
        }
    })
    .catch(error => {
        console.error('Erreur de transcription:', error);
    });
}
