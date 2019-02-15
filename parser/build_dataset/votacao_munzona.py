# -*- coding: utf-8 -*-

# import libraries
import pandas as pd

LABELS_TO_REMOVE = [
    'secao',
    'percentual_nominais',
    'percentual_brancos',
    'percentual_nulos',
    'percentual_legenda',
    'percentual_anulados',
    'percentual_abstencoes',
    'uf',
    'codigo_municipio'
]

def buildVotacaoZonaDataframe (df_detalhe_secao):
    columns = list(df_detalhe_secao.columns.values)
    codigo_municipio = df_detalhe_secao['codigo_municipio'][0].item()
    cols = list(filter(lambda item : item not in LABELS_TO_REMOVE, columns))
    df_filtered = df_detalhe_secao[cols].apply(pd.to_numeric)
    df = df_filtered.groupby('zona').sum().reset_index()
    df.insert(0, 'codigo_municipio', codigo_municipio)
    return df
