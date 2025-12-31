# Power Bpy <a id="hex-sticker" href="https://russell-shean.github.io/powerbpy/"><img src="https://github.com/user-attachments/assets/e372239d-5c28-4ed1-acf6-fb96a03b8a1a" align="right" height="240" /></a>  
Do you wish you could build dashboards with code, but can't because the client specifically asked for Power BI or your employer only supports publishing Power BI? Do you love Power BI, but wish there was a way to automatically generate parts of your dashboard to speed up your development process?      

Introducing Power Bpy, a python package that lets you create Power BI dashboards using python. Dashboards created using these functions can be opened, edited and saved normally in Power BI desktop. Power Bpy uses the new .pbip/.pbir format which stores dashboards as directories of text files instead of binary files letting you version control your dashboards!       

Not immediately convinced?        
See some [example dashboards](https://www.russellshean.com/powerbpy/example_dashboards.html) or the [use cases](#use-cases) section below for more details about when you might use this package. 

[![pypi Version](https://img.shields.io/pypi/v/powerbpy.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/powerbpy/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/powerbpy?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/powerbpy)
[![Codecov test coverage](https://codecov.io/gh/Russell-Shean/powerbpy/branch/master/graph/badge.svg)](https://app.codecov.io/gh/Russell-Shean/powerbpy?branch=main)

           
## Features      
Currently the package has functions that let you do the following *without opening Power BI Desktop*: 
<ul>
           <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#create-a-new-dashboard">Create new dashboards</a></li>
           <li>Import data from:</li>
           <ul>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-dataset">Csv files</a> stored locally</li>
                      <li><a href="https://www.russellshean.com/powerbpy/reference/dashboard.Dashboard.html#powerbpy.dashboard.Dashboard.add_blob_csv">Csv files</a> stored in Azure Data Lake Storage (ADLS)</li>
                      <li><a href="https://www.russellshean.com/powerbpy/reference/dashboard.Dashboard.html#powerbpy.dashboard.Dashboard.add_tmdl">Datasets</a> stored as a Tabular Model Definition Language (TMDL) file</li>
           </ul>
           <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-new-page">Add new pages</a></li>
           <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-background-image">Add background images</a> to a page</li>
           <li>Add visuals to a page:</li>
           <ul>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-button">Buttons</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/reference/page._Page.html#powerbpy.page._Page.add_card">Cards</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-chart">Charts</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-choropleth-map">Maps</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/reference/page._Page.html#powerbpy.page._Page.add_slicer">Slicers</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-table">Tables</a></li>
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#add-a-text-box">Text boxes</a></li>
           </ul>    
           <li>Get information about your dashboard:</li>     
           <ul>      
                      <li><a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#list-all-the-dashboards-pages">List pages</a> attached to a dashboard</li>
                      <li><a href="https://www.russellshean.com/powerbpy/reference/dashboard.html#powerbpy.dashboard.Dashboard.get_measures_list">List measures</a> attached to a dashboard</li>
                      <li>Load existing <a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#load-an-existing-page">pages</a> or <a href="https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html#load-an-existing-dashboard">dashboards</a> into python so you can add pages, datasets, or visualizations</li></ul>
</ul>

## Dependencies    
Before you can start to build power BI dashboards using this package's functions you'll need the following:       
<ol>
           <li>Python 3.10+</li>
           <li>Power BI Desktop (You can create the dashboards without this, but not view them).</li>
</ol>             


Power BI settings:      
You'll need to enable some preview features in Power BI Desktop. Navigate to `File` > `Options and Settings` > `Options` > `Preview features` and enable the following options:         
<ol>
           <li>Power BI Project (.pbip) save option</li>
           <li>Store Semantic Model using TMDL format</li>
           <li>Store reports using enhanced metadata format (PBIR)</li>
</ol>     

## Example Workflows      
- For more details about how to install python and run python scripts, see the setup [tutorial](https://www.russellshean.com/powerbpy/basic_setup.html).       
- To see an intro example of how to create dashboards using the package, see the [test dashboard](https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html) tutorial.      
- To see more example dashboards and the scripts used to create them, see the [example dashboards](https://www.russellshean.com/powerbpy/example_dashboards.html) section of the website. 

## Publishing
The .pbip and .pbir formats can be tricky to publish to Power BI Service. See this [guide](https://www.russellshean.com/powerbpy/dashboard_publishing.html) for potential workarounds that let you continue publishing. 

## Use Cases
<strong>Q: Why would I use a python package to create dashboards instead of just creating dashboards/visualizations using python tools such as flask?</strong>     
     
A: Many organizations only support certain tools for publishing. Power BI is often bundled with an organization's subscription to Microsoft. If your organization lets you use flask or react or whatever else, then this package probably won't be much use. If the only tool you are allowed to use to create and publish dashboards is Power BI, this package might help you build version controlled, reproducible and automated dashboard workflows using python instead of manually re-creating dashboards in Power BI desktop.         

<strong>Q: I like Power BI because I don't have to write code to build dashboards. Why would I use this instead of Power BI Desktop?</strong>        
     
A: You don't have to choose! Dashboards created with Power Bpy can be opened and edited normally in Power BI Desktop. You can use code when it makes sense and point-and-click tools when it doesn't.       
    
Additionally, Power BI isn't actually a no-code tool because you have to learn DAX and M. This package give you the additional option of using python, (a language many people find easy to learn and use), for both data preparation and building dashboards.       
   
You also don't have to be really good at python to use the functions in this package, see the [test dashboard](https://www.russellshean.com/powerbpy/example_dashboards/Test%20Dashboard/Testing%20Dashboard.html) and [example dashboards](https://www.russellshean.com/powerbpy/example_dashboards.html) tutorials for examples of how easy it is to build dashboards with python! 

## Contributing   
I welcome various types of feedback:            
<ol>
           <li>Pull requests to add features, fix bugs, add tests, or improve documentation. If the change is a major change, create an issue first.</li><br>
           <li>Issues to suggest new features, report bugs, or tell me that the documentation is confusing.</li><br>
           <li>Power BI feature requests. I need help from Power BI developers who don't necessarily have experience with python or github, but who do know what Power BI features they'd like to see.<br><br>If possible it would be really helpful to show the change you want you by including a .pbix file that has the feature,  or even better, before and after commits to GitHub of the dashboard showing the change. (Use the .pbip or .pbir format for the Github commits).</li>

</ol>

## Sponsorship
Power Bpy is free and open-source, however if you found the package useful or inspiring, feel free to [sponsor](https://github.com/sponsors/Russell-Shean) the project so that I can keep building it out. Additionally, I am a freelance software developer; if you would like to hire me to build out a custom Power Bpy workflow for your organization, please feel free to reach out to me on [Linkedin](https://www.linkedin.com/in/russell-shean/) or [Bluesky](https://bsky.app/profile/rshean.bsky.social). 
