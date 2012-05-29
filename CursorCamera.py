import sys, soya, soya.sdlconst
import os
class ControlledCamera(soya.Camera):
	def __init__(self, parent):
		soya.Camera.__init__(self, parent)
		self.left_key_down = self.right_key_down = self.up_key_down = self.down_key_page_down  = self.down_key_page_up  =self.down_key_down = 0
		
	def begin_round(self):
		soya.Camera.begin_round(self)
		
		# Processes the events
		
		for event in soya.process_event():
			if   event[0] == soya.sdlconst.KEYDOWN:
				if   (event[1] == soya.sdlconst.K_r):
#					soya._main.stop(self)
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
		proportion = 0.2
		if (self.left_key_down == 1):		self.x -= proportion
		if (self.right_key_down == 1):		self.x += proportion
		if (self.up_key_down == 1):		self.y += proportion
		if (self.down_key_down == 1):		self.y -= proportion
		if (self.down_key_page_down == 1):	self.z += proportion
		if (self.down_key_page_up == 1):	self.z -= proportion


#			if event[0] == soya.sdlconst.BUTTON_WHEELDOWN:
#				print "wheeldown"
#				self.z = self.z + 1
#			elif event[0] == soya.sdlconst.BUTTON_WHEELUP:
#				self.z = .z - 1
#				print "wheelup"
#			elif event[0] == soya.sdlconst.BUTTON_LEFT:
#			if event[0] == soya.sdlconst.MOUSEMOTION:
#				self.mouse_pos = camera.coord2d_to_3d(event[1], event[2], -15.0)
#				self.move(self.mouse_pos)
		
