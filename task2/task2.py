import json
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import argparse
import sys

def sphere_collision(file_name):
    str(file_name)
    with open(file_name) as json_file:
       data = json.load(json_file) 
       for sphere in data['sphere']:
           center = data['sphere']['center']
           radius = data['sphere']['radius']
       for line in data['sphere']:
           start_point = data['line']['a']
           end_point = data['line']['b']

    length = [0,0,0]
    
    cx = center[0]
    cy = center[1]
    cz = center[2]
    
    x0 = start_point[0]
    y0 = start_point[1]
    z0 = start_point[2]
    
    x1 = end_point[0]
    y1 = end_point[1]
    z1 = end_point[2]
   
    for i in range(len(start_point)):
        length[i] = end_point[i] - start_point[i]
        
    l0 = length[0]
    l1 = length[1]
    l2 = length[2]
  
    A = l0 ** 2 + l1 ** 2 + l2 ** 2
    B = 2 * (x0*l0 + y0*l1 +  z0*l2 - l0*cx - l1*cy - l2*cz)
    C = x0**2 - 2*x0*cx + cx**2 + y0**2 - 2*y0*cy + cy**2 + z0**2 - 2*z0*cz + cz**2 - radius**2
    
    discriminant = B**2 - 4*A*C
    
    if discriminant < 0:
        print('Коллизий не найдено')
        
    elif discriminant == 0:
        t1 = ( - B - sqrt(discriminant)) / (2 * A)
        collision_x1 = x0 * (1 - t1) + t1 * x1
        collision_y1 = y0 * (1 - t1) + t1 * y1
        collision_z1 = z0 * (1 - t1) + t1 * z1
        
        print(round(collision_x1, 2), round(collision_y1, 2), round(collision_z1, 2))
        
    elif discriminant >= 0:
        t1 = ( - B - sqrt(discriminant)) / (2 * A)
        t2 = ( - B + sqrt(discriminant)) / (2 * A)
        collision_x1 = x0 * (1 - t1) + t1 * x1
        collision_y1 = y0 * (1 - t1) + t1 * y1
        collision_z1 = z0 * (1 - t1) + t1 * z1
        
        collision_x2 = x0 * (1 - t2) + t2 * x1
        collision_y2 = y0 * (1 - t2) + t2 * y1
        collision_z2 = z0 * (1 - t2) + t2 * z1
        
        print(round(collision_x1, 2), round(collision_y1, 2), round(collision_z1, 2) , '\t', round(collision_x2, 2), round(collision_y2, 2), round(collision_z2, 2))
        
    # Блок визуализации
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Задаем параметры прорисовки сферы
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = radius * np.outer(np.cos(u), np.sin(v)) + cx
    y = radius * np.outer(np.sin(u), np.sin(v)) + cy
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + cz

    # 
    x2 = np.linspace(x0, x1)
    y2 = np.linspace(y0, y1)
    z2 = np.linspace(z0, z1)

    ax.plot(x2, y2, z2)

    # Plot the surface
    #ax.plot_surface(x, y, z, color='r')
    ax.plot_wireframe(x, y, z, color="r")

    plt.show()
    
    
def createParser ():
    par = argparse.ArgumentParser()
    par.add_argument('file_name', nargs='?')
    return par

def main(a):
    #try:
    sphere_collision(a)
    #except:
    #    print('Неверные данные!')
        
        
if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    main(args.file_name)

     
           

