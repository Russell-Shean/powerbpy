# Power Bpy <a id="hex-sticker" href="https://russell-shean.github.io/powerbpy/"><img src="https://github.com/user-attachments/assets/e372239d-5c28-4ed1-acf6-fb96a03b8a1a" align="right" height="240" /></a>  
Do you wish you could build dashboard with python or R, but can't because the client specifically asked for Power BI or your employer only supports publishing Power BI? Do you love love love Power BI, but wish there was a way to automatically generate parts of your dashboard to speed up your development process?      

Introducing Power Bpy, a python package that lets you create Power BI dashboards using python. Dashboards created using these functions can be opened, edited and saved normally in Power BI desktop. Power Bpy uses the new .pbip/.pbir format which stores dashboards as directories of text files instead of binary files letting you version control your dashboards!       

Still not convinced? See the [use cases](#use-cases) section below for more details about when you might use this package. 

[![pypi Version](https://img.shields.io/pypi/v/powerbpy.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/powerbpy/)
[![PyPI Downloads](https://static.pepy.tech/badge/powerbpy)](https://pepy.tech/projects/powerbpy)
[![Codecov test coverage](https://codecov.io/gh/Russell-Shean/powerbpy/branch/master/graph/badge.svg)](https://app.codecov.io/gh/Russell-Shean/powerbpy?branch=master)

           
## Features      
Currently the package has functions that let you do the following *without opening Power BI Desktop*: 
<ul>
           <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#create-a-new-dashboard">Create a new dashboard</a></li>
           <li>Import data from</li>
           <ul>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-dataset">csv file stored locally</a></li>
                      <li>csv file stored in Azure Data Lake Storage (ADLS)</li>
                      <li>Power BI table stored as a Tabular Model Definition Language (TMDL) file</li>
           </ul>
           <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-new-page">Add a page</a></li>
           <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-background-image">Add background images</a> to a page</li>
           <li>Add visuals to a page</li>
           <ul>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-button">buttons</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/reference/page._Page.html#powerbpy.page._Page.add_card">cards</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-chart">charts</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-choropleth-map">maps</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/reference/page._Page.html#powerbpy.page._Page.add_slicer">slicers</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/reference/page._Page.html#powerbpy.page._Page.add_table">tables</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-text-box">text boxes</a></li>
           </ul>    
           <li>Get information about your dashboard:</li>     
           <ul>      
                      <li><a href="https://www.russellshean.com/powerbpy/reference/dashboard.html#powerbpy.dashboard.Dashboard.list_pages">List pages</a> attached to a dashboard</li>
                      <li><a href="https://www.russellshean.com/powerbpy/reference/dashboard.html#powerbpy.dashboard.Dashboard.get_measures_list">List measures</a> attached to a dashboard</li>
                      <li>Load existing <a href="https://www.russellshean.com/powerbpy/reference/dashboard.html#powerbpy.dashboard.Dashboard.load_page">pages</a> or <a href="https://www.russellshean.com/powerbpy/reference/dashboard.html#powerbpy.dashboard.Dashboard.load">dashboards</a> into python so you can add pages,datasets, or visualizations</li></ul>
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


## Example Workflows      
- To see an intro example of how to create dashboards using the package, see the [test dashboard](https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html) tutorial.
- For more details about how to install python and run python scripts see the setup [tutorial](https://www.russellshean.com/powerbpy/basic_setup.html).
- To see more example dashboards and the scripts used to create them see the [example dashboards](https://www.russellshean.com/powerbpy/example_dashboards.html) section of the website. 

## Use Cases
<strong>Q: Why would I use a python package to create dashboards instead of just creating dashboards/visualizations using python tools such as flask?</strong>     
A: Many organizations only support certain tools for publishing. Power BI is often bundled with an organization's subscription to Microsoft. If your organization lets you use flask or build webpages directly with React, then this package probably won't be much use. If the only tool you are allowed to use to create and publish dashboards is Power BI, this package might help you build version controlled, reproducible and automated dashboard workflows using python instead of manually re-creating dashboards in Power BI desktop.         

<strong>Q: One of the reasons I like Power BI is because I don't have to write code to build dashboards. Why would I use this instead of Power BI desktop?</strong>        
A: You don't have to choose! Dashboards created with Power Bpy can be opened and edited normally in Power BI Desktop. Furthermore, Power BI isn't actually a no-code tool because you have to learn DAX and M. This package give you the option of using python, (a language many people find easy to learn and use), for both data preparation and building dashboards. You also don't have to be really good at python to use the functions in this package, see the [test dashboard](https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html) and [example dashboards](https://www.russellshean.com/powerbpy/example_dashboards.html) tutorials for examples of how easy it is to build dashboards with python! 

## Contributing   
I welcome the following feedback:            
<ol>
           <li>Pull requests to add features, add tests, fix bugs, or improve documentation. If the change is a major change create an issue first.</li>
           <li>Issues to suggest new features, report bugs, or tell me that the documentation is confusing.</li>
           <li>Power BI feature requests. I need help from Power BI developers who don't neccesarily have experience with python or github. It would be really helpful if you could include a .pbix file that has the feature or even better a git diff of the dashboard before and after the change. (Use the .pbip format)</li>
           <!-- <li>Tests. I need some way to test DAX, M and TMDL for validity without using Power BI desktop. If you know of a tool I could use in Github Actions let me know!</li> -->
</ol>


