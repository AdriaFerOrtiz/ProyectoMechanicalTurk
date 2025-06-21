FROM python:3.10-slim

# Instalar dependencias necesarias para ejecutar Stockfish
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY app.py .
COPY stockfish/ ./stockfish/

# Dar permisos de ejecución al binario de stockfish
RUN chmod +x ./stockfish/stockfish

# Definir puerto (Cloud Run usa 8080)
ENV PORT 8080

# Ejecutar la aplicación
CMD ["python", "app.py"]
