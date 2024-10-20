// static/script.js
document.getElementById('startWebcam').addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });

        const videoElement = document.createElement('video');
        videoElement.srcObject = stream;
        videoElement.autoplay = true;

        document.body.appendChild(videoElement);

        document.getElementById('startWebcam').disabled = true;
        document.getElementById('stopWebcam').disabled = false;

        alert('Webcam started!');
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }
});

document.getElementById('stopWebcam').addEventListener('click', () => {
    const videoElement = document.querySelector('video');
    if (videoElement) {
        const tracks = videoElement.srcObject.getTracks();
        tracks.forEach(track => track.stop());
        videoElement.remove();
        document.getElementById('startWebcam').disabled = false;
        document.getElementById('stopWebcam').disabled = true;
        alert('Webcam stopped!');
    }
});
