import  os, json, re

from powerbpy.dashboard import Dashboard
from powerbpy.page import Page

class _Visual:
	def __init__(page, 
                #  page_id, 
				  visual_id, 

				  data_source, 
				  visual_title, 
				  
				  height, 
				  width,
				  x_position, 
				  y_position, 
				
				  z_position = 6000, 
				  tab_order=-1001):

		if not isinstance(page, Page):
			raise TypeError("Visuals must be added to a specific page")

		# Get everything else from the dashboard
		# Attribute delegation (inherit parent instance attributes)
		def __getattr__(self, name):
			return getattr(self._page, name)

		self.page = page
		self.visual_id = visual_id
		self.visual_title = visual_title
		self.height = height
		self.width = width
		self.x_position = position
		self.z_position = z_position
		self.tab_order = tab_order

