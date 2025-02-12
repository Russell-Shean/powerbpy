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
	new_file.write("include-before-body:\n")
	new_file.write(" text: |\n")
	new_file.write('  <script>document.title = "Power Bpy";</script>\n')
	new_file.write("---\n\n")

	# That didn't work let's try adding an ojs block
	#new_file.write('```{ojs}\ndocument.title = "Power Bpy"\n```\n\n')

	with open(og_readme_path, "r") as old_file:
		for line in old_file.readlines():
			line = line.replace("batchfile", "dosbat")
			new_file.write(line)


