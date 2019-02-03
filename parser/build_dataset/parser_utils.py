# -*- coding: utf-8 -*-

import pandas as pd

# helper functions
removeSpaces = lambda string : string.strip()

removeQuotes = lambda line : str(line).replace('"', '')

def parserFile (file):
    dataLines = []
    for line in file:
        _line = removeQuotes(line)
        dataColumns = list(map(removeSpaces, _line.split(';')))
        dataColumns[0] = dataColumns[0].replace("b'", '')
        dataColumns[-1] = dataColumns[-1].replace("\\n'", '')
        dataLines.append(dataColumns)
    
    return dataLines

def generateDataset (dataLines, columns):
    return pd.DataFrame.from_records(dataLines, columns=columns)
    
def generateRegionDataset (dataLines, columns, codMun, turn = '2', use_turn = True):
    df = generateDataset(dataLines=dataLines, columns=columns)
    if turn and use_turn:
        return df[(df['codigo_municipio'] == codMun) & (df['turno'] == turn)]
    
    return df[df['codigo_municipio'] == codMun]

def parserFileToGenerate (file, codMun, turn):
    dataLines = []
    for line in file:
        _line = removeQuotes(line)
        dataColumns = list(map(removeSpaces, _line.split(';')))
        dataColumns[0] = dataColumns[0].replace("b'", '')
        dataColumns[-1] = dataColumns[-1].replace("\\n'", '')
        
        if dataColumns[3] == turn and dataColumns[7] == codMun:
            dataLines.append(dataColumns)
        
    return dataLines

def getNameInProp (prop):
    return list(prop.split('_'))[1]
