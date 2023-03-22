import pandas as pd

def evaluation(fileList):
    #x.evaluationPassage(fileList)
    #return fileList
    #for x in fileList:
        outputFormatData = pd.read_csv("/Data/output-york07-ga-01.txt", 
                              sep="\s+",
                              names= ["Topic#", "Document ID", "Passage Rank", "Okapi Score", "Byte Offset", "Passage Length", "Tag ID"])
        print(outputFormatData)