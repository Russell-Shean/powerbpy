# Power Bpy <a id="hex-sticker" href="https://russell-shean.github.io/powerbpy/"><img src="https://github.com/user-attachments/assets/e372239d-5c28-4ed1-acf6-fb96a03b8a1a" align="right" height="240" /></a>  
Do you wish you could build dashboard with python or R, but can't because the client specifically asked for Power BI or your employer only supports publishing Power BI? Do you love love love Power BI, but wish there was a way to automatically generate parts of your dashboard to speed up your development process?      


Introducing Power Bpy, a python package that lets you create Power BI dashboards using functions 💪 instead of a point-and-click interface 🥹. Dashboards created using these functions can be opened, edited and saved normally in Power BI desktop.       

This package uses the new .pbip/.pbir format with TMDL enabled. This stores dashboards as directories of text files instead of binary files letting you version control your dashboards! 🥳 These features are still preview features, so use this with caution until there's more clarity from microsoft about what they're going to do with .pbir and tmdl.       

[![pypi Version](https://img.shields.io/pypi/v/powerbpy.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/powerbpy/)
[![PyPI Downloads](https://static.pepy.tech/badge/powerbpy)](https://pepy.tech/projects/powerbpy)
[![Codecov test coverage](https://codecov.io/gh/Russell-Shean/powerbpy/branch/master/graph/badge.svg)](https://app.codecov.io/gh/Russell-Shean/powerbpy?branch=master)

           
# Features      
Currently the package has functions that let you do the following *without opening Power BI* 🥳: 
<!-- Because quarto and or github are dumb, we're using html instead of markdown for the bullet points -->
<ul>
           <li>Create a new dashboard</li>
           <li>Import data from</li>
           <ul>
                      <li>csv file stored locally</li>
                      <li>csv file stored in Azure Data Lake Storage (ADLS)</li>
                      <li>Power BI table stored as a Tabular Model Definition Language (TMDL) file</li>
           </ul>
           <li>Add a page</li>
           <li>Add background images to a page</li>
           <li>Add visuals to a page</li>
           <ul>
                      <li>charts</li>
                      <li>slicers</li>
                      <li>cards</li>
                      <li>maps</li>
                      <li>text boxes</li>
                      <li>buttons</li>
           </ul>
</ul>

## Dependencies    
Before you can start to build power BI dashboards using this package's functions you'll need the following:       
<ol>
           <li>Python (version 3.12 or higher!) and pip installed and on path</li>
           <li>Git installed and on path</li>
           <li>Power BI Desktop (You can create the dashboards without this, but not view them).</li>
</ol>             


Power BI settings:      
You'll need to enable some preview features in Power BI Desktop. Navigate to `File` > `Options and Settings` > `Options` > `Preview features` and enable the following options:         
<ol>
           <li>Shape map visual</li>
           <li>Power BI Project (.pbip) save option</li>
           <li>Store Semantic Model using TMDL format</li>
           <li>Store reports using enhanced metadata format (PBIR)</li>
</ol>



# Run the example
This example assumes you are on windows. All the code below should be entered in command prompt or put in a batch script.      

1. Create a new folder to store all the files you'll need.    
```dosbat
:: create a new folder
mkdir automatic_PBI_dashboards_example

:: move into the new folder
cd automatic_PBI_dashboards_example
```
2. Clone the files from github.    
```batchfile
git clone https://github.com/Russell-Shean/powerbpy
```
3. Activate venv.    
The following is taken from this <a href="https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/">tutorial</a>. We'll use venv to install the python package in an isolated environemnt.   
```batchfile
:: create a virtual environment
py -m venv .venv

:: activate the virtual environment
.venv\Scripts\activate

:: For extra credit, verify that venv is working
where python

```

4. Make sure pip is installed and up-to-date.    
Pip is the tool we'll use to install the package.  
```batchfile
:: install and/or upgrade pip
py -m pip install --upgrade pip

:: check version number (and confirm it's working)
py -m pip --version

```   
   
5. Install the package.      
This package isn't on pypi yet, so you'll need to install it from Github      
```batchfile
```dosbat     
py -m pip install git+https://github.com/Russell-Shean/powerbpy.git#egg=powerbpy     
```      

After the package is on pypi, you'll be able to install it using this: 
```batchfile
py -m pip install powerbpy
```     

6. Create the example dashboard.
Run an example script to generate an example dashboard.
```batchfile

py powerbpy/examples/create_example_dashboard.py

```     
    
7. Open the dashboard.      
Open the dashboard to confirm everything worked. 
```batchfile
start test_dashboard/test_dashboard.pbip
```

8. Refresh data models

After Power BI opens, you'll see a banner that looks like this:
![image](https://github.com/Russell-Shean/powerbpy/blob/main/docs/assets/images/refresh_warning.png?raw=true)      

Click `Refresh now`      

If everything worked you should have a dashboard that looks like this:     
![image](https://github.com/Russell-Shean/powerbpy/blob/main/docs/assets/images/page1.png?raw=true)         
        
![image](https://github.com/Russell-Shean/powerbpy/blob/main/docs/assets/images/page2.gif?raw=true)            
          
![image](https://github.com/Russell-Shean/powerbpy/blob/main/docs/assets/images/dataset_list.png?raw=true)       

# Next steps
The code used to generate the dashboard is stored <a href= "https://github.com/Russell-Shean/powerbpy/blob/main/examples/create_example_dashboard.py">here</a>         
Try building your own dashboards with these functions and let me know what happens!   

# Feedback    
I welcome the following feedback:            
<ol>
           <li>Pull requests to add features, add tests, fix bugs, or improve documentation. If the change is a major change create an issue first.</li>
           <li>Issues to suggest new features, report bugs, or tell me that the documentation is confusing 😅</li>
           <li>Power BI feature requests. I need help from Power BI developers who don't neccesarily have experience with python or github. I don't really know Power BI 😅, so please feel free to suggest new features. It would be really helpful if you could include a .pbix file that has the feature or even better a git diff of the dashboard before and after the change.(Use the .pbip format)</li>
           <!-- <li>Tests. I need some way to test DAX, M and TMDL for validity without using Power BI desktop. If you know of a tool I could use in Github Actions let me know!</li> -->
</ol>
<!--
# Big changes coming up:            
1. This package will be renamed as powerbpy and migrated to a different github and pypi location. The version will be reset to 0.1.0
2. I will add a step-by-step explanation/tutorial for the example dashboard
3. I will deploy to conda
4. I plan to convert the functions to classes and methods
5. I will add tests and input validation. I doubt this will do anything except prevent malformed dashboard files, but stricter input validation may break some edge case uses.
6. I will add functions to do the following:
    - Create a map with a dynamic legend
    - Add cards and slicers
    - list pages
-->


