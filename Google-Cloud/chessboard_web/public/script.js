// Configuración de imágenes para las piezas (notación FEN)
const imagenesPiezas = {
  'K': 'img/rey-blanco.png',
  'Q': 'img/reina-blanca.png',
  'R': 'img/torre-blanca.png',
  'B': 'img/alfil-blanco.png',
  'N': 'img/caballo-blanco.png',
  'P': 'img/peon-blanco.png',
  'k': 'img/rey-negro.png',
  'q': 'img/reina-negra.png',
  'r': 'img/torre-negra.png',
  'b': 'img/alfil-negro.png',
  'n': 'img/caballo-negro.png',
  'p': 'img/peon-negro.png'
};

const POSICION_INICIAL = [
  ['r','n','b','q','k','b','n','r'],
  ['p','p','p','p','p','p','p','p'],
  ['.','.','.','.','.','.','.','.'],
  ['.','.','.','.','.','.','.','.'],
  ['.','.','.','.','.','.','.','.'],
  ['.','.','.','.','.','.','.','.'],
  ['P','P','P','P','P','P','P','P'],
  ['R','N','B','Q','K','B','N','R']
];

let estadoActual = POSICION_INICIAL.map(row => row.slice());
let modoJuego = "jugador"; // Puede ser: "jugador", "stockfish", "vsIA"
let seleccionOrigen = null;


// DOM
const tablero = document.getElementById('chessboard');
const btnSubir = document.getElementById('btn-subir');
const btnReiniciar = document.getElementById('btn-reiniciar');
const inputImagen = document.getElementById('input-imagen');
const mensajes = document.getElementById('mensajes');
const mejorMovimientoDiv = document.getElementById('mejor-movimiento');
const btnIniciarCamara = document.getElementById('btn-iniciar-camara');
const btnCapturarFoto = document.getElementById('btn-capturar-foto');
const camaraContainer = document.getElementById('camara-container');
const videoCamara = document.getElementById('video-camara');
const canvasCaptura = document.getElementById('canvas-captura');
const fotoCapturada = document.getElementById('foto-capturada');
const btnModoGrabar = document.getElementById('btn-modo-grabar');
const btnModoJuego = document.getElementById('btn-modo-juego');
let grabando = false;
let intervaloGrabacion = null;
let ultimoTableroDigitalizado = null;
let stream = null;

// Mostrar animación de carga
function mostrarCarga() {
  document.getElementById("overlay-carga").style.display = "flex";
}

// Ocultar animación de carga
function ocultarCarga() {
  document.getElementById("overlay-carga").style.display = "none";
}

// Utilidades
function mostrarMensaje(texto, esError = false) {
  mensajes.textContent = texto;
  mensajes.className = esError ? 'error' : '';
  setTimeout(() => mensajes.textContent = '', 5000);
}

// Transforma tablero a FEN para validar movimientos
function convertirEstadoAFEN(tablero, turnoBlancas) {
  const filas = tablero.map(fila => {
    let result = "";
    let vacias = 0;
    for (const p of fila) {
      if (p === ".") {
        vacias++;
      } else {
        if (vacias > 0) {
          result += vacias;
          vacias = 0;
        }
        result += p;
      }
    }
    if (vacias > 0) result += vacias;
    return result;
  });

  const fen = filas.join("/") + ` ${turnoBlancas ? "w" : "b"} - - 0 1`;
  return fen;
}


// Convierte notación tipo "e2" a índice 0-63
function algebraicAIndice(casilla) {
  const files = "abcdefgh";
  const col = files.indexOf(casilla[0]);
  const row = 8 - parseInt(casilla[1]);
  return row * 8 + col;
}

// Convierte índice 0-63 a notación tipo "e2"
function indiceAAlgebraica(fila, col) {
  const files = "abcdefgh";
  return files[col] + (8 - fila);
}

function mostrarFinPartida(texto) {
  const finPartida = document.getElementById("fin-partida");
  const finTexto = document.getElementById("fin-texto");
  finTexto.textContent = texto;
  finPartida.style.display = "flex";
}

function reiniciarPartidaDesdeFinal() {
  document.getElementById("fin-partida").style.display = "none";
  estadoActual = POSICION_INICIAL.map(row => row.slice());
  renderizarTablero();
  mejorMovimientoDiv.style.display = "none";
  mostrarMensaje("Tablero reiniciado a posición inicial");
  ultimoTableroDigitalizado = null;
}

// Pinta de verde las casillas de origen y destino
function pintarCasillasVerdes(origen, destino) {
  document.querySelectorAll('.square').forEach(sq => sq.classList.remove('verde'));
  [origen, destino].forEach(idx => {
    const sq = document.querySelector(`#chessboard .square[data-idx="${idx}"]`);
    if (sq) sq.classList.add('verde');
  });
}

