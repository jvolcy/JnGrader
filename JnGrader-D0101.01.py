import os
import json
import sys

loginIDs = {"agraves7@scmail.spelman.edu":"Ahmari Graves",
"aprice17@scmail.spelman.edu":"Aaliyah Price",
"bsmith83@scmail.spelman.edu":"Bradleigh Smith",
"kgrimste@scmail.spelman.edu":"Kiara Grimstead",
"kkirkla6@scmail.spelman.edu":"KaJalene Kirkland",
"mbarne21@scmail.spelman.edu":"Meyah Barnes",
"ttuckerc@scmail.spelman.edu":"Taja Tucker-Cooper",
"ltaylo38@scmail.spelman.edu":"Lauren Taylor",
"ccorbin2@scmail.spelman.edu":"Camryn Corbin",
"dedmonds1@spelman.edu":"Denver Edmonds",
"iherrin1@scmail.spelman.edu":"Imani Herring",
"Jyemonja@scmail.spelman.edu":"Jabari Yemonja-Olukun",
"nlowman@scmail.spelman.edu":"Niyah Lowman",
"sricha34@scmail.spelman.edu":"Shelby Richardson",
"acash4@scmail.spelman.edu":"Amari Cash",
"ahayne16@scmail.spelman.edu":"Adia Haynes",
"aricha59@scmail.spelman.edu":"Adrianna Richardson",
"gevans1@scmail.spelman.edu":"Gabrielle Evans",
"jjack135@scmail.spelman.edu":"Jaden Jackson",
"kfulton2@scmail.spelman.edu":"Kelsi Fulton",
"eojeda@scmail.spelman.edu":"Erin Ojeda",
"irelandbattle@gmail.com":"Ireland Battle",
"mblasing@scmail.spelman.edu":"Maya Blasingame",
"adanie29@scmail.spelman.edu":"Aniah Daniels",
"ahall40@scmail.spelman.edu":"Ashley Hall",
"cheywar2@scmail.spelman.edu":"Cheyenne Heyward",
"dahniellemilton@gmail.com":"Dahnielle Milton",
"dlittle3@scmail.spelman.edu":"DeAira Little",
"tfolsom@scmail.spelman.edu":"Tiandra Folsom",
"lanijeah.smith@scmail.spelman.edu":"LaNijeah Smith",
"mstewa21@scmail.spelman.edu":"Mone't Stewart",
"naisuan@scmail.spelman.edu":"Nadley Aisuan",
"plabranc@scmail.spelman.edu":"Phalyn LaBranche",
"sapatira@scmail.spelman.edu":"Suliah Apatira",
"sholme23@scmail.spelman.edu":"Starr Holmes",
"awoodar8@scmail.spelman.edu":"Asja Woodard",
"jholla10@scmail.spelman.edu":"Jada Holland",
"krobbin1@scmail.spelman.edu":"Kennedy Robbins",
"ksutton5@scmail.spelman.edu":"Kailyn Sutton",
"lhoard@scmail.spelman.edu":"Lauryn Hoard",
"msaulsbu@scmail.spelman.edu":"Maya Saulsbury",
"ajennin8@scmail.spelman.edu":"Aaliyah Jennings",
"alang3@scmail.spelman.edu":"Ayannah Lang",
"bfindley@scmail.spelman.edu":"Brionna Findley",
"creeder2@scmail.spelman.edu":"Christian Reeder",
"dsmit116@scmail.spelman.edu":"Deâ€™Ja Smith",
"idiggs@scmail.spelman.edu":"Imani Diggs",
"lwhite33@scmail.spelman.edu":"Layla White"
}


def getStudentName(homeDirName):
    #skip the 'jupyter-' and use the next 16 chars
    homeDirBeginning = homeDirName[8:24]
    #print('-->',homeDirBeginning)
    for entry in loginIDs.keys():
        if entry.startswith(homeDirBeginning):
            return loginIDs[entry]
        
        
def getStudentNamesAndDirs(homeDir):
    userDirs = []
    #get a list of all directories in the home dir
    dirEntries = os.listdir(homeDir)
    for dirEntry in dirEntries:
        entryPath = homeDir+'/'+dirEntry
        if os.path.isdir(entryPath):
            name = getStudentName(dirEntry)
            userDirs.append((name, entryPath))

    return userDirs

def getNotebookSourceAndOutput(noteBookPath):
    try:
        #load the notebook file
        fp = open(noteBookPath, 'r')
        notebook = json.load(fp)
        fp.close()
    except:
        print('AG Error:', sys.exc_info()[0])
        return []

    sourceAndOutput = []
    
    #the notebook is a dictionary.  keys include 'cells', 'metadata', 'nbformat', 'nbformat_minor', ...
    #we want the 'cells'
    cells = notebook['cells']

    #the cells is a list of dictionaries.  Go through each cell in the list
    for cell in cells:
        #Each dictionary has keys like 'cell_type', 'execution_count', 'metadata', 'outputs', 'source'...
        #we are interested in cells with a 'metadata' entry.
        if 'metadata' in cell:
            #The metadata is a dictionary.  We are looking for a 'ds4all' entry
            if 'ds4all' in cell['metadata']:
                #ds4all is a dictionary.  We are looking for a 'type' set to 'studentSolution'
                if cell['metadata']['ds4all']['type'] == 'studentSolution':
                    #print(cell)
                    if cell['outputs'] == []:
                        output = 'AG: No Output'
                    elif cell['outputs'][0]['output_type'] == 'execute_result':
                        output = ('\n'.join((cell['outputs'][0])['data']['text/plain']))
                    elif cell['outputs'][0]['output_type'] == 'error':
                        output = (cell['outputs'][0]['ename'])
                    else:
                        output = 'AG: Unkonwn Output'
                    
                    #print('***', cell['source'])
                    #print('***', output)
                    #print the joined items in the cell's source
                    #print('[source]', '\n'.join(cell['source']))
                    #print the joined items in the cell's outputs
                    #print('[outputs]', '\n'.join((cell['outputs'][0])['data']['text/plain']))
                    #print('[outputs]', output)
                    #print()
                    sourceAndOutput.append(('\n'.join(cell['source']), output))
                    
    return sourceAndOutput


def main():
    #specify the location of the home directories
    HOME_DIRS = '/home'
    D0101_01_expectedOutputs = ['47.18181818181818', '2194324.4545454546', '0.5', '0.005950963947465129', '3.8531269947891365']

    expectedOutput = D0101_01_expectedOutputs

    studentNamesAndDirs = getStudentNamesAndDirs(HOME_DIRS)

    NOTEBOOK_PATH = 'Current-Course-Materials/assignments/D0101.01-math_expressions_1/D0101.01-math_expressions_1.ipynb'
    for nameAndDir in studentNamesAndDirs:
        #print(nameAndDir[0])
        studentNotebook = nameAndDir[1]+'/'+NOTEBOOK_PATH
        #print (studentNotebook)
        sourceAndOutput = getNotebookSourceAndOutput(studentNotebook)
        print()
        #print(nameAndDir[0])
        i = 0
        grade = 0
        for item in sourceAndOutput:
            print('[source',i,']', item[0])
            print('[output',i,']', item[1])
            if item[1] == expectedOutput[i]:
                grade += 1
            i += 1
            print()

        print('-->', nameAndDir[0], ':', 100*grade/len(expectedOutput))
        print('-----------------------------------------')

        
main()
