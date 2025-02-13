'''
This file switches out the code highlighting blocks because Github and pandoc use different code highlighting services. 
Github recognizes batch scripts. Pandoc doesn't so we're going to call dosbat close enough for the quarto site.

We're also going to try adding a qmd title, although I doubt that will work and I'll probably need to mess with the html file instead. 
This script will run on github actions each time the quartodoc rendering + gh page publishing action runs.
'''

import shutil


def add_html_title(og_path, title):

	temp_path = "this_is_stupid.qmd"

	with open(temp_path, "w") as new_file:
		new_file.write("---\n")
		new_file.write('Title: "Power Bpy - Function Reference"\n')

		# include a js script to update the title
		new_file.write("include-before-body:\n")
		new_file.write(" text: |\n")
		new_file.write(f'  <script>document.title = "{title}";</script>\n')
		new_file.write("---\n\n")


		with open(og_path, "r") as old_file:
			for line in old_file.readlines():
				new_file.write(line)


	shutil.move(temp_path, og_path)

# Change titles
og_path = "docs/reference/index.qmd"
title = "Power Bpy - Function Reference"
add_html_title(og_path, title)

og_path = "docs/worked_examples/index.qmd"
title = "Power Bpy - Worked examples"
add_html_title(og_path, title)