// Muestra el mejor movimiento y la barra de evaluación vertical
function mostrarMejorMovimiento(movimiento, evaluacion) {
  mejorMovimientoDiv.style.display = "flex";
  document.getElementById('movimiento-texto').textContent = movimiento || '--';

  // Barra de evaluación vertical
  let evalNum = parseFloat(evaluacion.replace(',', '.'));
  if (isNaN(evalNum)) evalNum = 0;
  document.getElementById('eval-numero-vert').textContent = evalNum > 0 ? `+${evalNum}` : evalNum;

  // +6 o más = 100% blancas, -6 o menos = 100% negras
  let propBlancas = Math.max(0, Math.min(1, 0.5 + evalNum / 12));
  document.getElementById('barra-eval-negras-vert').style.height = `${propBlancas * 100}%`;
  document.getElementById('barra-eval-blancas-vert').style.height = `${(1 - propBlancas) * 100}%`;
}

// Renderiza el tablero y marca las casillas verdes si existen
function renderizarTablero(casillasVerdes=[]) {
  tablero.innerHTML = '';
  for (let fila = 0; fila < 8; fila++) {
    for (let columna = 0; columna < 8; columna++) {
      const pieza = estadoActual[fila][columna];
      const casilla = document.createElement('div');
      casilla.classList.add('square');
      casilla.classList.add((fila + columna) % 2 === 0 ? 'white' : 'black');
      casilla.setAttribute('data-idx', fila * 8 + columna);
      if (casillasVerdes.includes(fila * 8 + columna)) casilla.classList.add('verde');
      if (pieza !== '.') {
        const img = document.createElement('img');
        img.src = imagenesPiezas[pieza];
        img.alt = pieza;
        img.classList.add('pieza-ajedrez');
        casilla.appendChild(img);
      }
      tablero.appendChild(casilla);
      casilla.addEventListener('click', () => {
        if (modoJuego === "stockfish") return;

        const fila = Math.floor(casilla.dataset.idx / 8);
        const col = casilla.dataset.idx % 8;
        const pieza = estadoActual[fila][col];

        if (!seleccionOrigen) {
          if (pieza === '.') {
            mostrarMensaje("Selecciona una pieza válida", true);
            return;
          }
          const esBlanca = pieza === pieza.toUpperCase();
          const turnoBlancas = modoJuego === "vsIA";
          if ((turnoBlancas && !esBlanca) || (!turnoBlancas && esBlanca)) {
            mostrarMensaje("No puedes mover las piezas del oponente", true);
            return;
          }
          seleccionOrigen = { fila, col };
          renderizarTablero([fila * 8 + col]); // pinta origen en verde
        } else {
          const origen = seleccionOrigen;
          const destino = { fila, col };

          const turnoBlancas = modoJuego === "vsIA"; // Jugador mueve blancas si juega contra IA, negras si es persona vs persona
          const fen = convertirEstadoAFEN(estadoActual, turnoBlancas);
          const game = new Chess(fen);
          const moveUCI = indiceAAlgebraica(origen.fila, origen.col) + indiceAAlgebraica(destino.fila, destino.col);
          const legalMoves = game.moves({ verbose: true });

          const movimientoValido = legalMoves.some(m => m.from === moveUCI.slice(0,2) && m.to === moveUCI.slice(2,4));

          if (!movimientoValido) {
            mostrarMensaje("Movimiento ilegal", true);
            seleccionOrigen = null;
            renderizarTablero();
            return;
          }

          console.log(`[DEBUG] Movimiento seleccionado: ${moveUCI}`);
          mostrarMensaje(`Movimiento: ${moveUCI}`);

          if (modoJuego === "jugador") {
            // TODO: enviar a backend
            enviarMovimientoAlRobot(moveUCI);
          }
          
          // Actualizar estado del tablero
          estadoActual[destino.fila][destino.col] = estadoActual[origen.fila][origen.col];
          estadoActual[origen.fila][origen.col] = '.';

          // Reset
          seleccionOrigen = null;
          renderizarTablero();

          if (modoJuego === "vsIA") {
            setTimeout(() => {
              analizarYMarcarMejorJugada(estadoActual.map(row => row.slice()), true);
            }, 500); // pequeña pausa visual
          }
        }
      });
    }
  }
}

function tablerosDiferentes(t1, t2) {
  if (!t1 || !t2) {
    console.log("[DEBUG] Uno de los tableros es null o undefined");
    return true;
  }
  let diferencias = [];
  for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
      if (t1[i][j] !== t2[i][j]) {
        diferencias.push({ fila: i, col: j, antes: t2[i][j], ahora: t1[i][j] });
      }
    }
  }
  if (diferencias.length > 0) {
    console.log("[DEBUG] Diferencias detectadas entre tableros:", diferencias);
    return true;
  }
  return false;
}

