import os
import json
import sys


def splitLine(text, width):
    x = text.split('\n')
    if len(x[0]) <= width:
        #if len(x[0]) == 0:
        #    return x[0], ''
        return x[0], '\n'.join(x[1:])
    
    #here, no '\n' was found in the first width characters
    #search for the last space in the first <width> characters of the text.
    firstWidthChars = text[:width+1]
    lastSpaceLoc = firstWidthChars.rfind(' ')
    #if we don't find a ' ', break the line at location <width-1>
    if lastSpaceLoc == -1:
        return text[:width], text[width:]
    elif lastSpaceLoc == len(text)-1:
        return text[:lastSpaceLoc],None
    else:
        return text[:lastSpaceLoc], text[lastSpaceLoc+1:]


def column(text, width):
    '''this function formats the supplied text to fit into a column
of the specied width.'''
    outText = ''
    while len(text) > width:
        x = splitLine(text, width)
        outText += x[0] + '\n'
        text = x[1]
        #print(text)
    outText += text

    return outText


def makeColumns(texts, widths, separator='|'):
    output = ''
    textColumnsLists = []
    for index in range(len(texts)):
        textColumnsLists.append(column(texts[index], widths[index]).split('\n'))

    maxLines = 0
    for colList in textColumnsLists:
        if len(colList) > maxLines:
            maxLines = len(colList)

    for index in range(maxLines):
        line = ''
        for colListIndex in range(len(textColumnsLists)):
            if len(textColumnsLists[colListIndex]) > index:
                line += textColumnsLists[colListIndex][index]
                line += ' '*(widths[colListIndex] - len(textColumnsLists[colListIndex][index]))
            else:
                line += ' '*widths[colListIndex]
            #skip the trailing separator
            if colListIndex < len(widths)-1:
                line += separator   
        output += line + '\n'
    return output
            
            
            

#global dictionary to hold email->studet name dictionary
loginIDs = None

#this function creates a dictionary.  The keys are the student email addresses.
#The values are the student names.
def getStudentIDs(studentIDsFile):
    idFile = open(studentIDsFile, 'r')
    studentIDs = dict()
    for id in idFile:
        x = id.split(',')
        studentIDs[x[1].strip()] = x[0].strip()
    return studentIDs


#given a student's home directory, this function tries to identify the student.
def getStudentName(homeDirName):
    #skip the 'jupyter-' and use the next 16 chars
    homeDirBeginning = homeDirName[8:24]
    #print('-->',homeDirBeginning)
    for entry in loginIDs.keys():
        if entry.lower().startswith(homeDirBeginning):
            return loginIDs[entry]

        
        
def getStudentNamesAndDirs(homeDir):
    userDirs = []
    #get a list of all directories in the home dir
    dirEntries = os.listdir(homeDir)
    dirEntries.sort()
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
                    if 'outputs' not in cell:
                        output = 'AG: No Output'
                    elif cell['outputs'] == []:
                        output = 'AG: No Output'
                    elif cell['outputs'][0]['output_type'] == 'execute_result':
                        output = ''.join((cell['outputs'][0])['data']['text/plain'])
                    elif cell['outputs'][0]['output_type'] == 'stream':
                        output = ''.join((cell['outputs'][0])['text'])
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
                    sourceAndOutput.append((''.join(cell['source']), output))
                    
    return sourceAndOutput


