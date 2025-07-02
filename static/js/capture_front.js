const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const captureBtn = document.getElementById('captureBtn');
const overlay = document.getElementById('overlay');

async function setup() {
  const stream = await navigator.mediaDevices.getUserMedia({
  video: { facingMode: { exact: "environment" } }
});
  video.srcObject = stream;

  const model = await cocoSsd.load();
  setInterval(async () => {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const predictions = await model.detect(canvas);
    const match = predictions.some(p => ['book', 'cell phone', 'tv'].includes(p.class) && p.score > 0.6);
    captureBtn.disabled = !match;
    overlay.style.borderColor = match ? 'limegreen' : 'orangered';
  }, 1000);
}

captureBtn.addEventListener('click', () => {
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataURL = canvas.toDataURL('image/jpeg');
  sessionStorage.setItem('id_front_img', dataURL);
  window.location.href = '/join/capture_id_back/';
});

window.addEventListener('load', () => {
  canvas.width = 480;
  canvas.height = 360;
  setup();
});