function mostrarSenalDeMovimiento() {
  mensajes.textContent = "¡Movimiento detectado!";
  mensajes.style.color = "#e67e22";
  setTimeout(() => mensajes.textContent = '', 3000);
  console.log("[DEBUG] Señal de movimiento mostrada");
}

// Procesar respuesta de la API de predicción y llamar a Stockfish
async function procesarRespuestaAPI(datosApi) {
  try {
    console.log("[DEBUG] Respuesta recibida de la API de predicción:", datosApi);

    if (!datosApi.board) throw new Error("Respuesta sin tablero");

    // Compara con el último tablero digitalizado
    if (tablerosDiferentes(datosApi.board, ultimoTableroDigitalizado)) {
      mostrarSenalDeMovimiento();
    } else {
      console.log("[DEBUG] No hay diferencias entre tableros");
    }
    // Actualiza el último tablero digitalizado
    ultimoTableroDigitalizado = datosApi.board.map(row => row.slice());

    estadoActual = datosApi.board;
    console.log("[DEBUG] Tablero digitalizado actualizado:", estadoActual);

    renderizarTablero();
    if (modoJuego == "stockfish") {
      await analizarYMarcarMejorJugada(datosApi.board);
    }
    mostrarMensaje(`Tablero actualizado`);
  } catch (error) {
    console.error('[DEBUG] Error procesando respuesta:', error);
    mostrarMensaje("Error procesando la respuesta de la API", true);
  }
}

// Llama a Stockfish y pinta todo al cargar el tablero
async function analizarYMarcarMejorJugada(board) {
  const tableroStockfish = board.map(fila => fila.join(' '));
  console.log("[DEBUG] Enviando a Stockfish:", tableroStockfish);
  try {
    const resp = await fetch("https://stockfish-service-38939463765.europe-west1.run.app", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tablero: tableroStockfish })
    });
    const datos = await resp.json();
    console.log("[DEBUG] Respuesta de Stockfish:", datos);

    mostrarMejorMovimiento(datos.mejor_movimiento, datos.evaluacion);

    if (datos.mejor_movimiento && datos.mejor_movimiento.length >= 4) {
      const desde = datos.mejor_movimiento.slice(0,2);
      const hasta = datos.mejor_movimiento.slice(2,4);
      const [f1, c1] = [8 - parseInt(desde[1]), "abcdefgh".indexOf(desde[0])];
      const [f2, c2] = [8 - parseInt(hasta[1]), "abcdefgh".indexOf(hasta[0])];

      if (modoJuego === "stockfish" || modoJuego === "vsIA") {
        // TODO: enviar a backend
        enviarMovimientoAlRobot(datos.mejor_movimiento);
      }

      estadoActual[f2][c2] = estadoActual[f1][c1];
      estadoActual[f1][c1] = '.';
      renderizarTablero();
      mostrarMensaje(`Stockfish ha jugado: ${datos.mejor_movimiento}`);
      pintarCasillasVerdes(algebraicAIndice(desde), algebraicAIndice(hasta));
      console.log(`[DEBUG] Flecha pintada: ${desde} -> ${hasta}`);
    }

        // Detectar jaque mate
    if (typeof datos.evaluacion === "string" && datos.evaluacion.includes("Mate en")) {
      const mateNum = parseInt(datos.evaluacion.replace(/\D/g, '')) || 1;
      if (mateNum === 1) {
        setTimeout(() => {
          mostrarFinPartida("¡Jaque mate!");
        }, 2000); // espera 1.5 segundos
        return;
      }
    }
  } catch (e) {
    console.error('[DEBUG] Error llamando a Stockfish:', e);
    mostrarMensaje('No se pudo obtener la mejor jugada', true);
  }
}

// Subir imagen y procesarla
btnSubir.addEventListener('click', async () => {
  if (!inputImagen.files || inputImagen.files.length === 0) {
    mostrarMensaje("Selecciona una imagen primero", true);
    return;
  }
  const archivo = inputImagen.files[0];
  btnSubir.disabled = true;
  mostrarCarga();
  try {
    const formData = new FormData();
    formData.append('file', archivo, 'imagen.jpg');
    console.log("[DEBUG] Enviando imagen a la API de predicción:", archivo);

    const respuesta = await fetch('https://europe-southwest1-rey-y-dama-mechanical-turk.cloudfunctions.net/predict_chessboard', {
      method: 'POST',
      body: formData
    });
    console.log("[DEBUG] Status de respuesta de la API de predicción:", respuesta.status);

    if (!respuesta.ok) throw new Error('Error en la API: ' + respuesta.statusText);
    const datos = await respuesta.json();
    await procesarRespuestaAPI(datos);
  } catch (error) {
    console.error('[DEBUG] Error en subida de imagen:', error);
    mostrarMensaje("Error: " + error.message, true);
  } finally {
    btnSubir.disabled = false;
    ocultarCarga();
  }
});

