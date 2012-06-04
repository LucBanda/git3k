
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

	def __init__(self, parent, commit, cam, faces):
		soya.Body.__init__(self,parent, self.sphere_white)
		self.faces_world = faces
		self.commit = commit
		self.old_model=self.model
		self.camera = cam
		self.label = soya.label3d.Label3D(parent, self.commit.message)
		self.vertex1 = soya.Vertex(self.faces_world, self.x-0.1, self.y-0.1, self.z-0.1)
		self.vertex2 = soya.Vertex(self.faces_world, self.x+0.1, self.y+0.1, self.z+0.1)

	def append(self, parentcmt):
		self.parents.append(parentcmt)
		self.faces.append(soya.Face(self.faces_world, [self.vertex1,self.vertex2,  parentcmt.vertex1, parentcmt.vertex2]))

	def set_coords(self, x, y):
		self.y = y
		self.x = x
		self.vertex1.set_xyz(x,y,self.z)
		self.vertex2.set_xyz(x+0.1,y+0.1,self.z+0.1)
		self.label.set_xyz(self.x, self.y+0.5, self.z)
		self.label.size = 0.04
		
	def set_color(self,color, permanent = 0):
		if color == 'RESTORE':
			self.model = self.old_model
		if color == 'YELLOW':
			self.model = self.sphere_yellow
		elif color == 'RED':
			self.model = self.sphere_red
		elif color == 'BLUE':
			self.model = self.sphere_blue
		elif color == 'GREEN':
			self.model = self.sphere_green
		if permanent == 1:
			self.old_model = self.model

	
class Repo3D(soya.World, git.Repo):

	def __init__(self, parent, path, cam, centerpos):
		self.commit3d = {}
		self.world = soya.World()
		soya.World.__init__(self, parent)
		git.Repo.__init__(self, path)
		self.cam = cam
		self.head = self.commit( self.git.log(n=1, pretty="format:%H"))
		
		self.draw_branch(self.commit('master'), centerpos)
		j = 0
		for head in self.branches:
			j+= 1
			x = 15*j+centerpos
			if head.name != 'master':
				self.draw_branch(head.commit, x)

		self.commit3d[self.head.id].set_color('YELLOW', 1)
		soya.Body(parent, self.world.to_model())
			

	def draw_branch(self, top, x):
		commit3d = Commit3D(self.parent, top, self.cam, self.world)
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
			next = self.draw_branch(parent_commit, x+15.0*i)
			commit3d.set_coords(x, next.y + 3.0)
			commit3d.append(next)
			i+=1

		return commit3d
