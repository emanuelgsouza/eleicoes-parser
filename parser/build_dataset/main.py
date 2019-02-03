# -*- coding: utf-8 -*-

from detalhe_votacao import buildVotacaoSecaoDataframe
from boletim_urna import buildBoletimUrnaDataframe

class FactoryDataframe:
    def __init__ (self, file, codMun, turno = 2):
        self.file = file
        self.cod_mun = codMun
        self.turno = turno
    
    def buildSecaoDataframe (self):
        return buildVotacaoSecaoDataframe(file=self.file, codMun=self.cod_mun, turno=self.turno)
    
    def buildBoletimUrnaDataframe (self):
        return buildBoletimUrnaDataframe(file=self.file, codMun=self.cod_mun, turno=self.turno)
