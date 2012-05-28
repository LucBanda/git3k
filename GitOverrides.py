
import sys, os, os.path, soya, soya.sphere
import git
import math

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
				me = self.camera.coord3d_to_2d(self.position())
				
				dist= math.sqrt(math.pow(me[0] - event[1],2)+math.pow(me[1] - event[2],2))
				if dist < 20:
					if self.entering_zone == 0:
						print self.message
					self.entering_zone = 1
				elif dist > 20:
					self.entering_zone = 0


class Repo3D(git.Repo):
	def __init__(self, parent, path, cam):
		git.Repo.__init__(self, path)
#		soya.World.__init__(self, parent)
		i=0
		for commit in self.commits():
			i+=1
			Commit3D(parent, commit, cam).y = 2*i

