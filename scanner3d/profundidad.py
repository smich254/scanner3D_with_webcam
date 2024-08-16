import cv2

def estimar_profundidad(rutas_imagenes):
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    profundidades = []
    for i in range(len(rutas_imagenes) - 1):
        img1 = cv2.imread(rutas_imagenes[i])
        img2 = cv2.imread(rutas_imagenes[i+1])
        gris1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gris2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        disparity = stereo.compute(gris1, gris2)
        profundidades.append(disparity)
    return profundidades