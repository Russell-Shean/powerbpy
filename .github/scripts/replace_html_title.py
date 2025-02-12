'''
This script changes the title of the webpage from index to something more meaningful.
It'd be awesome if quarto provided a title argument so I didn't have to do all this
hacky stuff messing with the html after it's rendered...
'''


import bs4
from bs4 import BeautifulSoup as bs

import shutil

old_home_page = "docs/docs/index.html"
new_home_page = "output1.html"
 
# open the newly rendered home page
with open(old_home_page, "r", encoding="utf-8") as file:

	# parse the html
	soup = bs(file.read(), "html.parser")

	# find and replace the title
	title = soup.find("title")
	title.string = "Power Bpy"
 

# write the new file out
with open(new_home_page, "w", encoding="utf-8") as file:
    file.write(str(soup))

# overwrite the old file with the new file
shutil.move(new_home_page, old_home_page)




