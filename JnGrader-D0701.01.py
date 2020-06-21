import JnGrader

def main():
    
    # baseHomeDir='/home', 
    notebookPath = 'Current-Course-Materials/assignments/D0701.01-function_exercises_1/D0701.01-function_exercises_1.ipynb'
    compareSources = True    #always a string
    compareOutputs = False
    outputType = str    #set to int, float or str (matters only if comparing outputs)
    # floatTolerancePct = 0.00001, #how far can answer deviate from expected value (0.01 = 1%)
    expectedSources = ['Start\n-1\nEnd', '2', 'Hello\n-50\n150', 'Start\n20 20 5', '3',
                      'Peter\n9', 'Peter Rob\n5 3\n8\n-2', 'P+Q\n-63\n16\n4']
    expectedOutputs = []
    # studentIDsFile = 'idFile.txt'


    studentGrades = JnGrader.grade( 
                          # baseHomeDir = baseHomeDir,
                          notebookPath = notebookPath,
                          compareSources = compareSources,
                          compareOutputs = compareOutputs,
                          outputType = outputType,
                          # floatTolerancePct = floatTolerancePct,
                          expectedSources = expectedSources,
                          expectedOutputs = expectedOutputs,
                          # studentIDsFile = studentIDsFile
                            )

         
main()
