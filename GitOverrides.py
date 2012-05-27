
import sys, os, os.path, soya, soya.sphere
import git

soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))
sphere_world = soya.World.load("sphere")		
sphere_model = sphere_world.to_model()

class Commit3D(soya.Body, git.Commit):

	def __init__(self, parent, commit, cam):
		soya.Body.__init__(self, parent, sphere_model)
		git.Commit.__init__(self, commit.repo, commit.id, commit.tree, commit.author, commit.authored_date, commit.message, commit.parents)
		self.camera = cam

	def begin_round(self):
		soya.Body.begin_round(self)
		
		# Processes the events
		
		for event in soya.process_event():
			
			if event[0] == soya.sdlconst.MOUSEMOTION:
				mouse_pos = self.camera.coord2d_to_3d(event[1], event[2], -15.0)
				mouse_pos.x = abs(mouse_pos.x + self.camera.x)
				mouse_pos.y = abs(mouse_pos.y + self.camera.y)
				if abs(mouse_pos.x - self.x - 1) < 1 and abs(mouse_pos.y-self.y-1) < 1:
					if self.entering_zone == 0:
						print self.message
					self.entering_zone = 1
				elif abs(mouse_pos.x - self.x - 1) > 1 or abs(mouse_pos.y-self.y-1) > 1:
					self.entering_zone = 0
