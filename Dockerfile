# Imagen base con Node
FROM node:18

# Instala librerías necesarias para Electron
RUN apt-get update && apt-get install -y \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libnss3 \
    libx11-6 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Crea directorio de trabajo
WORKDIR /app

# Copia todo el proyecto
COPY ./app/ .

# Instala dependencias
RUN npm install

# Comando por defecto para ejecutar la app
CMD ["npm", "start"]