// Reiniciar tablero
btnReiniciar.addEventListener('click', () => {
  estadoActual = POSICION_INICIAL.map(row => row.slice());
  renderizarTablero();
  mejorMovimientoDiv.style.display = "none";
  mostrarMensaje("Tablero reiniciado a posición inicial");
  console.log("[DEBUG] Tablero reiniciado");
});

// ----------- CÁMARA -----------
btnIniciarCamara.addEventListener('click', async () => {
  camaraContainer.style.display = "block";
  btnCapturarFoto.style.display = "inline-block";
  btnModoGrabar.style.display = "inline-block";
  btnModoGrabar.textContent = "Modo grabar";
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoCamara.srcObject = stream;
    mostrarMensaje("Cámara iniciada");
    console.log("[DEBUG] Cámara iniciada");
  } catch (err) {
    console.error('[DEBUG] No se pudo acceder a la cámara:', err);
    mostrarMensaje("No se pudo acceder a la cámara", true);
  }
});

function capturarYEnviarFoto() {
  canvasCaptura.width = videoCamara.videoWidth;
  canvasCaptura.height = videoCamara.videoHeight;
  canvasCaptura.getContext('2d').drawImage(videoCamara, 0, 0, canvasCaptura.width, canvasCaptura.height);
  canvasCaptura.toBlob(async (blob) => {
    fotoCapturada.src = URL.createObjectURL(blob);
    fotoCapturada.style.display = "block";
    console.log("[DEBUG] Imagen capturada de la cámara, enviando a API...");
    mostrarCarga();
    try {
      const formData = new FormData();
      formData.append('file', blob, 'captura.jpg');
      const respuesta = await fetch('https://europe-southwest1-rey-y-dama-mechanical-turk.cloudfunctions.net/predict_chessboard', {
        method: 'POST',
        body: formData
      });
      console.log("[DEBUG] Status de respuesta de la API de predicción (cámara):", respuesta.status);
      if (!respuesta.ok) throw new Error('Error en la API: ' + respuesta.statusText);
      const datos = await respuesta.json();
      await procesarRespuestaAPI(datos);
    } catch (error) {
      console.error('[DEBUG] Error enviando imagen de cámara:', error);
      mostrarMensaje("Error: " + error.message, true);
    } finally {
      ocultarCarga();
    }
  }, 'image/jpeg', 0.9);
}

btnCapturarFoto.addEventListener('click', () => {
  capturarYEnviarFoto();
  console.log("[DEBUG] Botón capturar foto pulsado");
});

btnModoGrabar.addEventListener('click', () => {
  if (!grabando) {
    grabando = true;
    btnModoGrabar.textContent = "Detener grabación";
    capturarYEnviarFoto(); // Captura una inmediatamente
    intervaloGrabacion = setInterval(capturarYEnviarFoto, 10000); // cada 10 segundos
    mostrarMensaje("Modo grabar activado: capturando cada 10 segundos");
    console.log("[DEBUG] Modo grabar activado");
  } else {
    grabando = false;
    btnModoGrabar.textContent = "Modo grabar";
    clearInterval(intervaloGrabacion);
    mostrarMensaje("Modo grabar detenido");
    console.log("[DEBUG] Modo grabar detenido");
  }
});

btnModoJuego.addEventListener('click', () => {
  if (modoJuego === "jugador") modoJuego = "stockfish";
  else if (modoJuego === "stockfish") modoJuego = "vsIA";
  else modoJuego = "jugador";

  btnModoJuego.textContent = `Modo: ${modoJuego === "jugador" ? "Jugador" : (modoJuego === "stockfish" ? "Stockfish" : "Jugador vs IA")}`;
  mostrarMensaje(`Modo cambiado a: ${btnModoJuego.textContent.split(': ')[1]}`);
  console.log(`[DEBUG] Modo de juego: ${modoJuego}`);
});


async function enviarMovimientoAlRobot(uci) {
  try {
    const response = await fetch("http://localhost:5000/mover", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        movimiento: uci,
        estado_tablero: estadoActual
      })
    });

    const datos = await response.json();
    console.log("[DEBUG] Respuesta del robot:", datos);
    mostrarMensaje("Movimiento enviado al robot");
  } catch (error) {
    console.error("[DEBUG] Error al comunicar con el robot:", error);
    mostrarMensaje("Error de comunicación con el robot simulado", true);
  }
}

// Inicialización
renderizarTablero();
console.log("[DEBUG] Página inicializada");