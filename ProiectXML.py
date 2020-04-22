#!/usr/bin/env python
# coding: utf-8

# In[1]:


from xml.etree import ElementTree as ET
import json
import xmltodict
from tkinter import *
import easygui
import lxml.etree as ET


# In[2]:


from json2xml import json2xml
from json2xml.utils import readfromurl, readfromstring, readfromjson


# In[3]:


# global variables
inputXml =  ""
inputJson = ""
inputXsl = ""
resultXml = ""
resultJson = ""
resultHtml = ""


# In[4]:


# inserts the xml file into the program

def insertXML():
    global inputXml
    inputXml = easygui.fileopenbox()
    
    # check if the file has the extension ".xml"; if not, show a pop up error message
    if (inputXml[-4:len(inputXml)] != ".xml"):
        inputXml = ""
        errorWindow=Tk()
        errorWindow.title('Input ERROR')
        errorLabel=Label(errorWindow, text="Invalid XML Input!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("300x100+350+200")
        errorWindow.mainloop()
        return
    
    
    return


# In[5]:


# inserts the json file into the program

def insertJSON():
    global inputJson
    inputJson = easygui.fileopenbox()
    
    # check if the file has the extension ".json"; if not, show a pop up error message
    if (inputJson[-5:len(inputJson)] != ".json"):
        inputJson = ""
        errorWindow=Tk()
        errorWindow.title('Input ERROR')
        errorLabel=Label(errorWindow, text="Invalid JSON Input!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("300x100+350+200")
        errorWindow.mainloop()
        return
    
    
    return


# In[6]:


# converts the inserted xml into json

def convertToJSON():
    global inputXml
    global resultJson
    
    # check if there was inserted a xml file; if not, show a pop up error message
    if( not inputXml ):
        resultJson = ""
        errorWindow=Tk()
        errorWindow.title('Convert ERROR')
        errorLabel=Label(errorWindow, text="No XML to convert!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("300x100+350+200")
        errorWindow.mainloop()
        
        return
    
    # tries to convert the xml file into json; if the xml is not well formated it gives out an error message
    try:
        xmlRoot = ET.parse(inputXml).getroot()
        strXml = ET.tostring(xmlRoot , encoding = "UTF-8", method = "xml")
        jsonDict = xmltodict.parse(strXml)  
        resultJson = json.dumps(jsonDict, indent=4)
    except Exception as e:
        resultJson = ""
        errorWindow=Tk()
        errorWindow.title('Convert ERROR')
        errorLabel=Label(errorWindow, text="Bad file!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("200x100+350+200")
        errorWindow.mainloop()
        
    
    
    return


# In[7]:


# converts the inserted json into xml

def convertToXML():
    global inputJson
    global resultXml
    
    # check if there was inserted a json file; if not, show a pop up error message
    if( not inputJson ):
        resultXml = ""
        errorWindow=Tk()
        errorWindow.title('Convert ERROR')
        errorLabel=Label(errorWindow, text="No JSON to convert!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("300x100+350+200")
        errorWindow.mainloop()
    
        return
    

    # tries to convert the json file into xml; if the json is not well formated it gives out an error message
    
    with open(inputJson, 'r') as myfile:
        strJson = myfile.read()
    try:
        json_object = json.loads(strJson)
    except Exception as e:
        resultXml =""
        errorWindow=Tk()
        errorWindow.title('Convert ERROR')
        errorLabel=Label(errorWindow, text="Bad file!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("200x100+350+200")
        errorWindow.mainloop()
        return
        
    jsonData = readfromstring(strJson)
    xml = json2xml.Json2xml(jsonData).to_xml()
    resultXml = xml    
    
    return
    


# In[8]:


# opens a new window with the json conversion text

def previewJSON():
    
    global resultJson
    
    # check if there exists a json file that was generated using the app; if not, show a pop up error message
    if( not resultJson ):
        errorWindow=Tk()
        errorWindow.title('Preview ERROR')
        errorLabel=Label(errorWindow, text="No JSON to display!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("300x100+350+200")
        errorWindow.mainloop()
        return
    
    # preview of the new json in a new window
    windowPreviewJSON=Tk()
    textBoxJSON = Text(windowPreviewJSON, height=700, width=550) 
    windowPreviewJSON.title('JSON Preview')
    windowPreviewJSON.geometry("700x550+400+200")
    textBoxJSON.insert(END, resultJson)
    textBoxJSON.pack()
    windowPreviewJSON.mainloop()
    
    return


# In[9]:


# opens a new window with the xml conversion text

def previewXML():
    
    global resultXml
    
    # check if there exists a xml file that was generated using the app; if not, show a pop up error message
    if( not resultXml ):
        errorWindow=Tk()
        errorWindow.title('Preview ERROR')
        errorLabel=Label(errorWindow, text="No XML to display!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("300x100+350+200")
        errorWindow.mainloop()
        return
    
    # preview of the new xml in a new window
    windowPreviewXML=Tk()
    textBoxJXML = Text(windowPreviewXML, height=900, width=550)
    windowPreviewXML.title('XML Preview')
    windowPreviewXML.geometry("900x550+350+200")
    textBoxJXML.insert(END, resultXml)
    textBoxJXML.pack()
    windowPreviewXML.mainloop()
    
    return


# In[10]:


# downloads the json conversion into the same folder the input xml is in

def downloadJSON():
    global inputXml, resultJson
    
    # checks if there was a xml inserted and if there is a conversion of it; if not, show a pop up error message
    if(inputXml == "" or resultJson == ""):
        errorWindow=Tk()
        errorWindow.title('Download ERROR')
        errorLabel=Label(errorWindow, text="Please input and convert your XML to JSON!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("550x100+350+200")
        errorWindow.mainloop()
        return
    
    # writes the json
    inXML = inputXml
    inXML = inXML.replace(".xml","")
    with open(inXML+'ToJson.json', "w") as textFile:
        textFile.write(resultJson)
    textFile.close()
    
    return


# In[11]:


# downloads the xml conversion into the same folder the input json is in 

def downloadXML():
    
    global inputJson, resultXml
    
    # checks if there was a json inserted and if there is a conversion of it; if not, show a pop up error message
    if(inputJson == "" or resultXml == ""):
        errorWindow=Tk()
        errorWindow.title('Download ERROR')
        errorLabel=Label(errorWindow, text="Please input and convert your JSON to XML!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("550x100+350+200")
        errorWindow.mainloop()
        return
    
    # writes the xml
    inJson = inputJson
    inJson = inJson.replace(".json","")
    with open(inJson+'ToXml.xml', "w") as textFile:
        textFile.write(resultXml)
    textFile.close()
    
    return


# In[12]:


# inserts the xsl file into the program

def insertXSL():
    
    global inputXsl
    inputXsl = easygui.fileopenbox()
    
    # check if the file has the extension ".json"; if not, show a pop up error message
    if (inputXsl[-4:len(inputXsl)] != ".xsl"):
        inputXsl = ""
        errorWindow=Tk()
        errorWindow.title('Input ERROR')
        errorLabel=Label(errorWindow, text="Invalid XSL Input!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("300x100+350+200")
        errorWindow.mainloop()
        return
    
    return


# In[13]:


# downloads the HTML into the folder of the XML source

def downloadHTML():    
    
    # checks if there was a xml and a xsl inserted; if not, show a pop up error message
    if(inputXml == "" or inputXsl == ""):
        errorWindow=Tk()
        errorWindow.title('Download ERROR')
        errorLabel=Label(errorWindow, text="Please input both the XML and the XSL!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("550x100+350+200")
        errorWindow.mainloop()
        return
    
    # convert the XML using the XSL to HTML
    try: 
        dom = ET.parse(inputXml)
        xslFile = ET.parse(inputXsl)
        transform = ET.XSLT(xslFile)
        print(transform)
        newdom = transform(dom)
        print(newdom)
        resultHtml = (ET.tostring(newdom, pretty_print=True)).decode("UTF-8")
    except Exception as e:
        resultXml =""
        errorWindow=Tk()
        errorWindow.title('Convert ERROR')
        errorLabel=Label(errorWindow, text="XML or XSL is bad!", fg='red', font=("Helvetica", 16))
        errorLabel.place(x=60, y=50)
        errorWindow.geometry("300x100+350+200")
        errorWindow.mainloop()
        return
    
    # download the HTML
    inXml = inputXml
    inXml = inXml.replace(".xml","")
    with open(inXml+'ToHtml.html', "w") as textFile:
        textFile.write(resultHtml)
    textFile.close()
    
    return


# In[ ]:


# UI 

window=Tk()

# buttons
btn0 = Button(window, text="INSERT XML", fg='blue', font=("Helvetica", 16), command = insertXML)
btn0.place(x=30, y=100)

btn1 = Button(window, text="INSERT JSON", fg='blue', font=("Helvetica", 16), command = insertJSON)
btn1.place(x=25, y=200)

btn2 = Button(window, text="CONVERT TO JSON", fg='red', font=("Helvetica", 16), command = convertToJSON)
btn2.place(x=225, y=100)

btn3 = Button(window, text="CONVERT TO XML", fg='red', font=("Helvetica", 16), command = convertToXML)
btn3.place(x=230, y=200)

btn4 = Button(window, text="PREVIEW JSON", fg='orange', font=("Helvetica", 16), command = previewJSON)
btn4.place(x=500, y=100)

btn5 = Button(window, text="PREVIEW XML", fg='orange', font=("Helvetica", 16), command = previewXML)
btn5.place(x=505, y=200)

btn6 = Button(window, text="DOWNLOAD JSON", fg='green', font=("Helvetica", 16), command = downloadJSON)
btn6.place(x=120, y=300)

btn7 = Button(window, text="DOWNLOAD XML", fg='green', font=("Helvetica", 16), command = downloadXML)
btn7.place(x=370, y=300)

btn8 = Button(window, text="IMPORT XSL", fg='purple', font=("Helvetica", 16), command = insertXSL)
btn8.place(x=130, y=20)

btn9 = Button(window, text="DOWNLOAD HTML", fg='purple', font=("Helvetica", 16), command = downloadHTML)
btn9.place(x=370, y=20)

# window details
window.title('XML ~ JSON PARSER')
window.geometry("700x400+400+200")

window.mainloop()


# In[ ]:




