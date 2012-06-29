# This file is part of git3k software
# Copyright (C) 2012  <Luc Banda>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


import sys, os, os.path, soya, soya.sphere, time
import git

soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

			
class GitLabel(soya.Body):
	label_green = soya.World.load("label_green").to_model()
	label_yellow = soya.World.load("label_yellow").to_model()
	label_white = soya.World.load("label_white").to_model()
	label_blue = soya.World.load("label_blue").to_model()
	label_red = soya.World.load("label_red").to_model()
	
	def __init__(self, parent, name, world, commit):
		soya.Body.__init__(self, parent, world)
		self.parent.x = commit.x
		self.parent.y = commit.y
		self.name = name
		self.label = soya.label3d.Label3D(parent, name)
		self.label.size = 0.04
		self.label.set_xyz(5.5, 0.0, 1.0)
		self.label.lit = 0
		self.commit = commit
		commit.appendlabel(self)
		self.old_model=self.model
		
	def rotate_y(self, angle):
		self.parent.rotate_y(angle)
			
	def select(self):
		self.set_color("RED")
		
	def unselect(self):
		self.set_color("RESTORE")
				
	def set_color(self,color, permanent = 0):
		if color == 'RESTORE':
			self.model = self.old_model
		if color == 'YELLOW':
			self.model = self.label_yellow
		elif color == 'RED':
			self.model = self.label_red
		elif color == 'BLUE':
			self.model = self.label_blue
		elif color == 'GREEN':
			self.model = self.label_green
		if permanent == 1:
			self.old_model = self.model
			
	
		
class BranchLabel(GitLabel):
	
	def __init__(self, parent, name, commit):
		GitLabel.__init__(self, soya.World(parent), name, self.label_green, commit)

	def description(self):
		return "Branch : " + self.name
		
		
class TagLabel(GitLabel):
	def __init__(self, parent, name, commit):
		GitLabel.__init__(self, soya.World(parent), name, self.label_yellow, commit)
	
	def description(self):
		return "Tag : " + self.name
		
class RemoteLabel(GitLabel):
	def __init__(self, parent, name, commit):
		GitLabel.__init__(self, soya.World(parent), name, self.label_blue, commit)
	
	def description(self):
		return "Remote : " + self.name
		
def cmpchilds(x, y):
	if x.size_of_queue > y.size_of_queue:
		return -1
	elif x.size_of_queue < y.size_of_queue:
		return 1
	else:
		return 0
		
class Commit3D(soya.Body):
	sphere_white = soya.World.load("sphere_white").to_model()
	sphere_blue = soya.World.load("sphere_blue").to_model()
	sphere_yellow = soya.World.load("sphere_yellow").to_model()
	sphere_red = soya.World.load("sphere_red").to_model()
	sphere_green = soya.World.load("sphere_green").to_model()


	entering_zone = 0
	faces = []
	
	def __init__(self, parent, commit, faces):
		soya.Body.__init__(self,parent, self.sphere_white)
		self.parents = []
		self.size_of_queue = 0
		self.faces_world = faces
		self.commit = commit
		self.old_model=self.model
		self.childs = []
		self.label = soya.label3d.Label3D(parent, self.commit.message)
		self.vertex1 = soya.Vertex(self.faces_world, self.x-0.1, self.y-0.1, self.z-0.1)
		self.vertex2 = soya.Vertex(self.faces_world, self.x+0.1, self.y+0.1, self.z+0.1)
		self.labels = []
		self.autoposed = False
		
	def description(self):
		string  = self.commit.hexsha + "\n\n"
		string += "author : " + str(self.commit.committer) + "\n"
		commited_time = time.gmtime(self.commit.committed_date)
		string += "date : " + str(time.asctime(commited_time)) + "\n\n"
		string += self.commit.message + "\n\n"
		#~ if len(self.parents) == 1:
			#~ string += "".join([str(diffi.diff for diffi in self.commit.tree.diff(self.parents[0].commit.tree, create_patch=True))])
		
		return string
		
	def select(self):
		self.set_color("RED")
		
	def unselect(self):
		self.set_color("RESTORE")
				
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
			
	def size(self):
		return 3.0

	def appendlabel(self, label):
		label.rotate_y(45.0 * len(self.labels))
		self.labels.append(label)
		
		
	def linkparents(self, commits):
		for par in self.commit.parents:
			parent = commits[par.hexsha]
			parent.childs.append(self)
			self.parents.append(parent)
			self.faces.append(soya.Face(self.faces_world, [self.vertex1,self.vertex2,  parent.vertex1, parent.vertex2]))
	
	def sort_childs(self):
		self.childs.sort(cmpchilds)
		
	def set_coords(self, x, y):
		self.y = y
		self.x = x
		self.vertex1.set_xyz(x,y,self.z)
		self.vertex2.set_xyz(x+0.1,y+0.1,self.z+0.1)
		self.label.set_xyz(self.x, self.y, self.z)
		self.label.size = 0.02
	
	def get_coords(self):
		return (self.x,self.y)
		
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
	
	def set_label(self, label):
		self.label.text = label
		
