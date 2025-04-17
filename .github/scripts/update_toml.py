import re, shutil

import argparse

# commandline args code modified from here: https://stackoverflow.com/a/42929351/16502170
parser = argparse.ArgumentParser("Update semantic version in pyproject.toml file with the github release tag")
parser.add_argument("release_tag", help="This should be the release tag provided by githb actions as: ${{ github.event.release.tag_name }}.", type=str)
args = parser.parse_args()



with open("./pyproject3.toml", "w") as tmp:
  with open("./pyproject.toml", "r") as file:
    for line in file.readlines():
      
      # look for the version line and extract version
      version_match = re.search('(?<=version = ").*(?=")', line )

      #print(line)

      # if a version was found
      if version_match is not None:
        print(line)
        print(version_match.group(0))

        # add one to the old version
        print(version_match.group(0))
        ending_number = re.search("\\d+$" , version_match.group(0))
        print(ending_number.group(0))
      
        new_ending_number = int(ending_number.group(0)) + 1
        print(new_ending_number)

        release_tag = args.release_tag
        release_tag = release_tag.replace("v", "")

        #line = re.sub('\\d+"$', str(new_ending_number) + '"', line)
        line = line.replace(version_match.group(0), release_tag)
        print(line)


      tmp.write(line)

shutil.move("./pyproject3.toml", "./pyproject.toml")

    
