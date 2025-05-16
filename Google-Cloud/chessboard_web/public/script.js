// Nuevo mapeo: minúsculas = blancas, mayúsculas = negras
const imagenesPiezas = {
  'r': 'img/torre-blanca.png',
  'n': 'img/caballo-blanco.png',
  'b': 'img/alfil-blanco.png',
  'q': 'img/reina-blanca.png',
  'k': 'img/rey-blanco.png',
  'p': 'img/peon-blanco.png',
  'R': 'img/torre-negra.png',
  'N': 'img/caballo-negro.png',
  'B': 'img/alfil-negro.png',
  'Q': 'img/reina-negra.png',
  'K': 'img/rey-negro.png',
  'P': 'img/peon-negro.png'
};

const tablero = document.getElementById('chessboard');
const btnSubir = document.getElementById('btn-subir');
const inputImagen = document.getElementById('input-imagen');
const mensajes = document.getElementById('mensajes');

// Debug
const debugContainer = document.createElement('div');
debugContainer.style.position = 'fixed';
debugContainer.style.bottom = '10px';
debugContainer.style.left = '10px';
debugContainer.style.backgroundColor = 'white';
debugContainer.style.padding = '10px';
debugContainer.style.border = '1px solid #ccc';
debugContainer.style.maxHeight = '300px';
debugContainer.style.overflow = 'auto';
debugContainer.style.zIndex = '1000';
document.body.appendChild(debugContainer);

function logDebug(message, data = null) {
  const debugEntry = document.createElement('div');
  debugEntry.style.marginBottom = '5px';
  debugEntry.style.fontFamily = 'monospace';
  
  const timestamp = new Date().toLocaleTimeString();
  debugEntry.innerHTML = `<strong>[${timestamp}]</strong> ${message}`;
  
  if (data) {
    const pre = document.createElement('pre');
    pre.style.whiteSpace = 'pre-wrap';
    pre.textContent = JSON.stringify(data, null, 2);
    debugEntry.appendChild(pre);
  }
  
  debugContainer.appendChild(debugEntry);
  debugContainer.scrollTop = debugContainer.scrollHeight;
}

// Validar que todas las piezas del tablero sean válidas
function validarTablero(matriz) {
  for (let fila = 0; fila < matriz.length; fila++) {
    for (let columna = 0; columna < matriz[fila].length; columna++) {
      const pieza = matriz[fila][columna];
      if (pieza !== '.' && !imagenesPiezas[pieza]) {
        logDebug(`Elemento con posición inválida o sin pieza en fila ${fila}, columna ${columna}`, pieza);
      }
    }
  }
}

// Renderizar tablero completo
function renderizarTablero(matriz) {
  logDebug("Iniciando renderizado del tablero", matriz);
  tablero.innerHTML = '';
  for (let fila = 0; fila < 8; fila++) {
    for (let columna = 0; columna < 8; columna++) {
      const pieza = matriz[fila][columna];
      const casilla = document.createElement('div');
      casilla.classList.add('square');
      casilla.classList.add((fila + columna) % 2 === 0 ? 'white' : 'black');
      if (pieza !== '.') {
        const img = document.createElement('img');
        img.src = imagenesPiezas[pieza];
        img.alt = obtenerNombrePieza(pieza);
        img.classList.add('pieza-ajedrez');
        casilla.appendChild(img);
        logDebug(`Añadida pieza ${pieza} en fila ${fila}, columna ${columna}`);
      }
      tablero.appendChild(casilla);
    }
  }
}

// Obtener nombre completo de la pieza
function obtenerNombrePieza(pieza) {
  const nombres = {
    'r': 'Torre blanca', 'n': 'Caballo blanco', 'b': 'Alfil blanco',
    'q': 'Reina blanca', 'k': 'Rey blanco', 'p': 'Peón blanco',
    'R': 'Torre negra', 'N': 'Caballo negro', 'B': 'Alfil negro',
    'Q': 'Reina negra', 'K': 'Rey negro', 'P': 'Peón negro'
  };
  return nombres[pieza] || pieza;
}

