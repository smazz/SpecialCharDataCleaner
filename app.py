
from flask import Flask, render_template, request, redirect, make_response
import pandas as pd
import os
import re
import sys
import webbrowser


print('\n \n A browser window or tab should open that runs the web app. If it does not open after one minute, copy the URL below and paste it into your browser. (it should look something like http://127.0.0.1:5000/) \n')

base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)
app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))

#Loads the default home page
@app.route("/", methods=['GET'])
def home():
    global inchars
    inchars = 'Enter is the characters you would like replaced separated with a space (ie: "$ # , & !")'
    global InSkip
    InSkip = 'Enter the row # that the header is in: '
    
    return render_template("CleanCharsUI.html", InChars=inchars, InSkipRow =InSkip)

@app.route("/", methods=['POST', 'GET'])
def upload_file():
    FileName = request.files.get('file')
    #after a file is selected and the first form is submited it executes the below
    if FileName is not None:
        #get the row number of the header
        RowtoSkip = request.form.get('skiprow') 
        Rownum = int(RowtoSkip) - 1
        #make the df global and read in the file
        global df
        df = pd.read_csv(FileName, encoding='unicode escape', skiprows=Rownum)
        #We get the list of space delimited characters to replace & store them to print out later
        global CList
        CharList = request.form.get('Chars')   
        CList= list(CharList.split(' '))
        PrintChars = 'Charachters to Replace: ' + CharList
        global dg
        
    
        
        dg=df
        #We create a list of column headers which we will print out with check boxes for the user to select which columns to edit
        cols2 = dg.columns.tolist()
        #create a blank list to store the checked items later
        checked=[]
        #We get the selection from the radio input that decides whether we want to delete the characters or replace with _
        global ReplaceChar
        ReplaceChar = request.form.get('RepChar') 
        
        #We store the selected columns
        if request.method=="POST":
          
            for i in request.form.getlist('cols[]'):
                
                checked.append(i)
            return render_template("CleanCharsUI.html", cols=cols2, CPrint=PrintChars)
        elif request.method=="GET":
            
            return render_template("CleanCharsUI.html")
    else:
        
        #get the selected columns so we know which ones to edit
        lst = request.form.getlist("cols[]")
        
        global CountCharStr
        #printout list to tell the user what edits were made
        printout =[]

        #if the user the selects delete we replace with an empty string or else we replace with _ 
        if ReplaceChar == "Blank":
            for c in CList:
                
                for l in lst:
                    dgStr = dg[l].to_string()
                    ct= dgStr.count(c)
                    ctStr= str(ct)
                    
                    #count and store the output message to tell the user what was replaced in each column
                    CountCharStr = 'We replaced '+ctStr + ' of the Character '+ c+' in column '+l 
                    printout.append(CountCharStr)
                
                    dg[l]=dg[l].replace(c,"")
        else:
            
            for l in lst:
                for c in CList:
                    dgStr = dg[l].to_string()
                    ct= dgStr.count(c)
                    ctStr= str(ct)
                    #count and store the output message to tell the user what was replaced in each column
                    CountCharStr = 'We replaced '+ctStr + ' of the Character '+ c+' in column '+l 
                    printout.append(CountCharStr)
                #for fun, we use a lambda here instead to do the same as the delete function
                #option to use this instead dg[l]=dg[l].str.replace(c,"_")
                dg[l] = dg[l].apply(lambda x: "_" if (x in CList) else x) 
                          
        
            
        
        #no matter what all column headers are changed to replace non-alpha numeric characters to _
        for columns in dg:
            dg.columns = dg.columns.map(lambda x: re.sub(r'\W+', '_', x))
            
        #Outputs to user
        ColHeader = dg.columns.values
        ColStr = 'Your new column headers are:'
        NameFile = request.form.get('NameSave') 
        dg.to_csv(NameFile+'.csv', index=False)
        filename = app.root_path
        PrintFN = 'Your file has been cleansed and saved in following location: ' + filename+NameFile
        RStr = 'Replacements Made:'
    return render_template("CleanCharsUI.html", PrintOut=printout, colhead=ColHeader, colstr=ColStr, rstring = RStr, printFN=PrintFN, InChars=inchars, InSkipRow =InSkip)


if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True, use_reloader=False)