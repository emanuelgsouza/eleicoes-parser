# -*- coding: utf-8 -*-

# import libraries

from parser_utils import parserFile, generateRegionDataset, getNameInProp
import pandas as pd

LABELS = [
    'data',
    'hora',
    'ano',
    'turno',
    'descricao',
    'uf',
    'ue',
    'codigo_municipio',
    'nome_municipio',
    'zona',
    'secao',
    'codigo_cargo',
    'cargo',
    'aptos',
    'comparecimento',
    'abstencoes',
    'votos_nominais',
    'votos_brancos',
    'votos_nulos',
    'votos_legenda',
    'votos_anulados'
]

LABELS_TO_BUILD = [
    'uf',
    'codigo_municipio',
    'zona',
    'secao',
    'aptos',
    'votos_nominais',
    'votos_brancos',
    'votos_nulos',
    'votos_legenda',
    'votos_anulados',
    'abstencoes'
]

LABELS_TO_NUMERIC = [
    'codigo_municipio',
    'zona',
    'secao',
    'aptos',
    'votos_nominais',
    'votos_brancos',
    'votos_nulos',
    'votos_legenda',
    'votos_anulados',
    'abstencoes'
]

LABELS_TO_PERCENTUAL = [
    'votos_nominais',
    'votos_brancos',
    'votos_nulos',
    'votos_legenda',
    'votos_anulados'
]

def buildVotacaoSecaoDataframe (file, codMun, turno):
    dataLines = parserFile(file)
    df = generateRegionDataset(dataLines=dataLines, columns=LABELS, codMun=codMun, turn=turno)
    processedDf = df[LABELS_TO_BUILD]
    processedDf = processedDf[LABELS_TO_NUMERIC].apply(pd.to_numeric)
    processedDf['nao_considerados'] = processedDf['aptos'] - processedDf['votos_nominais']
    return processedDf

def insertProp (df, prop, name):
    percent_label = 'percentual_{}'.format(name)
    df[percent_label] = df[prop] / df['aptos']
    df[percent_label] = df[percent_label].round(2)
    return df

def addPercentualColumns (df):
    for prop in LABELS_TO_PERCENTUAL:
        df = insertProp(df, prop, getNameInProp(prop))
    
    df = insertProp(df, 'abstencoes', 'abstencoes')
    return df