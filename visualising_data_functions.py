# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 13:02:44 2017

@author: rcdenleybowers
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)


##functions to wrangle to cell population database:

##CONDITONEXTRACT = extracts dataframe for particular growth condition.

##CELLTYPEEXTRACT = extracts dataframe for particular cell type

##STATSARRAY = given an array, calculates the mean, sd and variance.

##PERCENTCHANGE = calculates the percent change between two instances

##CHANGEDISTRIBUTION = calculates percent change over two distributions

##POSITIONNUMBER = returns numerical value according to position on leaf: base = 0, mid = 1, tip = 2.

## LIGHTSTRING = returns string representing light intensity: 50 = 'low', 250 = 'high', anything else returns 'mid'

def conditionExtract(df, light, age, position=None):
    
    #find all unique leaf condition names in sheet
    UniqueNames = df.leafCondition.unique()
    #make dictionary of rows sorted by leaf condition into discrete dataframes
    DataFrameDict = {elem : pd.DataFrame for elem in UniqueNames}
    
    for key in DataFrameDict.keys():
        DataFrameDict[key] = df[:][df.leafCondition == key]
    
    #extract df that corresponds to age and light conditions specified above, then merge into one dataframe
    dataFrameArray = [0,0,0]

    for key in DataFrameDict.keys():
        if light in key and age in key:
            if 'base' in key:        
    
                df = DataFrameDict[key]   
                dataFrameArray[0] = df
                
            elif 'mid' in key:
                
                df = DataFrameDict[key]
                dataFrameArray[1]= df
                
            elif 'tip' in key:
    
                df = DataFrameDict[key]
                dataFrameArray[2] = df
            elif 'base' and 'mid' and 'tip' not in key:

                inputDf = DataFrameDict[key]   
 
    if age != 'young':
        if position is None:
            inputDf = pd.concat(dataFrameArray)
        else:
            inputDf = dataFrameArray[int(position)]
    
    return inputDf
    
def cellTypeExtract(inputDf, typeString):
    

    #find all unique leaf condition names in sheet
    UniqueNamesCell = inputDf.cellType.unique()
    #make dictionary of rows sorted by leaf condition into discrete dataframes
    DataFrameDictCell = {elem : pd.DataFrame for elem in UniqueNamesCell}
    
    for key in DataFrameDictCell.keys():
        DataFrameDictCell[key] = inputDf[:][inputDf.cellType == key]
    
    cellTypeDF = DataFrameDictCell[typeString]
    
    return cellTypeDF
    
def statsArray(array):
    meanGroup1 = np.mean(array)
    sdGroup1 = np.std(array)
    varGroup1 = np.var(array)
    
    statsVector1 = [meanGroup1, sdGroup1, varGroup1]
    
    return statsVector1
    
def percentChange(current, previous):
    if previous == 0:
        return 100.0
    elif current == previous:
        return 0.0
    else:    
        (abs((current - previous)/previous)*100.0)

        
def changeDistribution(df, conditions, cellTypes):
    #conditions is a 2d array- [[light1, light2],[age1, age2],[position1, position2]]

    light = conditions[0]
    age = conditions[1]
    position = conditions[2]
    if position[0] is None:
        inputdf = conditionExtract(df, light[0], age[0])
    else:     
        inputdf = conditionExtract(df, light[0], age[0], position[0])
        
    if position[1] is None:
        inputdf2 = conditionExtract(df, light[1], age[1])
    else:
        inputdf2 = conditionExtract(df, light[1], age[1], position[1])
        

    ## extract cell type 
    
    cellTypeDF = cellTypeExtract(inputdf, cellTypes[0])
    cellTypeDF2 = cellTypeExtract(inputdf2, cellTypes[1])
    
    cellTypeCount =  cellTypeDF['cellCount'].values
    cellTypeCount2 =  cellTypeDF2['cellCount'].values
    
    #Compare percentage change of celltype1 to celltype2
    
    comparisonArray = []
    
    for i in range(len(cellTypeCount)):
        change = percentChange(cellTypeCount2[i], cellTypeCount[i])
        comparisonArray.append(change)

    return comparisonArray

def populationString(index):
    if index == 0:
        popstring = 'base'
    elif index == 1:
        popstring = 'mid'
    elif index == 2:
        popstring = 'tip'
    else:
        print('\n\n popindex not valid \n\n' )
        popstring = 'ERROR'
    return popstring

def positionNumber(position, age= None):
    
    if age != None:
        if age == 'young':
            position_value = None
        else:
            if position == 'base':
                position_value = 0
            elif position == 'mid':
                position_value = 1
            elif position == 'tip':
                position_value = 2  
    else:
        if position == 'base':
            position_value = 0
        elif position == 'mid':
            position_value = 1
        elif position == 'tip':
            position_value = 2
            
    return position_value
    
def lightString(light):
    if light == np.int64(50):
        light_string = 'low'
    elif light == np.int64(250):
        light_string = 'high'
    else:
        light_string = 'mid'
    return light_string
    
def cellTypeCountExtract(df, condition0, cell_types, i):
    ##accepts two lists of the form [light0, age0, position0] and [light1, age1, position1]
    ##cell_types array
    ##cell types index

    lights = condition0[0]
    age = condition0[1]
    positions = condition0[2]
    
    comparison_frame1 = df.loc[(df['light'] == int(lights)) & (df['age'] == age) 
            & (df['position'] == positions) & (df['cellType'] == cell_types[i])]        
    
    cellTypeCount0 = comparison_frame1['cellCountMm2'].values

    
    return cellTypeCount0
    
def totalCellCount(df, conditions, cell_types):
    lights = conditions[0]
    age = conditions[1]
    positions = conditions[2]
    
    cellTypeList = []
    for i in range(len(cell_types)):
        comparison_frame1 = df.loc[(df['light'] == int(lights)) & (df['age'] == age) 
                & (df['position'] == positions) & (df['cellType'] == cell_types[i])]        
        
        cellTypeCount0 = comparison_frame1['cellCountMm2'].values
        cellTypeList.append(cellTypeCount0)
    totalCellCount = [sum(j[k] for j in cellTypeList) for k in range(len(cellTypeList[0]))]
    
    return totalCellCount