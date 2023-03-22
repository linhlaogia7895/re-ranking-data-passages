import pandas as pd


fileList = ["output-york07-ga-01.txt", "output-york07-ga-02.txt", "output-york07-ga-03.txt"]

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


print(mergedDf)