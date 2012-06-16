
import sys, os, os.path, soya, soya.sphere
import git

soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

			
class GitLabel(soya.World):
	label_green = soya.World.load("label_green")
	label_yellow = soya.World.load("label_yellow")
	label_white = soya.World.load("label_white")
	
	def __init__(self, parent, name, world):
		soya.World.__init__(self, parent)
		self.label = soya.label3d.Label3D(self, name)
		self.label.size = 0.04
		self.label.set_xyz(3.5, 0.0, 1.0)
		self.label.lit = 0
		self.body = soya.Body(self, world.to_model())
		
class BranchLabel(GitLabel):
	
	def __init__(self, parent, name):
		GitLabel.__init__(self, parent, name, self.label_green)

class TagLabel(GitLabel):
	def __init__(self, parent, name):
		GitLabel.__init__(self, parent, name, self.label_yellow)
		
class RemoteLabel(GitLabel):
	def __init__(self, parent, name):
		GitLabel.__init__(self, parent, name, self.label_white)
		
class Commit3D(soya.Body):
	sphere_white = soya.World.load("sphere_white").to_model()
	sphere_blue = soya.World.load("sphere_blue").to_model()
	sphere_yellow = soya.World.load("sphere_yellow").to_model()
	sphere_red = soya.World.load("sphere_red").to_model()
	sphere_green = soya.World.load("sphere_green").to_model()

	parents = []
	entering_zone = 0
	faces = []

	def __init__(self, parent, commit, faces):
		soya.Body.__init__(self,parent, self.sphere_white)
		self.faces_world = faces
		self.commit = commit
		self.old_model=self.model

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
		self.label.set_xyz(self.x, self.y, self.z)
		self.label.size = 0.02
		
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

class Branch3D(soya.World):
	
	def __init__(self, parent, x, name = ""):
		soya.World.__init__(self, parent)
		self.x = x
		self.commit3d=[]
		self.bornes_y=(0.0,0.0)
		self.name = name
		#~ if name:
			#~ self.label = BranchLabel(parent, self.name)
		parent.branches3d.append(self)

	def set_name(self, name):
		self.name = name

	def append(self, commit3d):
		self.commit3d.append(commit3d)

	def update_bornes(self):
		if len(self.commit3d) != 0:
			self.bornes_y = (self.commit3d[0], self.commit3d[len(self.commit3d)-1])
	
	def set_x(self, x):
		self.x = x
		for commit3d in self.commit3d:
			commit3d.set_coords(x, commit3d.y)

	def overlaps(self, branch):
		if branch.x != self.x or branch == self: return False
		for commit1 in branch.commit3d:
			for commit2 in self.commit3d:
				if commit1.y == commit2.y:
					return True
		return False
	
	#def update(self):
		#~ if self.name:
			#~ self.label.set_xyz(self.x, self.commit3d[0].y, self.z)
		
	def __str__(self):
		ret ="BRANCH %s at %d\n" %(self.name, self.x)
		for commit in self.commit3d:
			ret = ret + commit.commit.message + "\n"
		return ret


class Repo3D(soya.World):

	def __init__(self, parent, path, centerpos):
		soya.World.__init__(self, parent)
		self.repo = git.Repo(path)

		self.commit3d = {}
		self.faces = soya.World()
		self.branches3d = []
		self.centerpos = centerpos
		self.draw()

	def get_branch_byname(self, pos, branchname):
		for br in self.branches3d:
			if branchname == br.name:
				return br
		return Branch3D(self, pos, branchname)

	def draw(self):
		branch = self.get_branch_byname(self.centerpos, "master")
		self.draw_branch(self.repo.commit('master'), branch)
		j = 0
		for head in self.repo.branches:
			j+= 1
			x = self.centerpos
			if head.name != 'master':
				branch = self.get_branch_byname(x, head.name)
				self.draw_branch(head.commit, branch)
				for branchiter in self.branches3d:
					if branch.overlaps(branchiter):
						branch.set_x(branch.x+15.0)


		self.head3d = self.commit3d[self.repo.commit( self.repo.head).hexsha]
		self.head3d.set_color('YELLOW', 1)
		soya.Body(self.parent, self.faces.to_model())			
	
	def draw_branch(self, top, branch):
		commit3d = Commit3D(self.parent, top, self.faces)
		branch.append(commit3d)
		self.commit3d[top.hexsha] = commit3d
		if len(top.parents) == 0:
			commit3d.set_coords(branch.x, 0.0)
			branch.update_bornes()
			
			return commit3d
		i=0
		for parent_commit in top.parents:
			if parent_commit.hexsha in self.commit3d:
				base = self.commit3d[parent_commit.hexsha]
				commit3d.append(base)
				commit3d.set_coords(branch.x, max(base.y + 3.0, commit3d.y))
				branch.update_bornes()
				continue
			newbranch=branch
			if i != 0:
				newbranch = Branch3D(self, newbranch.x)

			next = self.draw_branch(parent_commit, newbranch)
			commit3d.set_coords(branch.x, max(next.y + 3.0, commit3d.y))
			commit3d.append(next)
			i+=1
		for branchiter in self.branches3d:
			if branch.overlaps(branchiter):
				branch.set_x(branch.x+15.0)

		return commit3d

	def begin_round(self):
		soya.World.begin_round(self)
		
		# Processes the events
		
		#~ for event in soya.process_event():
			#~ if   event[0] == soya.sdlconst.KEYDOWN:
				#~ if   (event[1] == soya.sdlconst.K_F5):
					#~ self.reload()
					
