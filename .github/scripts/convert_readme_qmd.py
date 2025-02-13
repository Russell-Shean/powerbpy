'''
This file switches out the code highlighting blocks because Github and pandoc use different code highlighting services. 
Github recognizes batch scripts. Pandoc doesn't so we're going to call dosbat close enough for the quarto site.

We're also going to append some Javascript to: 
	1. Change the page title 
	2. Resize the smaller image and change its css float property to none 
	3. Remove quarto figure captions
'''

og_readme_path = "README.md"
index_qmd_path = "docs/index.qmd"


with open(index_qmd_path, "w") as new_file:
	new_file.write("---\n")
	new_file.write('Title: "Power Bpy"\n')

	# include a js script to update the title
	new_file.write("include-after-body:\n")
	new_file.write(" text: |\n")

	#  js~ Yay~~ 
	# change document title
	new_file.write('  <script>document.title = "Power Bpy";')

	# fix image in scroll bar - smaller, cuter, and floatier
	new_file.write('  document.querySelector("a.nav-link:nth-child(2) > img:nth-child(1)").style.height="140px";')
	new_file.write('  document.querySelector("a.nav-link:nth-child(2) > img:nth-child(1)").style.float="none";')

	# remove the figure captions on images
	# I could find the quarto setting, but this is easier lol
	# but I should eventually make this a standalone script....

	# find all the figure captions
	new_file.write('  const fig_captions = document.querySelectorAll(".figure > figcaption");')

	# loop through them and remove them
	new_file.write('  for(let caption of fig_captions){caption.remove();}')

	new_file.write('  </script>\n')
	new_file.write("---\n\n")

	# write the old file to the new file
	# after all the title stuff above
	with open(og_readme_path, "r") as old_file:
		for line in old_file.readlines():

			# Replace the code highlighting language
			line = line.replace("batchfile", "dosbat")
			new_file.write(line)


