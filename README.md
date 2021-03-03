# SpecialCharDataCleaner
*This is a resting Flask app that will remove problematic characters from data with different schemas*


This app is built for use on Windows and you can use PyInstaller
to create an EXE so it can function as rest app locally. 

The purpose of the app is to cleanse large data files of problematic characters
when the data may all have different data schemas. 

The app reads in csv files and allows the user to select which columns and special
character to delete or replace with an underscore.

It replaces all Non-Alpha numeric characters in the headers

Then is saves the cleansed file & creates an output outlining which special characters 
were removed or replaced & lists the new column headers.


**To make into an executable file install the latest version of PyInstaller and use the following:**

`PyInstaller  -F --icon=YourLogo.ico  --add-data "C:\Users\RESTOFPATH\;templates" app.py --name Your_Name`
