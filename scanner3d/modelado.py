import numpy as np
import open3d as o3d
import os
import trimesh
import pyrender

def crear_modelo_3d(imagenes_procesadas, profundidades):
    try:
        print("Iniciando creación del modelo 3D...")
        pcd = o3d.geometry.PointCloud()
        all_points = []
        for i, (img, prof) in enumerate(zip(imagenes_procesadas, profundidades)):
            print(f"Procesando imagen {i+1} de {len(imagenes_procesadas)}")
            y, x = np.where(img > 0)
            z = prof[y, x]  # Usar la información de profundidad
            puntos = np.column_stack((x, y, z))
            all_points.append(puntos)
        
        all_points = np.vstack(all_points)
        pcd.points = o3d.utility.Vector3dVector(all_points)
        
        print("Eliminando outliers...")
        pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        
        print("Estimando normales...")
        pcd.estimate_normals()
        
        print("Reconstruyendo superficie...")
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)
        print("Modelo 3D creado exitosamente")
        return mesh
    except Exception as e:
        print(f"Error al crear el modelo 3D: {e}")
        return None

def guardar_obj(mesh, nombre_archivo="modelo_3d.obj"):
    try:
        print("Guardando modelo en formato OBJ...")
        carpeta_modelos = os.path.join(os.getcwd(), 'modelos')
        if not os.path.exists(carpeta_modelos):
            os.makedirs(carpeta_modelos)
        
        ruta_archivo = os.path.join(carpeta_modelos, nombre_archivo)
        o3d.io.write_triangle_mesh(ruta_archivo, mesh)
        print(f"Modelo guardado exitosamente en: {ruta_archivo}")
        return ruta_archivo
    except Exception as e:
        print(f"Error al guardar el modelo: {e}")
        return None

def visualizar_obj(ruta_archivo):
    try:
        print(f"Visualizando archivo OBJ: {ruta_archivo}")
        trimesh_mesh = trimesh.load(ruta_archivo)
        
        # Calcular las normales de las caras
        trimesh_mesh.fix_normals()
        
        # Crear un array de colores
        face_colors = np.ones((len(trimesh_mesh.faces), 4)) * [0.5, 0.5, 0.5, 1.0]  # Gris por defecto
        
        # Identificar las caras superiores (orientadas hacia arriba)
        up_vector = np.array([0, 1, 0])  # Asumiendo que Y es el eje vertical
        dot_products = np.dot(trimesh_mesh.face_normals, up_vector)
        upper_faces = dot_products > 0.7  # Ajusta este valor para cambiar la sensibilidad
        
        # Colorear las caras superiores de azul
        face_colors[upper_faces] = [0.0, 0.0, 1.0, 1.0]  # Azul
        
        # Asignar colores a las caras
        trimesh_mesh.visual.face_colors = face_colors
        
        # Convertir a un mesh de pyrender
        mesh = pyrender.Mesh.from_trimesh(trimesh_mesh, smooth=False)
        
        # Crear la escena
        scene = pyrender.Scene(bg_color=[1.0, 1.0, 1.0])
        scene.add(mesh)
        
        # Añadir luz
        light = pyrender.SpotLight(color=np.ones(3), intensity=3.0,
                                   innerConeAngle=np.pi/16.0,
                                   outerConeAngle=np.pi/6.0)
        scene.add(light, pose=np.eye(4))
        
        # Visualizar
        viewer = pyrender.Viewer(scene, use_raymond_lighting=True, viewport_size=(800, 600), 
                                 cull_faces=False, run_in_thread=True)
        
    except Exception as e:
        print(f"Error al visualizar el archivo OBJ: {e}")
        raise