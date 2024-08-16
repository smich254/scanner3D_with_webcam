import cv2

def procesar_imagenes(rutas_imagenes):
    imagenes_procesadas = []
    for ruta in rutas_imagenes:
        img = cv2.imread(ruta)
        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        filtrada = cv2.GaussianBlur(gris, (5, 5), 0)
        bordes = cv2.Canny(filtrada, 100, 200)
        imagenes_procesadas.append(bordes)
    return imagenes_procesadas