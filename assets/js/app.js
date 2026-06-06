/**
 * Lógica principal da aplicação Media Downloader.
 */
const btnFetch = document.getElementById('btnFetch');
const inputUrl = document.getElementById('kwaiUrl');
const customFilename = document.getElementById('customFilename');
const preview = document.getElementById('preview');
const loading = document.getElementById('loading');
const overlay = document.getElementById('overlay');
const overlayText = document.getElementById('overlayText');
const modal = document.getElementById('modal');
const btnMp3 = document.getElementById('btnMp3');
const btnMp4 = document.getElementById('btnMp4');
const videoFile = document.getElementById('videoFile');
const btnConvert = document.getElementById('btnConvert');
const convertStatus = document.getElementById('convertStatus');

let lastProcessedUrl = '';
let lastProcessedTitle = 'kwai_video';

function showOverlay(text) {
  overlayText.innerText = text;
  overlay.style.display = 'flex';
}

function hideOverlay() {
  overlay.style.display = 'none';
}

function showModal() {
  modal.style.display = 'flex';
}

function hideModal() {
  modal.style.display = 'none';
}

async function downloadBlob(endpoint, url, filename, extension, overlayMsg) {
  showOverlay(overlayMsg);
  try {
    const encodedUrl = encodeURIComponent(url);
    const encodedFilename = encodeURIComponent(filename);
    const response = await fetch(
      `${endpoint}?url=${encodedUrl}&filename=${encodedFilename}`
    );

    if (!response.ok)
      throw new Error(`Erro ao baixar ${extension.toUpperCase()}.`);

    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');

    a.href = downloadUrl;
    a.download = `${filename}.${extension}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(downloadUrl);

    showModal();
  } catch (e) {
    alert(`Erro no download: ${e.message}`);
  } finally {
    hideOverlay();
  }
}

btnFetch.onclick = async () => {
  const rawText = inputUrl.value.trim();
  if (!rawText) return alert('Cole uma URL ou texto com link!');

  showOverlay('Analisando vídeo...');
  preview.style.display = 'none';
  btnFetch.disabled = true;

  try {
    const formData = new FormData();
    formData.append('url', rawText);

    const response = await fetch('/api/info', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();

    if (data.success) {
      document.getElementById('videoThumb').src = data.thumbnail;
      document.getElementById('videoTitle').innerText = data.title;
      customFilename.value = data.title;
      lastProcessedUrl = data.source;
      lastProcessedTitle = data.clean_title;
      preview.style.display = 'block';
    } else {
      alert('Erro: ' + data.error);
    }
  } catch (e) {
    alert('Erro na conexão com o servidor.');
  } finally {
    hideOverlay();
    btnFetch.disabled = false;
  }
};

btnMp4.onclick = () => {
  const filename = customFilename.value.trim() || lastProcessedTitle;
  downloadBlob(
    '/api/download/mp4',
    lastProcessedUrl,
    filename,
    'mp4',
    'Preparando vídeo...'
  );
};

btnMp3.onclick = () => {
  const filename = customFilename.value.trim() || lastProcessedTitle;
  downloadBlob(
    '/api/download/mp3',
    lastProcessedUrl,
    filename,
    'mp3',
    'Convertendo áudio... aguarde.'
  );
};

// Move cursor ao final do campo após clique/focus
customFilename.addEventListener('focus', function () {
  setTimeout(() => {
    const len = this.value.length;
    this.setSelectionRange(len, len);
  }, 0);
});

// === LÓGICA DO CONVERSOR ===
btnConvert.onclick = async () => {
  const file = videoFile.files[0];
  if (!file) {
    alert('Selecione um arquivo de vídeo!');
    return;
  }

  const allowedExts = ['.mp4', '.ts', '.mkv', '.avi', '.mov', '.webm'];
  const fileExt = '.' + file.name.split('.').pop().toLowerCase();
  const maxSize = 200 * 1024 * 1024; // 200MB

  if (!allowedExts.includes(fileExt)) {
    alert('Formato não suportado. Use: ' + allowedExts.join(', '));
    return;
  }

  if (file.size > maxSize) {
    alert('Arquivo muito grande. Limite: 200MB');
    return;
  }

  const outputName = file.name.replace(/\.[^/.]+$/, '') + '_convertido.mp3';

  showOverlay('Enviando e convertendo...');
  btnConvert.disabled = true;
  convertStatus.style.display = 'block';
  convertStatus.innerText = 'Processando...';

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/convert', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) throw new Error("Falha na conversão.");

    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = outputName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(downloadUrl);

    convertStatus.innerText = 'Download iniciado!';
    showModal();
    setTimeout(() => {
      convertStatus.style.display = 'none';
      convertStatus.innerText = '';
      videoFile.value = '';
    }, 3000);
  } catch (e) {
    alert('Erro na conexão: ' + e.message);
    convertStatus.style.display = 'none';
  } finally {
    hideOverlay();
    btnConvert.disabled = false;
  }
};
