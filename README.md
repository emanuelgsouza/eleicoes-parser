# eleicoes-parser

Parser para leitura dos dados vindos do Repositório de Dados do TSE. O objetivo é ter ao final, arquivos CSV com os dados consolidados das seções e das zonas eleitorais.

## Como usar?

É recomendando que use este repositório com virtualenv, para que se isole os pacotes instalados aqui, dos do seu SO. Para tanto, é necessário executar os seguintes passos:

```sh
# substitua o caminho pelo do python3
virtualenv --python='/usr/bin/python3' .

# para ativar o ambiente virtual
source bin/activate

# o pip irá instalar os pacotes a partir do arquivo requirements.txt
pip install -r requirements.txt
```

Com os pacotes já instalados, entre na pasta parser e execute o arquivo cli.py

### Executando o arquivo cli.py

É imprescindível que, antes de executar o cli, exista na pasta `parser/data`, dois arquivos:

* Um referente ao Boletim de Urna do turno que quer analisar
* E outro referente ao Detalhe da Votação do Estado que quer analisar

#### Exemplo do Rio de Janeiro, município de Duque de Caxias.

1. Acesso a [página](http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1/repositorio-de-dados-eleitorais) do Repositório de Dados Eleitorais do TSE.
2. Acesso a página Resultados no menu
3. Seleciono o ano (referência 2016)
4. Faço o download do link 'Detalhe da apuração por seção eleitoral (formato ZIP)'
5. Depois faço o download do link interno da página 'Boletim de urna — Segundo turno'. Nesta página, há uma lista de links para cada Estado. Seleciono o do RJ
6. Extraio os arquivos baixados
7. Seleciono o boletim de urna do RJ e copio para a pasta `parser/data` do repositório
8. Seleciono o Estado do RJ na pasta resultante criada pela extração do arquivo de Detalhe da Apuração por seção eleitoral e copio para a pasta `parser/data` do repositório

Se você executar `python cli.py`, ele irá pegar as configurações padrão, que é analisar o município de Duque de Caxias (código 58335), e gerar dois arquivos que estarão na pasta `parser/dataset/`, um referente ao detalhe de votação por zona e o outro por seção.

#### Parâmetros para o cli.py

* `--municipio`: é o código do município de análise. Para saber o código, basta abrir qualquer um dos dois arquivos do TSE que foram baixados. O valor padrão é o código do município de Duque de Caxias/RJ.
* `--turno`: é o turno que se quer analisar os dados. O valor padrão é dois.
* `--secao_file`: é o nome do arquivo de seção que foi baixado do TSE.
* `--boletim_file`: é o nome do arquivo de boletim de urna.

É possível ter acesso as mesmas informações, digitando:

```sh
python cli.py --help
```
