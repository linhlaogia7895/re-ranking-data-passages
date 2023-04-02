import pandas as pd
import numpy as np
import subprocess
def evaluation(fileList, selectedOption):
    if selectedOption == "Decision Tree":
        return decisionTree(fileList)
    elif selectedOption == "Knn":
        return knn(fileList)
    else:
        return meanScore(fileList)
    
def meanScore(fileList):
    dfs = []
    # Loop through each file and read it into a data frame
    for path in fileList:
        df = pd.read_csv("Data\\"+path, 
                                sep="\s+",
                                names= ["Topic#", "Document ID", "Passage Rank", "Okapi Score", "Byte Offset", "Passage Length", "Tag ID"])
        
        dfs.append(df)

    # Merge the data frames on the common columns
    mergedDf = dfs[0][["Topic#", "Document ID", "Okapi Score", "Byte Offset", "Passage Length", "Tag ID"]]
    for i in range(1, len(dfs)):
        mergedDf = pd.merge(mergedDf, dfs[i][["Topic#", "Document ID", "Okapi Score", "Byte Offset", "Passage Length", "Tag ID"]], on=["Topic#", "Document ID", "Byte Offset", "Passage Length"], how='outer')

    # Fill NaN values with 0
    mergedDf = mergedDf.fillna(0)

    #Method 1: rerank by calculate mean of three okapi score columns

    data1 = mergedDf.copy()
    data1["Average Okapi"] = data1[["Okapi Score_x", "Okapi Score_y", "Okapi Score"]].mean(axis=1).round(3)
    df = []
    for name, group in data1.groupby('Topic#'):
        top_1000 = group.sort_values(by='Average Okapi', ascending=False).head(n=1000)
        top_1000["new_rank"] = top_1000["Average Okapi"].rank(ascending=False).astype(int)
        df.append(top_1000)
    data1 = pd.concat(df)
    #print(data1)
    data1[["Topic#", "Document ID", "new_rank", "Average Okapi", "Byte Offset", "Passage Length", "Tag ID"]].to_csv('Export Data\\output-format-method-1.csv', index=False)
    data1[["Topic#", "Document ID", "new_rank", "Average Okapi", "Byte Offset", "Passage Length", "Tag ID"]].to_csv('Export Data\\output-format-method-1.txt', sep='\t', header=False, index=False)
    #return data
    #return data1[["Topic#", "Document ID", "new_rank", "Average Okapi", "Byte Offset", "Passage Length", "Tag ID"]]
    result = subprocess.run(['python', 'trecgen2007_score.py', 'gold-standard-07.txt', 'Export Data\\output-format-method-1.txt'], capture_output=True, text=True)
    return result.stdout

def decisionTree(fileList):
    return fileList

def knn(fileList):
    return fileList