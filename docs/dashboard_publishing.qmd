---
title: "Publish .pbir and .pbip dashboards"
format: html
---

# Background 
It is not currently possible to directly publish .pbir or .pbip dashboards directly to Power BI service like you can with .pbix files. According to Microsoft, if you have fabric enabled git workspaces, it should be possible to directly publish, but if you don't there is another workaround. This document describes that workaround. 

## Convert to .pbit      
The first step is to convert the .pbir or .pbip file to a Power BI template (.pbit) file.     
