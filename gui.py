import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from scanner3d import capturar_imagenes, procesar_imagenes, estimar_profundidad, crear_modelo_3d, guardar_obj, visualizar_obj
import threading
import traceback
import os
import shutil

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Escáner 3D")
        self.geometry("500x600")
        
        self.rutas_imagenes = []
        self.imagenes_procesadas = []
        self.profundidades = []
        
        self.crear_widgets()
    
    def crear_widgets(self):
        ttk.Label(self, text="Escáner 3D", font=("Arial", 24)).pack(pady=20)
        
        # Control de tiempo de escaneo
        frame_tiempo = ttk.Frame(self)
        frame_tiempo.pack(pady=10)
        ttk.Label(frame_tiempo, text="Tiempo de escaneo (segundos):").pack(side=tk.LEFT)
        self.tiempo_escaneo = ttk.Scale(frame_tiempo, from_=10, to=60, orient=tk.HORIZONTAL, length=200)
        self.tiempo_escaneo.set(30)
        self.tiempo_escaneo.pack(side=tk.LEFT)
        self.label_tiempo = ttk.Label(frame_tiempo, text="30")
        self.label_tiempo.pack(side=tk.LEFT)
        self.tiempo_escaneo.config(command=self.actualizar_tiempo)
        
        ttk.Button(self, text="Iniciar Captura", command=self.iniciar_captura).pack(pady=10)
        
        self.boton_modelo = ttk.Button(self, text="Crear Modelo 3D", command=self.crear_modelo, state='disabled')
        self.boton_modelo.pack(pady=10)
        
        ttk.Button(self, text="Visualizar Modelo OBJ", command=self.visualizar_modelo).pack(pady=10)
        
        ttk.Button(self, text="Limpiar Carpeta de Capturas", command=self.limpiar_capturas).pack(pady=10)
        
        self.progreso = ttk.Progressbar(self, length=300, mode='determinate')
        self.progreso.pack(pady=20)
        
        self.estado = ttk.Label(self, text="")
        self.estado.pack(pady=10)
    
    def actualizar_tiempo(self, valor):
        self.label_tiempo.config(text=f"{int(float(valor))}")
    
    def iniciar_captura(self):
        tiempo = int(self.tiempo_escaneo.get())
        self.estado.config(text=f"Capturando imágenes ({tiempo} segundos)...")
        self.progreso['value'] = 0
        self.update()
        
        thread = threading.Thread(target=self.capturar_y_procesar, args=(tiempo,))
        thread.start()
    
    def capturar_y_procesar(self, tiempo):
        try:
            self.rutas_imagenes = capturar_imagenes(duracion=tiempo)
            self.progreso['value'] = 50
            self.update()
            
            self.estado.config(text="Procesando imágenes...")
            self.imagenes_procesadas = procesar_imagenes(self.rutas_imagenes)
            self.progreso['value'] = 75
            self.update()
            
            self.estado.config(text="Estimando profundidad...")
            self.profundidades = estimar_profundidad(self.rutas_imagenes)
            self.progreso['value'] = 100
            self.update()
            
            self.estado.config(text="Captura y procesamiento completados")
            self.boton_modelo['state'] = 'normal'
        except Exception as e:
            print(f"Error en captura y procesamiento: {e}")
            print(traceback.format_exc())
            self.estado.config(text="Error en captura y procesamiento")
    
    def crear_modelo(self):
        self.estado.config(text="Creando modelo 3D...")
        self.progreso['value'] = 0
        self.update()
        
        try:
            modelo_3d = crear_modelo_3d(self.imagenes_procesadas, self.profundidades)
            if modelo_3d is None:
                raise Exception("No se pudo crear el modelo 3D")
            
            self.progreso['value'] = 50
            self.update()
            
            self.estado.config(text="Guardando archivo OBJ...")
            nombre_modelo = filedialog.asksaveasfilename(defaultextension=".obj", filetypes=[("OBJ files", "*.obj")])
            if nombre_modelo:
                ruta_modelo = guardar_obj(modelo_3d, nombre_archivo=os.path.basename(nombre_modelo))
                if ruta_modelo is None:
                    raise Exception("No se pudo guardar el archivo OBJ")
                
                self.progreso['value'] = 100
                self.update()
                
                messagebox.showinfo("Modelo 3D Completado", f"El modelo 3D se ha guardado como {ruta_modelo}")
                self.estado.config(text="Proceso completado")
            else:
                self.estado.config(text="Guardado cancelado")
        except Exception as e:
            print(f"Error al crear el modelo: {e}")
            print(traceback.format_exc())
            messagebox.showerror("Error", f"No se pudo crear el modelo 3D: {e}")
            self.estado.config(text="Error al crear el modelo")
    
    def visualizar_modelo(self):
        try:
            ruta_archivo = filedialog.askopenfilename(filetypes=[("OBJ files", "*.obj")])
            if ruta_archivo:
                visualizar_obj(ruta_archivo)
        except Exception as e:
            print(f"Error al visualizar el modelo: {e}")
            print(traceback.format_exc())
            messagebox.showerror("Error", f"No se pudo visualizar el modelo: {e}")
    
    def limpiar_capturas(self):
        try:
            carpeta_capturas = os.path.join(os.getcwd(), 'capturas')
            if os.path.exists(carpeta_capturas):
                shutil.rmtree(carpeta_capturas)
                os.makedirs(carpeta_capturas)
                messagebox.showinfo("Limpieza Completada", "La carpeta de capturas ha sido limpiada")
            else:
                messagebox.showinfo("Información", "La carpeta de capturas no existe")
        except Exception as e:
            print(f"Error al limpiar la carpeta de capturas: {e}")
            print(traceback.format_exc())
            messagebox.showerror("Error", f"No se pudo limpiar la carpeta de capturas: {e}")

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
