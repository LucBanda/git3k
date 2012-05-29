
import sys, os, os.path, soya, soya.sphere
import git
import math

soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

			

class Commit3D(soya.Body):
	sphere_white = soya.World.load("sphere_white").to_model()
	sphere_blue = soya.World.load("sphere_blue").to_model() 	
	sphere_yellow = soya.World.load("sphere_yellow").to_model()
	sphere_red = soya.World.load("sphere_red").to_model()
	sphere_green = soya.World.load("sphere_green").to_model()						
	entering_zone = 0

	def __init__(self, parent, commit, cam):
		soya.Body.__init__(self, parent, self.sphere_white)
		self.commit = commit
		self.old_model=self.model
		self.camera = cam
		self.label = soya.label3d.Label3D(parent, self.commit.message)

	def set_coords(self, x, y):
		self.y = y
		self.x = x
		self.label.set_xyz(self.x, self.y+0.5, self.z)
		self.label.size = 0.04

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
						print self.commit.message
						self.old_model = self.model
						self.model = self.sphere_red

					self.entering_zone = 1
				elif dist > self.get_sphere()[1] and self.entering_zone == 1:
					self.entering_zone = 0
					self.model = self.old_model

class Repo3D(soya.World, git.Repo):
	commit3d = {}

	def __init__(self, parent, path, cam):
		soya.World.__init__(self, parent)
		git.Repo.__init__(self, path)
		self.cam = cam
		self.head = self.commit( self.git.log(n=1, pretty="format:%H"))
		j=0
		
		self.draw_branch('master', 0)
		j = 0
		for head in self.heads:
			j+= 1
			x = 10*j
			if head.name != 'master':
				self.draw_branch(head.name, x)
			
				
		print self.commit3d.keys()

	def draw_branch(self, branchname, x):
		i=0
		for commit in self.commits(branchname, max_count=100):
			base = None
			if not commit.id in self.commit3d:
				tmpcmt = Commit3D(self, commit, self.cam)
				self.commit3d[commit.id] = tmpcmt
				tmpcmt.set_coords(x, - 3.0*i)
				if commit.id == self.head.id:
					tmpcmt.set_color('YELLOW')
				i+=1
			else : 
				base = self.commit3d[commit.id]
				break

		#redraw from base
		if base != None:
			print base.commit.message
			j=0
			for commit in self.commits(branchname, max_count=100):
				commit3d = self.commit3d[commit.id]
				if commit3d.x == x:
					print (i,j,commit.message)
					commit3d.set_coords(x, base.y + (i-j)*3.0)
					j+=1








