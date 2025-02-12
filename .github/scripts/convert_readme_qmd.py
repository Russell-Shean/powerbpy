'''
This file switches out the code highlighting blocks because Github and pandoc use different code highlighting services. 
Github recognizes batch scripts. Pandoc doesn't so we're going to call dosbat close enough for the quarto site.

We're also going to try adding a qmd title, although I doubt that will work and I'll probably need to mess with the html file instead. 
This script will run on github actions each time the quartodoc rendering + gh page publishing action runs.
'''

og_readme_path = "README.md"
index_qmd_path = "docs/index.qmd"


with open(index_qmd_path, "w") as new_file:
	new_file.write("---\n")
	new_file.write('Title: "Power Bpy"\n')

	# include a js script to update the title
	new_file.write("include-before-body:\n")
	new_file.write(" text: |\n")

	# super duper dumb js~ Yay~~ 
	# change document title
	new_file.write('  <script>document.title = "Power Bpy";')

	# fix image in scroll bar - smaller, cuter, and floatier
	new_file.write('  document.querySelector("a.nav-link:nth-child(2) > img:nth-child(1)").style.height="140px";')
	new_file.write('  document.querySelector("a.nav-link:nth-child(2) > img:nth-child(1)").style.float="none";')

	# remove the stupid figure captions on images
	# I could find the quarto setting, but this is easier lol
	# but I should eventually make this a standalone script....

	# find all the figure captions
	new_file.write('  const fig_captions = document.querySelectorAll(".figure > figcaption");')

	# loop through them and remove them
	new_file.write('  for(let i = 0; i < fig_captions.length; i++){fig_captions[i].remove();}')

	new_file.write('  </script>\n')
	new_file.write("---\n\n")


	with open(og_readme_path, "r") as old_file:
		for line in old_file.readlines():
			line = line.replace("batchfile", "dosbat")
			new_file.write(line)


