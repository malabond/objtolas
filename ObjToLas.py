import pylas
import numpy as np

def obj_to_las(obj_filename, las_filename):
    # Read vertices from OBJ file
    vertices = []
    with open(obj_filename, 'r') as obj_file:
        for line in obj_file:
            parts = line.strip().split()
            if parts and parts[0] == 'v':  # Vertex definition
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])

    # Convert vertices list to numpy array for easier manipulation
    vertices_array = np.array(vertices)

    # Create a new LAS file
    # Automatically selects the LAS file version compatible with the provided point format
    las = pylas.create(point_format_id=2)  # Point format 0 is compatible with LAS 1.2, which is the minimum version we target

    # Populate the LAS file with vertices as point data
    # The 'x', 'y', and 'z' attributes expect data in the file's scale and offset, but for simplicity, we'll directly assign the vertex coordinates
    las.x = vertices_array[:, 0]
    las.y = vertices_array[:, 1]
    las.z = vertices_array[:, 2]

    # Write the populated LAS object to a file
    las.write(las_filename)

    print(f"Converted {len(vertices)} vertices to LAS format and saved as {las_filename}")

# Prompting user for filenames
obj_filename = input("Enter the path of the OBJ file: ")
las_filename = input("Enter the desired name/path for the LAS file: ")

obj_to_las(obj_filename, las_filename)