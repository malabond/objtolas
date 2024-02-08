import numpy as np
import cv2
import pylas

def read_obj(obj_filename):
    vertices = []
    texture_coords = []
    faces = []
    with open(obj_filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts:
                if parts[0] == 'v':
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif parts[0] == 'vt':
                    texture_coords.append([float(parts[1]), float(parts[2])])
                elif parts[0] == 'f':
                    face = [list(map(int, v.split('/'))) for v in parts[1:]]
                    faces.append(face)
    return np.array(vertices), np.array(texture_coords), faces

def get_vertex_colors(vertices, texture_coords, faces, texture_image):
    colors = np.zeros((len(vertices), 3), dtype=np.uint16)
    for face in faces:
        for vert in face:
            vert_index, tex_index = vert[0] - 1, vert[1] - 1
            u, v = texture_coords[tex_index]
            x, y = int(u * texture_image.shape[1]), int((1-v) * texture_image.shape[0])
            color = texture_image[y, x]  # OpenCV images are BGR
            colors[vert_index] = color[::-1]  # Convert BGR to RGB
    return colors

def obj_to_las_with_color(obj_filename, las_filename, texture_filename):
    vertices, texture_coords, faces = read_obj(obj_filename)
    texture_image = cv2.imread(texture_filename)
    colors = get_vertex_colors(vertices, texture_coords, faces, texture_image)
    
    vertices_array = np.array(vertices)
    colors_array = np.array(colors, dtype=np.uint16)
    
    las = pylas.create(point_format_id=2)  # Point format 2 supports RGB colors
    las.x = vertices_array[:, 0]
    las.y = vertices_array[:, 1]
    las.z = vertices_array[:, 2]
    las.red = colors_array[:, 0]
    las.green = colors_array[:, 1]
    las.blue = colors_array[:, 2]
    
    las.write(las_filename)
    print(f"Converted {len(vertices)} vertices with colors to LAS format and saved as {las_filename}")

# File paths need to be adjusted based on your actual files
obj_filename = input("Enter the path of the OBJ file: ")
texture_filename = input("Enter the path of the jpg file: ")
las_filename = input("Enter the path of the LAS file: ")

obj_to_las_with_color(obj_filename, las_filename, texture_filename)
