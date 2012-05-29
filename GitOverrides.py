
import sys, os, os.path, soya, soya.sphere
import git
import math

soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

			

class Commit3D(soya.Body, git.Commit):
	sphere_white = soya.World.load("sphere_white").to_model()
	sphere_blue = soya.World.load("sphere_blue").to_model() 	
	sphere_yellow = soya.World.load("sphere_yellow").to_model()
	sphere_red = soya.World.load("sphere_red").to_model()
	sphere_green = soya.World.load("sphere_green").to_model()						
	entering_zone = 0
	def __init__(self, parent, commit, cam):
		soya.Body.__init__(self, parent, self.sphere_white)
		git.Commit.__init__(self, commit.repo, commit.id, commit.tree, commit.author, commit.authored_date, commit.message, commit.parents)
		self.old_model=self.model
		self.camera = cam
		self.label = soya.label3d.Label3D(parent, self.message)

	def set_y(self, y):
		self.y = y
		self.label.set_xyz(self.x, self.y+0.5, self.z)
		self.label.size = 0.03
	def set_color(self,color):
		if color == 'YELLOW':
			self.model = self.sphere_yellow
		
	def begin_round(self):
		soya.Body.begin_round(self)
		
		# Processes the events
		
		for event in soya.process_event():
			
			if event[0] == soya.sdlconst.MOUSEMOTION:
				dist = self.distance_to(self.camera.coord2d_to_3d(event[1], event[2], self.z-self.camera.z))
				if dist < self.get_sphere()[1]:
					if self.entering_zone == 0:
#						print self.message
						self.old_model = self.model
						self.model = self.sphere_red

					self.entering_zone = 1
				elif dist > self.get_sphere()[1] and self.entering_zone == 1:
					self.entering_zone = 0
					self.model = self.old_model


class Repo3D(soya.World, git.Repo):
	commit3d = []

	def __init__(self, parent, path, cam):
		soya.World.__init__(self, parent)
		git.Repo.__init__(self, path)
		self.head = self.commit( self.git.log(n=1, pretty="format:%H"))
		i=0
		
		for commit in self.commits():
			self.commit3d.append(Commit3D(self, commit, cam))
			self.commit3d[i].set_y(30 - 3*i)				
			if self.commit3d[i].id == self.head.id:
				self.commit3d[i].set_color('YELLOW')
			i+=1
		
	def head(self):
		return self.head