class Repo3D(soya.World):

	def __init__(self, parent, path, centerpos):
		soya.World.__init__(self, parent)
		self.repo = git.Repo(path)

		self.commit3d = {}
		self.faces = soya.World()
		self.centerpos = centerpos
		self.commitbyxy = {}
		#creating objects
		self.populate()
		#setting depth
		self.depth(self.initial)
		#setting parents
		self.grow_tree()
		#display links
		soya.Body(self.parent, self.faces.to_model())	
		#identify head
		self.head3d = self.commit3d[self.repo.commit(self.repo.head).hexsha]
		self.head3d.set_color('YELLOW', 1)
		self.labels = []
		for head in self.repo.heads:
			self.labels.append(BranchLabel(self.parent,head.name, self.commit3d[head.commit.hexsha]))
		for remote in self.repo.remotes:
			if remote.name != "remote":
				for remoteref in remote.refs:
					self.labels.append(RemoteLabel(self.parent,remoteref.name, self.commit3d[remoteref.commit.hexsha]))
		for tag in self.repo.tags:
			self.labels.append(TagLabel(self.parent,tag.name, self.commit3d[tag.commit.hexsha]))
		
	def depth(self, commit):
		
		if len(commit.childs) == 0:
			commit.size_of_queue = 0
		for child in commit.childs:
			commit.size_of_queue = max(self.depth(child)+1, commit.size_of_queue)
		commit.sort_childs()
		return commit.size_of_queue
		
	def create_recurse(self, commit):
		commit3d = Commit3D(self.parent, commit, self.faces)
		if len(commit.parents) == 0:
			self.initial = commit3d
		for parent in commit.parents:
			if not parent.hexsha in self.commit3d:
				commit= self.create_recurse(parent)
				self.commit3d[parent.hexsha] = commit				
		return commit3d
		
	def populate(self):
		#creating all commits3d
		for ref in self.repo.refs:
			commit =ref.commit
			if not commit.hexsha in self.commit3d:
				ret = self.create_recurse(commit)
				self.commit3d[commit.hexsha] = ret
				
		for commit in self.commit3d.itervalues():
			commit.linkparents(self.commit3d)
	
	def place_recurse(self, commit):
		for child in commit.childs:
			if child.autoposed:
				return
			child.autoposed = True
			child.set_coords(commit.x, commit.y + commit.size())
			index_free= -15.0
			while child.get_coords() in self.commitbyxy:
				index_free += 15.0
				child.set_coords(index_free, child.y)
			#child.set_label(child.commit.message + str(child.get_coords()) + "\n" + str(child.size_of_queue))
			self.commitbyxy[child.get_coords()] = child
			self.place_recurse(child)
	
	def grow_tree(self):
		commit = self.initial
		commit.set_coords(self.centerpos, 0.0)
		self.commitbyxy[commit.get_coords()] = commit
		self.place_recurse(commit)
		
