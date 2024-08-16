import cv2
import time
import os

def capturar_imagenes(duracion=30):
    cap = cv2.VideoCapture(0)
    imagenes = []
    inicio = time.time()
    
    # Crear carpeta de capturas si no existe
    carpeta_capturas = os.path.join(os.getcwd(), 'capturas')
    if not os.path.exists(carpeta_capturas):
        os.makedirs(carpeta_capturas)
    
    contador = 0
    while time.time() - inicio < duracion:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Captura', frame)
            nombre_archivo = f'captura_{contador:04d}.jpg'
            ruta_archivo = os.path.join(carpeta_capturas, nombre_archivo)
            cv2.imwrite(ruta_archivo, frame)
            imagenes.append(ruta_archivo)
            contador += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return imagenes