'''
Function to grade notebooks.
baseHomeDir = the parent user directory.  This is the directory that contains the user home directories
notebookPath= the path within the user directory where the notebook under test can be found
compareSources = boolean.  Set to True to compare the source of the student solution cells
compareOutputs = boolean.  Set to True to compare the output of the student solution cells
# sourceType = 'string' or 'code'
outputType = str, float or int.  Specifies the expected output type.  Note that sources are always strings.
floatTolerancePct = how far answers can deviate from expected value (0.01 = 1%)
expectedSources = list of expected source values
expectedOutputs = list of expected output values
studentIDsFile = comma-seperated file containing student names and email addresses (the email address is assumed to be the Jupyter login)
'''
def grade(baseHomeDir='/home', 
          notebookPath='./', 
          compareSources = False, 
          compareOutputs = False, 
          outputType = str,
          floatTolerancePct = 0.00001, #how far can answer deviate from expected value (0.01 = 1%)
          expectedSources = [],
          expectedOutputs = [],
          studentIDsFile = 'idFile.txt'):

    #read the student ID information
    global loginIDs
    loginIDs = getStudentIDs(studentIDsFile)
    
    #assert that the length of source and outputs are the same if both are being tested
    if compareSources == True and compareOutputs == True and len(expectedSources) != len(expectedOutputs):
        print('** Warning ** : Number of expected outputs (',len(expectedOutputs), ') does not match the number of expected sources (', len(expectedSources), ').' )
              
    #adjust the # of questions to be graded by the # of comparisons we will be making
    NumQuestions = len(expectedSources) * (1 if compareSources == True else 0) + len(expectedOutputs) * (1 if compareOutputs == True else 0)
    studentNamesAndDirs = getStudentNamesAndDirs(baseHomeDir)

    grades = []    #list of names and grades
    
    
    for nameAndDir in studentNamesAndDirs:
        print('='*100)
        print(str(nameAndDir[0]).upper())
        studentNotebook = nameAndDir[1] + '/' + notebookPath
        #print (studentNotebook)
        sourceAndOutput = getNotebookSourceAndOutput(studentNotebook)
        print()
        #print(nameAndDir[0])
        i = 0
        grade = 0
        for item in sourceAndOutput:
            sourceStr = ''
            outputStr = ''

            #initialize 2 variables in case the student input does not match the expected values
            printedExpectedSource = ''
            printedExpectedOutput = ''
            
            if compareSources == True:   #are we comparing sources cells?
                try:
                    #try to compare items to the right of any = sign
                    #item[0] are sources
                    if item[0].split('=')[1] == expectedSources[i].split('=')[1]:
                        grade += 1
                        printedExpectedSource += 'ok\n'
                    else:
                        printedExpectedSource += '[Expected]\n' + expectedSources[i].split('=')[1] + '\n'
                except:
                    #just do a direct comparison
                    if item[0] == expectedSources[i]:
                        grade += 1
                        printedExpectedSource += 'ok\n'
                    else:
                        printedExpectedSource += '[Expected]\n' + expectedSources[i] + '\n'

                        
            if compareOutputs == True:    #are we comparing output cells?
                if outputType == int:     #integer outputs
                    try:
                        if int(item[1]) == int(expectedOutputs[i]):
                            grade += 1
                            printedExpectedOutput += 'ok\n'
                        else:
                            printedExpectedOutput += '[Expected]\n' + str(int(expectedOutputs[i])) + '\n'
                    except:
                        #print ('Could not convert to int:',  sys.exc_info()[0])
                        outputStr += 'Could not convert to int: ' + sys.exc_info()[0] + '\n'
                        
                elif outputType == float:    #float outputs
                    try:
                        expectedValue = float(expectedOutputs[i])
                        actualValue = float(item[1])
                        err = abs((expectedValue - actualValue)/expectedValue)
                        
                        if err < floatTolerancePct:
                            printedExpectedOutput += 'ok\n'
                            grade += 1
                        else:
                            printedExpectedOutput += '[Expected]\n' + str(float(expectedOutputs[i])) + '\n'

                    except:
                        #print ('Could not convert to float:',  sys.exc_info()[0])
                        outputStr += 'Could not convert to float: ' + sys.exc_info()[0] + '\n'
                        
                else:    #string outputs
                    if item[1] == expectedOutputs[i]:
                        printedExpectedOutput += '\n'
                        grade += 1
                        printedExpectedOutput += 'ok\n'
                    else:
                        printedExpectedOutput += '[Expected]\n' + expectedOutputs[i] + '\n'

#def makeColumns(texts, widths, separator='|'):

            sourceStr += '[source ' + str(i) + ']\n'   
            sourceStr += item[0] + '\n'
        
            outputStr += '[output ' + str(i) + ']\n'
            outputStr += item[1] + '\n'
            
            i += 1

            x = makeColumns([sourceStr, printedExpectedSource, outputStr, printedExpectedOutput], [30, 30, 30, 30])
            print(x, end='')
        
        if NumQuestions == 0:
            grades.append(str(nameAndDir[0]) + ' : ')
        else:
            grades.append(str(nameAndDir[0]) + ' : ' + str(grade) + '/' + str(NumQuestions) + ' = ' + str(100*grade/NumQuestions))
        print(grades[-1])  #print the last grades[] entry
        print() 

    #print a summary
    print()
    grades.sort()
    for grade in grades:
        print(grade)

    return (grades)

'''       
def main():
        #=============== Start Problem Specs ===============
    notebookPath = 'Current-Course-Materials/assignments/D0113.02-dual-operand_math_1/D0113.02-dual-operand_math_1.ipynb'
    compareSources = False    #always a string
    compareOutputs = False
    outputType = float    #set to int, float or str (matters only if comparing outputs)
    expectedSources = ['Q1_Ans = 3', 'Q2_Ans = 3', 'Q3_Ans = 6', 'Q4_Ans = 1', 'Q5_Ans = 7', 'Q6_Ans = 2', 'Q7_Ans = 8', 'Q8_Ans = 3', 'Q9_Ans = 2', 'Q10_Ans = 6']
    expectedOutputs = []
    studentIDsFile = 'su2020StudentList.txt'

    studentGrades = grade( notebookPath = notebookPath,
                          compareSources = compareSources,
                          compareOutputs = compareOutputs,
                          outputType = outputType,
                          expectedSources = expectedSources,
                          expectedOutputs = expectedOutputs,
                          studentIDsFile = studentIDsFile)
    
    
main()
'''