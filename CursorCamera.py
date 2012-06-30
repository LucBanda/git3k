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

import sys, soya, soya.sdlconst
import os
import GitOverrides

class ControlledCamera(soya.Camera):
	def __init__(self, parent, center):
		soya.Camera.__init__(self, parent)
		self.left_key_down = self.right_key_down = self.up_key_down = self.down_key_page_down  = self.down_key_page_up  =self.down_key_down = 0
		self.proportion = 1
		self.move = 0
		self.points_to = center
		self.old_impact = None
		
	def set_text_displayer(self, text_displayer):
		self.text_displayer = text_displayer
		
	def begin_round(self):
		soya.Camera.begin_round(self)
		
		# Processes the events
		
		for event in soya.process_event():
			if   event[0] == soya.sdlconst.KEYDOWN:
				if   (event[1] == soya.sdlconst.K_h):
					self.text_displayer.set_text(" h : show this help\n r : restart \n q : quit\n ")
				elif   (event[1] == soya.sdlconst.K_r):
					os.system("./git3k&")
					sys.exit()
				elif   (event[1] == soya.sdlconst.K_q) or (event[1] == soya.sdlconst.K_ESCAPE):
					sys.exit()
				elif event[1] == soya.sdlconst.K_LEFT:  self.left_key_down  = 1
				elif event[1] == soya.sdlconst.K_RIGHT: self.right_key_down = 1
				elif event[1] == soya.sdlconst.K_UP:    self.up_key_down    = 1
				elif event[1] == soya.sdlconst.K_DOWN:  self.down_key_down  = 1
				elif event[1] == soya.sdlconst.K_PAGEDOWN:  self.down_key_page_down  = 1
				elif event[1] == soya.sdlconst.K_PAGEUP:  self.down_key_page_up  = 1
			elif event[0] == soya.sdlconst.KEYUP:
				if   event[1] == soya.sdlconst.K_LEFT:  self.left_key_down  = 0
				elif event[1] == soya.sdlconst.K_RIGHT: self.right_key_down = 0
				elif event[1] == soya.sdlconst.K_UP:    self.up_key_down    = 0
				elif event[1] == soya.sdlconst.K_DOWN:  self.down_key_down  = 0
				elif event[1] == soya.sdlconst.K_PAGEDOWN:  self.down_key_page_down  = 0
				elif event[1] == soya.sdlconst.K_PAGEUP:  self.down_key_page_up  = 0
				elif event[1] == soya.sdlconst.K_KP_PLUS:
					self.proportion += 0.1
				elif event[1] == soya.sdlconst.K_KP_MINUS:
					self.proportion -= 0.1
			elif event[0] == soya.sdlconst.MOUSEBUTTONDOWN:
				if event[1] == soya.sdlconst.BUTTON_RIGHT:
					self.move = 1
				elif event[1] == soya.sdlconst.BUTTON_MIDDLE:
					point = self.coord2d_to_3d(event[2], event[3], -5.0)
					point.convert_to(self.parent)

					self.points_to.y = point.y
					self.points_to.x = point.x
					
					self.rotate = 1
				elif event[1] == soya.sdlconst.BUTTON_WHEELUP:
					self.add_vector(soya.Vector(self, 0.0,0.0,-10.0))

				elif event[1] == soya.sdlconst.BUTTON_WHEELDOWN:
					self.add_vector(soya.Vector(self, 0.0,0.0,10.0))
				
			elif event[0] == soya.sdlconst.MOUSEBUTTONUP:
				if event[1] == soya.sdlconst.BUTTON_RIGHT:
					self.move = 0
				elif event[1] == soya.sdlconst.BUTTON_MIDDLE:
					self.rotate = 0
			elif event[0] == soya.sdlconst.MOUSEMOTION:
				if self.move == 1:
					self.add_vector(soya.Vector(self,  - event[3]/10.0, event[4]/10.0, 0.0))

				elif self.rotate == 1:
					self.add_vector(soya.Vector(self,  event[3], -event[4], 0.0))
					self.look_at(self.points_to)
				else:
					mouse = self.coord2d_to_3d(event[1], event[2])
				
					result = self.parent.raypick(self, self.vector_to(mouse))
					if result:
						impact, normal = result
						if type(impact.parent) == GitOverrides.Commit3D or \
						type(impact.parent) == GitOverrides.BranchLabel or \
						type(impact.parent) == GitOverrides.TagLabel or \
						type(impact.parent) == GitOverrides.RemoteLabel:
							if self.old_impact and impact != self.old_impact:
								self.old_impact.unselect()
							impact.parent.select()
							self.text_displayer.set_text(impact.parent.description())
							self.old_impact = impact.parent
					elif self.old_impact:
						self.old_impact.unselect()
						self.old_impact = None


				
		if (self.left_key_down == 1):		self.x -= self.proportion
		if (self.right_key_down == 1):		self.x += self.proportion
		if (self.up_key_down == 1):		self.y += self.proportion
		if (self.down_key_down == 1):		self.y -= self.proportion
		if (self.down_key_page_down == 1):	self.z += self.proportion
		if (self.down_key_page_up == 1):	self.z -= self.proportion
		
