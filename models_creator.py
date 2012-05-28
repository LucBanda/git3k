import sys, os, os.path, soya, soya.sphere

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

sphere = soya.sphere.Sphere()
sphere.filename = "sphere_white"
sphere.save()

material = soya.Material()

material.shininess = 64.0

YELLOW = (0.0, 1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0, 1.0)
GREEN = (0.0,1.0, 0.0,1.0)
BLUE = (0.0,0.0,1.0,1.0)

material.diffuse   = YELLOW
sphere = soya.sphere.Sphere(None, material)
sphere.filename = "sphere_yellow"
sphere.save()

material.diffuse   = RED
sphere = soya.sphere.Sphere(None, material)
sphere.filename = "sphere_red"
sphere.save()

material.diffuse   = GREEN
sphere = soya.sphere.Sphere(None, material)
sphere.filename = "sphere_green"
sphere.save()

material.diffuse   = BLUE
sphere = soya.sphere.Sphere(None, material)
sphere.filename = "sphere_blue"
sphere.save()

