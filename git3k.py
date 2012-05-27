# -*- indent-tabs-mode: t -*-

# Imports and inits Soya.

import sys, os, os.path, soya, soya.sphere
import cerealizer
from CursorCamera import ControlledCamera

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))


# Creates the scene.

scene = soya.World()

# The soya.sphere module contains a Sphere function that creates and returns a World
# with several faces inside, organized in a sphere (see soya.sphere.Sphere.__doc__
# for more info).
# By default, soya.sphere creates smooth-lit faces.


# Compiles sphere_world and faceted_ball_world into Model.
# Creates a sphere Body in the scene, using the compilation of sphere_word as Model.
# Notice the use of World.to_model() to compile a World.

sphere_world = soya.World.load("sphere")
sphere_world.filename = "sphere"

sphere_model = sphere_world.to_model()
sphere = [soya.Body(scene, sphere_world.to_model()) for i in range(10)]
for i in range(10):
	sphere[i] = soya.Body(scene, sphere_model)
	sphere[i].y=2*i



# Creates a light.

light = soya.Light(scene)
light.set_xyz(10.0, 10.0, 20.0)

# Creates a camera.

camera = ControlledCamera(scene)
camera.set_xyz(0.0, 10.0, 20)

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()
