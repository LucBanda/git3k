
import sys, os, os.path, soya, soya.sphere
import git

soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

			

class Commit3D(soya.Body):
	sphere_white = soya.World.load("sphere_white").to_model()
	sphere_blue = soya.World.load("sphere_blue").to_model() 	
	sphere_yellow = soya.World.load("sphere_yellow").to_model()
	sphere_red = soya.World.load("sphere_red").to_model()
	sphere_green = soya.World.load("sphere_green").to_model()	

	parents = []
	entering_zone = 0
	faces = []
	def __init__(self, parent, commit, cam):
		soya.Body.__init__(self, parent, self.sphere_white)
		self.commit = commit
		self.old_model=self.model
		self.camera = cam
		self.label = soya.label3d.Label3D(parent, self.commit.message)
		self.vertex = soya.Vertex(parent, self.x, self.y, self.z)
	
	def append(self, parentcmt):
		self.parents.append(parentcmt)
		self.faces.append(soya.Face(self.parent, [self.vertex, parentcmt.vertex]))

	def set_coords(self, x, y):
		self.y = y
		self.x = x
		self.vertex.set_xyz(x,y,self.z)
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
		
		self.draw_branch(self.commit('master'), 0)
		j = 0
		for head in self.branches:
			print head
			j+= 1
			x = 15*j
			if head.name != 'master':
				self.draw_branch(head.commit, x)

		self.commit3d[self.head.id].set_color('YELLOW')
			

	def draw_branch(self, top, x):
		commit3d = Commit3D(self.parent, top, self.cam)
		self.commit3d[top.id] = commit3d
		if len(top.parents) == 0:
			commit3d.set_coords(x, 0.0)
			return commit3d
		i=0
		for parent_commit in top.parents:
			if parent_commit.id in self.commit3d:
				base = self.commit3d[parent_commit.id]
				commit3d.append(base)
				commit3d.set_coords(x, base.y + 3.0)
				continue
			next = self.draw_branch(parent_commit, x+10.0*i)
			commit3d.set_coords(x, next.y + 3.0)
			commit3d.append(next)
			i+=1

		return commit3d
