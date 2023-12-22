function startListening() {
    annyang.start({
        autoRestart: false,
        continuous: false
    });

    // Use the Web Speech API to record audio
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;

    recognition.onresult = function (event) {
        var audioBlob = event.results[0][0].blob;
        sendAudioToServer(audioBlob);
    };

    recognition.start();
}

function sendAudioToServer(audioBlob) {
    var formData = new FormData();
    formData.append('audio', audioBlob);

    fetch('/speech', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var recognizedText = data.text;
        // Handle the recognized text as needed (e.g., send to chatbot, update UI, etc.)
        console.log('Recognized Text:', recognizedText);
    })
    .catch(error => {
        console.error('Error processing speech:', error);
    });
}
