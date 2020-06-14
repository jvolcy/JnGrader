import JnGrader

def main():
    
    notebookPath = 'Current-Course-Materials/assignments/D0113.02-dual-operand_math_1/D0113.02-dual-operand_math_1.ipynb'
    compareSources = False    #always a string
    compareOutputs = False
    outputType = float    #set to int, float or str (matters only if comparing outputs)
    expectedSources = ['Q1_Ans = 3', 'Q2_Ans = 3', 'Q3_Ans = 6', 'Q4_Ans = 1', 'Q5_Ans = 7', 'Q6_Ans = 2', 'Q7_Ans = 8', 'Q8_Ans = 3', 'Q9_Ans = 2', 'Q10_Ans = 6']
    expectedOutputs = []
    studentIDsFile = 'su2020StudentList.txt'

    studentGrades = JnGrader.grade( notebookPath = notebookPath,
                          compareSources = compareSources,
                          compareOutputs = compareOutputs,
                          outputType = outputType,
                          expectedSources = expectedSources,
                          expectedOutputs = expectedOutputs,
                          studentIDsFile = studentIDsFile)
    
            
main()
