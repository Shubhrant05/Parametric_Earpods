import argparse
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import copy 

def create_earpods_model(radius, length, width, bud_thickness):

    # Create a cylinder for the earpod -- the vertical part
    earpod_cylinder = o3d.geometry.TriangleMesh.create_cylinder(
        radius=0.7, # fixed radius of vertical cylinder part to avoid problems
        height=length
    )

    # Create the earbud-tunnel part of the earpod -- the part that connects vertical end to silicon earbud
    earbud_cylinder2 = o3d.geometry.TriangleMesh.create_cylinder(
        radius=radius,
        height=width 
    )
    earbud_cylinder2_r = copy.deepcopy(earbud_cylinder2)
    R = earbud_cylinder2.get_rotation_matrix_from_xyz((np.pi / 2, 0, np.pi / 4))
    earbud_cylinder2_r.rotate(R, center=(0, 0, 0))
    earbud_cylinder2_r.translate([0,0.7+width/2,length / 2 - radius ])

    # Creating the silicon earbud part of earpod -- made using a torus

    radius = radius
    thickness = bud_thickness
    resolution = 70
    earbud_torus = o3d.geometry.TriangleMesh.create_torus(radius, thickness, resolution)
    earbud_torus_r = copy.deepcopy(earbud_torus)
    R = earbud_torus.get_rotation_matrix_from_xyz((np.pi / 2, 0, np.pi / 4))
    earbud_torus_r.rotate(R, center=(0, 0, 0))
    earbud_torus_r.translate([0,width+0.7,length / 2 - radius])

    # Combine the all sub part to create the earpod model

    earpod_model = earpod_cylinder + earbud_cylinder2_r + earbud_torus_r

    return earpod_model

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a 3D model of earpods.')
    parser.add_argument('--radius', type=float, help='Radius of the earpod cylinder.', default=0.55)
    parser.add_argument('--length', type=float, help='Length of the earpod cylinder.', default=7)
    parser.add_argument('--width', type=float, help='Width of the earbud.', default=1.5)
    parser.add_argument('--bud-thickness', type=float, help='Thickness of the earbud.', default=0.4)

    args = parser.parse_args()

    earpod_model = create_earpods_model(args.radius, args.length, args.width ,args.bud_thickness)

    o3d.visualization.draw_geometries([earpod_model])
