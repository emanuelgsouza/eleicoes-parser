# -*- coding: utf-8 -*-

import sys
sys.path.append('./build_dataset')

import os
from shutil import copy2
import pandas as pd
import click

from build_dataset.main import FactoryDataframe
from build_dataset.detalhe_votacao import addPercentualColumns
from build_dataset.votacao_munzona import buildVotacaoZonaDataframe
from build_dataset.boletim_urna import getConsolidateCandidates, insertCandidateInformation
from constants import *


columns_to_remove_on_candidate_df = [
    'codigo_municipio',
    'secao',
    'uf',
    'zona'
]


class ParserCli:
    def __init__(
        self,
        municipio=DC_CODE,
        turno=TURNO,
        secao_file=SECAO_FILE,
        boletim_file=BOLETIM_FILE
    ):
        self.csv_name = None
        self.municipio = municipio
        self.turno = turno
        self.secao_file = secao_file
        self.boletim_file = boletim_file
        
    def getCSVName(self, prop):
        return "{}_{}.csv".format(prop, self.getDistrictName())
    
    def getDistrictName (self):
        return self.municipio
    
    def getDataframeSecao(self):
        df_secao = None

        path = 'data/{}'.format(self.secao_file)
        with open(path, mode='rb') as file:
            _FactoryDataframe = FactoryDataframe(
                file=file,
                codMun=self.municipio,
                turno=self.turno
            )

            df_secao = _FactoryDataframe.buildSecaoDataframe()
        
        df = addPercentualColumns(df_secao)

        return df
    
    def getDataframeBoletimUrna (self):
        df = None

        path = 'data/{}'.format(self.boletim_file)
        with open(path, mode='rb') as file:
            _FactoryDataframe = FactoryDataframe(
                file=file,
                codMun=self.municipio,
                turno=self.turno
            )

            df = _FactoryDataframe.buildBoletimUrnaDataframe()
        
        return df

    def getDataframeByZona (self, df):
        return buildVotacaoZonaDataframe(df_detalhe_secao=df)

    def saveDataframe(self, df, prop):
        csv_name = self.getCSVName(prop)
        df.to_csv('dataset/{}'.format(csv_name), index=False)
        return df
    
    def getCandidateSecoesinformation (self):
        df_secoes = self.getDataframeSecao()
        _boletimUrna = self.getDataframeBoletimUrna()
        _candidates = getConsolidateCandidates(_boletimUrna)
        df_candidates = pd.DataFrame(_candidates)
        # removing unnecessary columns
        candidate_columns = list(
            filter(
                lambda column: column not in columns_to_remove_on_candidate_df, df_candidates.columns
            )
        )

        consolidatedInformation = insertCandidateInformation(
            df_secoes=df_secoes,
            df_candidates=df_candidates
        )

        return pd.DataFrame(
            consolidatedInformation,
            columns=COLUMNS_TO_DETALHE_SECAO + candidate_columns
        )
    
    def run (self):
        print('Generate initial informations')
        df = self.getCandidateSecoesinformation()
        df_zona = self.getDataframeByZona(df=df)

        print('Save detalhe_votacao_secao')
        self.saveDataframe(df, DETALHE_FILE_NAME)

        print('Save votacao_by_zona')
        self.saveDataframe(df_zona, MUNZONA_FILE_NAME)

@click.command()
@click.option('--municipio', default=DC_CODE, help='A municipio para uso')
@click.option('--turno', default=TURNO, help='Turno que será analisado')
@click.option('--secao_file', default=SECAO_FILE, help='Nome do arquivo do detalhe de votação por seção')
@click.option('--boletim_file', default=BOLETIM_FILE, help='Nome do arquivo do do boletim de urna')
def main(municipio, turno, secao_file, boletim_file):
   cli = ParserCli(
       municipio=municipio,
       turno=turno,
       secao_file=secao_file,
       boletim_file=boletim_file
    )

   cli.run()

if __name__ == '__main__':
   main()
