'''
This script changes the title of the webpage from index to something more meaningful.
It'd be awesome if quarto provided a title argument so I didn't have to do all this
hacky stuff messing with the html after it's rendered...
'''

import shutil

from bs4 import BeautifulSoup as bs

OLD_HOME_PAGE = "docs/docs/index.html"
NEW_HOME_PAGE = "output1.html"

# open the newly rendered home page
with open(OLD_HOME_PAGE, "r", encoding="utf-8") as file:

    # parse the html
    soup = bs(file.read(), "html.parser")

    # find and replace the title
    title = soup.find("title")
    title.string = "Power Bpy"


# write the new file out
with open(NEW_HOME_PAGE, "w", encoding="utf-8") as file:
    file.write(str(soup))

# overwrite the old file with the new file
shutil.move(NEW_HOME_PAGE, OLD_HOME_PAGE)
