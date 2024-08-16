# Escáner 3D

Este proyecto implementa un escáner 3D utilizando Python y varias bibliotecas de procesamiento de imágenes y modelado 3D.

## Requisitos

- Python 3.10.5
- Las bibliotecas listadas en `requirements.txt`
- Requiere la creación de un entorno virtual para instalar las dependencias de Python.

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. Crea un entorno virtual:
   ```
   python -m venv venv
   ```

3. Activa el entorno virtual:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS y Linux:
     ```
     source venv/bin/activate
     ```

4. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el programa principal:
   ```
   python main.py
   ```

2. Sigue las instrucciones en la interfaz gráfica para:
   - Ajustar el tiempo de escaneo (entre 10 y 60 segundos)
   - Iniciar la captura de imágenes
   - Procesar las imágenes y crear un modelo 3D
   - Visualizar el modelo 3D generado
   - Limpiar la carpeta de capturas si es necesario

## Estructura del Proyecto

- `main.py`: Punto de entrada del programa.
- `gui.py`: Implementación de la interfaz gráfica.
- `scanner3d/`: Módulo principal del escáner 3D.
  - `captura.py`: Funciones para capturar imágenes.
  - `procesamiento.py`: Funciones para procesar imágenes.
  - `profundidad.py`: Funciones para estimar la profundidad.
  - `modelado.py`: Funciones para crear y visualizar modelos 3D.
- `capturas/`: Directorio donde se guardan las imágenes capturadas.
- `modelos/`: Directorio donde se guardan los modelos 3D generados.

## Características

- Captura de imágenes con tiempo ajustable
- Procesamiento de imágenes y estimación de profundidad
- Creación de modelos 3D a partir de las imágenes procesadas
- Visualización de modelos 3D con colores personalizados (azul para la cara superior, gris para el resto)
- Interfaz gráfica intuitiva para controlar todo el proceso

## Notas

- Asegúrate de tener una cámara conectada y funcionando correctamente antes de iniciar la captura.
- La calidad del modelo 3D puede variar dependiendo de las condiciones de iluminación y la complejidad del objeto escaneado.
- Para mejores resultados, realiza el escaneo en un ambiente bien iluminado y con el objeto colocado sobre una superficie plana.