// Procesar imagen y llamar a la API
btnSubir.addEventListener('click', async () => {
  if (!inputImagen.files?.length) {
    mostrarMensaje("Selecciona una imagen primero", true);
    return;
  }
  
  btnSubir.disabled = true;
  mostrarMensaje("Procesando imagen...");
  logDebug("Iniciando procesamiento de imagen");

  try {
    const formData = new FormData();
    formData.append('file', inputImagen.files[0]);

    logDebug("Realizando llamada a la API...");
    const respuesta = await fetch('https://europe-southwest1-rey-y-dama-mechanical-turk.cloudfunctions.net/predict_chessboard', {
      method: 'POST',
      body: formData
    });

    logDebug(`Respuesta recibida - Status: ${respuesta.status}`);
    
    if (!respuesta.ok) {
      const errorText = await respuesta.text();
      throw new Error(`Error ${respuesta.status}: ${errorText}`);
    }

    const datos = await respuesta.json();
    logDebug("Datos recibidos de la API", datos);

    const board = datos.board; // <-- aquí accedes a la matriz real

    if (Array.isArray(board) && board.length === 8 && board.every(fila => Array.isArray(fila) && fila.length === 8)) {
      validarTablero(board);
      renderizarTablero(board);
      mostrarMensaje("Tablero generado correctamente");
    } else {
      throw new Error("Formato de tablero no reconocido");
    }

    
  } catch (error) {
    logDebug("Error en el proceso", error);
    mostrarMensaje(error.message, true);
  } finally {
    btnSubir.disabled = false;
  }
});

// Mostrar mensajes
function mostrarMensaje(texto, esError = false) {
  mensajes.textContent = texto;
  mensajes.className = esError ? 'error' : '';
  setTimeout(() => mensajes.textContent = '', 5000);
}

// Inicialización - Tablero vacío
logDebug("Inicializando aplicación");
renderizarTablero(Array(8).fill().map(() => Array(8).fill('.')));
//prueba_verion_1

const videoCamara = document.getElementById('video-camara');
const btnGrabar = document.getElementById('btn-grabar');
let mediaStream = null;
let intervaloEnvio = null;
let grabando = false;

// Inicializa la cámara al cargar
async function iniciarCamara() {
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    videoCamara.srcObject = mediaStream;
    logDebug("Cámara iniciada correctamente");
  } catch (error) {
    logDebug("Error al acceder a la cámara", error);
    alert('No se pudo acceder a la cámara: ' + error.message);
  }
}

function mostrarFotoCapturada(canvas) {
  const img = document.getElementById('foto-capturada');
  img.src = canvas.toDataURL('image/jpeg');
}

// Captura una imagen actual del video y la envía a la API
async function capturarYEnviarImagen() {
  if (!videoCamara.videoWidth || !videoCamara.videoHeight) {
    logDebug("Esperando a que la cámara esté lista para capturar imagen...");
    return;
  }

  const canvas = document.createElement('canvas');
  canvas.width = videoCamara.videoWidth;
  canvas.height = videoCamara.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(videoCamara, 0, 0, canvas.width, canvas.height);

  mostrarFotoCapturada(canvas);

  logDebug("Imagen capturada de la cámara. Enviando a la API...");

  canvas.toBlob(async (blob) => {
    const formData = new FormData();
    formData.append('file', blob, 'captura.jpg');
    try {
      logDebug("Enviando imagen a la API...");
      const respuesta = await fetch('https://europe-southwest1-rey-y-dama-mechanical-turk.cloudfunctions.net/predict_chessboard', {
        method: 'POST',
        body: formData
      });
      if (respuesta.ok) {
        const datos = await respuesta.json();
        logDebug("Respuesta recibida de la API", datos);
        if (datos.board) {
          validarTablero(datos.board);
          renderizarTablero(datos.board);
          mostrarMensaje("Tablero actualizado automáticamente");
        }
      } else {
        const errorText = await respuesta.text();
        logDebug("Error al enviar imagen a la API", errorText);
      }
    } catch (err) {
      logDebug("Error de red al enviar imagen", err);
    }
  }, 'image/jpeg');
}

// Botón para iniciar/detener el envío periódico
btnGrabar.addEventListener('click', () => {
  if (!mediaStream) return;

  if (!grabando) {
    btnGrabar.textContent = 'Detener grabación';
    grabando = true;
    logDebug("Grabación iniciada. Se enviarán imágenes cada 15 segundos.");
    capturarYEnviarImagen();
    intervaloEnvio = setInterval(capturarYEnviarImagen, 15000);
  } else {
    btnGrabar.textContent = 'Iniciar grabación';
    grabando = false;
    clearInterval(intervaloEnvio);
    logDebug("Grabación detenida. Se detiene el envío de imágenes.");
  }
});

iniciarCamara();
