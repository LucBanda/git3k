import sys, os, os.path, soya, soya.sphere

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

material = soya.Material()

material.shininess = 64.0

transparency = 0.5
YELLOW = (1.0, 1.0, 0.0, transparency)
RED = (1.0, 0.0, 0.0, transparency)
GREEN = (0.0,1.0, 0.0, transparency)
BLUE = (0.0,0.0,1.0, transparency)
WHITE = (1.0,1.0,1.0,transparency)

def color_to_str(color):
	if color == YELLOW: return "yellow"
	if color == RED: return "red"
	if color == GREEN: return "green"
	if color == BLUE: return "blue"
	if color == WHITE: return "white"

material.diffuse   = WHITE
sphere = soya.sphere.Sphere(None, material)
sphere.filename = "sphere_white"
sphere.save()


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

transparency = 1.0
YELLOW = (0.5, 0.5, 0.0, transparency)
RED = (1.0, 0.0, 0.0, transparency)
GREEN = (0.0,0.5, 0.0, transparency)
BLUE = (0.0,0.0,1.0, transparency)
WHITE = (1.0,1.0,1.0,transparency)


def create_label( color):
	world=soya.World()
	apex  = soya.Vertex(world,  1.0,  0.0,  0.0, diffuse = color)
	base1 = soya.Vertex(world,  1.5, 0.5,  0.5, diffuse = color)
	base2 = soya.Vertex(world, 1.5, 0.5,  -0.5, diffuse = color)
	base3 = soya.Vertex(world, 1.5, -0.5, -0.5, diffuse = color)
	base4 = soya.Vertex(world,  1.5, -0.5, 0.5, diffuse = color)
	extremity1 = soya.Vertex(world,  4.0, 0.5, 0.5, diffuse = color)
	extremity2 = soya.Vertex(world,  4.0, 0.5, -0.5, diffuse = color)
	extremity3 = soya.Vertex(world,  4.0, -0.5, -0.5, diffuse = color)
	extremity4 = soya.Vertex(world,  4.0, -0.5, 0.5, diffuse = color)

	soya.Face(world, [apex, base1, base2])
	soya.Face(world, [apex, base2, base3])
	soya.Face(world, [apex, base3, base4])
	soya.Face(world, [apex, base4, base1])
	
	soya.Face(world, [base1, base2, extremity2, extremity1])
	soya.Face(world, [base2, base3, extremity3, extremity2])
	soya.Face(world, [base3, base4, extremity4, extremity3])
	soya.Face(world, [base4, base1, extremity1, extremity4])
	
	soya.Face(world, [extremity1, extremity2, extremity3, extremity4])
	world.filename = "label_"+color_to_str(color)
	world.save()
	
create_label(GREEN)
create_label(YELLOW)
create_label(WHITE)


