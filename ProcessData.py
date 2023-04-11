import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.mixture import GaussianMixture
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import subprocess
def evaluation(fileList, selectedOption):
    substrings = [element[-6:-4] for element in fileList]
    string = '-'.join(substrings)
    option = selectedOption
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


    if selectedOption == "EM Algorithm":
        return EMAlgorithm(mergedDf, string, option)
    elif selectedOption == "K-mean":
        return knn(mergedDf, string, option)
    else:
        return meanScore(mergedDf, string, option) 
   
def meanScore(mergedDf, string, option):
    #Method 1: rerank by calculate mean of three okapi score columns using defaul 0 for missing values
    data1 = mergedDf.copy()
    data1 = data1.fillna(0)
    return output(data1, string, option)

def knn(mergedDf, string, option):
    data2 = mergedDf.copy()
    #impute missing values using KNN

    columns = ["Okapi Score_x", "Okapi Score_y", "Okapi Score"]

    # nomalize the scores (0-1)
    scaler = MinMaxScaler()
    scaledScores = scaler.fit_transform(data2[columns])

    # Impute missing data using kNN
    imputer = KNNImputer(n_neighbors=3, weights='uniform')
    imputed_scores = imputer.fit_transform(scaledScores)

    rescaledScores = scaler.inverse_transform(imputed_scores)
    data2[columns] = rescaledScores
    return output(data2, string, option)

def EMAlgorithm(mergedDf, string, option):
    data3 = mergedDf.copy()

    #Fill the missing data using the IterativeImputer
    imputer = IterativeImputer(random_state=42)
    data3[["Okapi Score_x", "Okapi Score_y", "Okapi Score"]] = imputer.fit_transform(data3[["Okapi Score_x", "Okapi Score_y", "Okapi Score"]])
    data3["Average"] = data3[["Okapi Score_x", "Okapi Score_y", "Okapi Score"]].mean(axis=1)
    
    selected_passages = []

    for _ in range(1000):
        gmm = GaussianMixture(n_components=10, random_state=42)
        data3['Cluster'] = gmm.fit_predict(data3[["Okapi Score_x", "Okapi Score_y", "Okapi Score"]])
        
        picked_passages = data3.loc[data3.groupby('Topic#')['Cluster'].idxmin()]
        selected_passages.append(picked_passages)
        
        # Remove picked passages from the data
        data3 = data3.drop(picked_passages.index)
        
    newData =  pd.concat(selected_passages)
    #Use Gaussian Mixture Model (GMM)
    # gmm = GaussianMixture(n_components=10, random_state=42)
    # data3["Cluster"] = gmm.fit_predict(data3[["Average"]])

    #rerank data
    newData["Rank"] = newData.groupby("Topic#").cumcount() + 1
    newData = newData.sort_values(by=["Topic#", "Rank"], ascending=[True, True])
    # top_1000 = data3.groupby("Topic#").head(1000)
    
    newData[["Topic#", "Document ID", "Rank", "Average", "Byte Offset", "Passage Length", "Tag ID"]].to_csv("Export Data\\output-format-"+string+"-"+option+".csv", index=False)
    newData[["Topic#", "Document ID", "Rank", "Average", "Byte Offset", "Passage Length", "Tag ID"]].to_csv("Export Data\\output-format-"+string+"-"+option+".txt", sep='\t', header=False, index=False)
    #return data
    #return data1[["Topic#", "Document ID", "new_rank", "Average Okapi", "Byte Offset", "Passage Length", "Tag ID"]]
    result = subprocess.run(['python', 'trecgen2007_score.py', 'gold-standard-07.txt', 'Export Data\\output-format-'+string+'-'+option+'.txt'], capture_output=True, text=True)
    return result.stdout

def output(data, string, option):
    data["Average Okapi"] = data[["Okapi Score_x", "Okapi Score_y", "Okapi Score"]].mean(axis=1).round(3)
    df = []
    for name, group in data.groupby('Topic#'):
        top_1000 = group.sort_values(by='Average Okapi', ascending=False).head(n=1000)
        top_1000["new_rank"] = top_1000["Average Okapi"].rank(ascending=False).astype(int)
        df.append(top_1000)
    data = pd.concat(df)
    #print(data1)
    data[["Topic#", "Document ID", "new_rank", "Average Okapi", "Byte Offset", "Passage Length", "Tag ID"]].to_csv("Export Data\\output-format-"+string+"-"+option+".csv", index=False)
    data[["Topic#", "Document ID", "new_rank", "Average Okapi", "Byte Offset", "Passage Length", "Tag ID"]].to_csv("Export Data\\output-format-"+string+"-"+option+".txt", sep='\t', header=False, index=False)
    #return data
    #return data1[["Topic#", "Document ID", "new_rank", "Average Okapi", "Byte Offset", "Passage Length", "Tag ID"]]
    result = subprocess.run(['python', 'trecgen2007_score.py', 'gold-standard-07.txt', 'Export Data\\output-format-'+string+'-'+option+'.txt'], capture_output=True, text=True)
    return result.stdout
