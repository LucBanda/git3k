# -*- indent-tabs-mode: t -*-

# Imports and inits Soya.

import sys, os, os.path, soya, soya.sphere
import cerealizer
from CursorCamera import ControlledCamera
from GitOverrides import *

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))


# Creates the scene.

scene = soya.World()


# Creates a light.

light = soya.Light(scene)
light.set_xyz(1000.0, 1000.0, 1000.0)

# Creates a camera.

camera = ControlledCamera(scene)
camera.set_xyz(0.0, 17.0, 30.0)


repo = Repo3D(scene, '.', camera)

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()
