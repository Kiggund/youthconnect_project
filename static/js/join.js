// ========== 1. Password Toggle ==========
document.querySelectorAll('.toggle-password').forEach(button => {
  button.addEventListener('click', function () {
    const input = this.previousElementSibling;
    const type = input.type === 'password' ? 'text' : 'password';
    input.type = type;
    this.querySelector('i').classList.toggle('fa-eye-slash');
  });
});

// ========== 2. Signature Pad ==========
const signatureCanvas = document.getElementById('signatureCanvas');
const signatureCtx = signatureCanvas.getContext('2d');
let isDrawing = false;
let lastX = 0;
let lastY = 0;

signatureCanvas.width = signatureCanvas.offsetWidth;
signatureCanvas.height = signatureCanvas.offsetHeight;

signatureCanvas.addEventListener('mousedown', startDrawing);
signatureCanvas.addEventListener('mousemove', draw);
signatureCanvas.addEventListener('mouseup', stopDrawing);
signatureCanvas.addEventListener('mouseout', stopDrawing);
signatureCanvas.addEventListener('touchstart', startDrawing);
signatureCanvas.addEventListener('touchmove', draw);
signatureCanvas.addEventListener('touchend', stopDrawing);

function getPosition(e) {
  const rect = signatureCanvas.getBoundingClientRect();
  return {
    x: (e.clientX || e.touches[0].clientX) - rect.left,
    y: (e.clientY || e.touches[0].clientY) - rect.top
  };
}

function startDrawing(e) {
  e.preventDefault();
  isDrawing = true;
  const pos = getPosition(e);
  [lastX, lastY] = [pos.x, pos.y];
}

function draw(e) {
  if (!isDrawing) return;
  e.preventDefault();
  const pos = getPosition(e);
  signatureCtx.beginPath();
  signatureCtx.moveTo(lastX, lastY);
  signatureCtx.lineTo(pos.x, pos.y);
  signatureCtx.strokeStyle = '#000';
  signatureCtx.lineWidth = 2;
  signatureCtx.stroke();
  [lastX, lastY] = [pos.x, pos.y];

  document.getElementById('signature').value = signatureCanvas.toDataURL();
}

function stopDrawing() {
  isDrawing = false;
}

document.querySelector('.clear-signature')?.addEventListener('click', () => {
  signatureCtx.clearRect(0, 0, signatureCanvas.width, signatureCanvas.height);
  document.getElementById('signature').value = '';
});

// ========== 3. TensorFlow.js Smart ID Capture ==========
document.addEventListener('DOMContentLoaded', async () => {
  const model = await cocoSsd.load();

  const setups = [
    {
      video: document.getElementById('video_user'),
      canvas: document.getElementById('canvas_user'),
      overlay: document.getElementById('overlay_user'),
      captureBtn: document.getElementById('captureBtn_user'),
      imageInput: document.getElementById('imageInput_user')
    },
    {
      video: document.getElementById('video_kin'),
      canvas: document.getElementById('canvas_kin'),
      overlay: document.getElementById('overlay_kin'),
      captureBtn: document.getElementById('captureBtn_kin'),
      imageInput: document.getElementById('imageInput_kin')
    }
  ];

  setups.forEach(async ({ video, canvas, overlay, captureBtn, imageInput }) => {
    if (!video || !canvas || !captureBtn || !imageInput) return;

    const ctx = canvas.getContext('2d');
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    setInterval(async () => {
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const predictions = await model.detect(canvas);
      const found = predictions.some(p =>
        ['book', 'cell phone', 'tv'].includes(p.class) && p.score > 0.6
      );
      captureBtn.disabled = !found;
      if (overlay) overlay.style.borderColor = found ? 'limegreen' : 'orangered';
    }, 1000);

    captureBtn.addEventListener('click', () => {
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataURL = canvas.toDataURL('image/jpeg');
      imageInput.value = dataURL;
      alert('ID captured! You can now submit the form.');
    });
  });
});



window.addEventListener('DOMContentLoaded', () => {
  ['id_front', 'id_back'].forEach(field => {
    const dataURL = sessionStorage.getItem(`${field}_img`);
    if (dataURL) {
      fetch(dataURL)
        .then(res => res.blob())
        .then(blob => {
          const file = new File([blob], `${field}.jpg`, { type: 'image/jpeg' });
          const dt = new DataTransfer();
          dt.items.add(file);
          document.getElementById(field).files = dt.files;
          const preview = document.getElementById(`preview_${field}`);
          if (preview) {
            preview.src = dataURL;
            preview.style.display = 'block';
          }
        });
    }
  });
});
