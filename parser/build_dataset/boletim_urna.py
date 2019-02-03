# -*- coding: utf-8 -*-

# import libraries
from parser_utils import parserFile, generateRegionDataset

LABELS = [
    'data',
    'hora',
    'codigo_pleito',
    'codigo_eleicao',
    'uf',
    'codigo_cargo',
    'descricao_cargo',
    'zona',
    'secao',
    'local_votacao',
    'numero_partido',
    'nome_partido',
    'codigo_municipio',
    'nome_municipio',
    'data_bu',
    'aptos',
    'abstencoes',
    'comparecimento',
    'tipo_eleicao',
    'tipo_urna',
    'descricao_urna',
    'numero_votavel',
    'nome_votavel',
    'votos',
    'codigo_tipo_votavel',
    'numero_urna',
    'codigo_urna_1',
    'codigo_urna_2',
    'data_carga',
    'codigo_flashcard',
    'cargo_pergunta_secao'
]

LABELS_TO_BUILD = [
    'uf',
    'codigo_municipio',
    'zona',
    'secao',
    'nome_votavel',
    'numero_votavel',
    'votos'
]

def buildBoletimUrnaDataframe (file, codMun, turno):
    dataLines = parserFile(file)
    df = generateRegionDataset(dataLines=dataLines, columns=LABELS, codMun=codMun, use_turn=False)
    df_filtered = df[LABELS_TO_BUILD][(df['nome_votavel'] != 'NULO') & (df['nome_votavel'] != 'BRANCO')]
    
    return df_filtered

def getConsolidateCandidates (df_boletim_urna):
    val = df_boletim_urna.to_dict(orient='index')
    items = val.values()
    dicts = []
    values = []
    
    for item in items:
        _val = list(filter(lambda x : x['secao'] == item['secao'] and x['zona'] == item['zona'], dicts))
        
        if len(_val) == 0:
            nome_votavel = item['nome_votavel']
            votos = item['votos']
            item[nome_votavel] = votos
            del item['nome_votavel']
            del item['votos']
            del item['numero_votavel']
            dicts.append(item)
        else:
            nome_votavel = item['nome_votavel']
            votos = item['votos']
            item[nome_votavel] = votos
            del item['nome_votavel']
            del item['votos']
            del item['numero_votavel']
            context = _val[0].copy()
            context.update(item)
            values.append(context)

    return values   

def insertCandidateInformation (df_secoes, df_candidates):
    _dict = df_secoes.to_dict(orient='index')
    _candidates = df_candidates.to_dict(orient='index').values()
    candidates = list(df_candidates.columns.values[0:2])

    values = []
    
    for item in _dict.values():
        _val = list(filter(lambda x : int(x['secao']) == int(item['secao']) and int(x['zona']) == int(item['zona']), _candidates))
        
        nome1 = candidates[0]
        nome2 = candidates[1]
        
        item[nome1] = _val[0][nome1]
        item[nome2] = _val[0][nome2]
        
        values.append(item)
    
    return values