import JnGrader

def main():
    
    # baseHomeDir='/home', 
    notebookPath = 'Current-Course-Materials/assignments/Dxxx/Dxxx.ipynb'
    compareSources = False    #always a string
    compareOutputs = False
    outputType = str    #set to int, float or str (matters only if comparing outputs)
    # floatTolerancePct = 0.00001, #how far can answer deviate from expected value (0.01 = 1%)
    expectedSources = []
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
