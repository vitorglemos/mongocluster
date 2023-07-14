# Trabalho - Gerência de Grandes Volumes de Dados
## Passo 1 - Obteção dos Dados

Para obter os dados de ISRC e característica das músicas (track_name), foi realizado um script que se conecta a API do Spotify. Para facilitar o processo de testes, o arquivo de DB do Mongo foi adicionado ao drive: https://drive.google.com/file/d/1qH9cG0p04gfxtCo3vbphsFdzTzQaPA9h/view?usp=sharing

Todos os arquivos (scripts) utilizados para baixar os dados para realizar a demonstração no Mongo, é possível encontrar em: 
https://github.com/vitorglemos/mongocluster/tree/main/isrc-csv

## Passo 2 - Instalação do Ambiente Ubuntu

Para a criação das máquinas, foi utilizado o Virtual Box com 4 máquinas virtuais utilizando o Ubuntu. 
Neste link: https://github.com/vitorglemos/mongocluster/tree/main/mongo-cluster-scripts é possível encontrar os scripts utilizados para
a instalação do Mongo no ambiente de testes. 

Além disso, é necessário configurar os arquivos de /etc/mongod.conf, /etc/hostname e /etc/host para que cada máquina consiga se reconhecer na rede.
Para facilitar os testes, foram disponibilizados todos os arquivos de configuração utilizados em cada máquina: https://github.com/vitorglemos/mongocluster/tree/main/mongo-cluster-config

Os dados referentes as máquinas em replicação do Mongo podem ser conferidas no arquivo de rs_status:

https://github.com/vitorglemos/mongocluster/blob/main/rs_status

## Passo 3 - Importando a Base de Dados para o Mongo

O arquivo da collection no Mongo foi exportado e inserido no Drive mencionado acima no Passo 1 (já que o Github limita o envio de arquivos maiores do que 25MB):

Essa é uma versão resumida da base de dados, contendo um total de 1761 ISRCS para busca. Para import, é possivel utilizar o comando abaixo numa máquina primary node do MongoDB:
```shell
mongoimport --host 127.0.0.1 --port 27017 --username admin --password admin --authenticationDatabase admin -db spotify --collection Spotifyv3 --file SpotifyDBSmall.json
```
## Passo 3 - Scripts em Paralelo
Os scripts utilizados para alocar as máquinas em paralelo (via ssh) e executar as consultas em fragmento podem ser encontradas no link abaixo:
- **Para a máquina master** (Que aloca as máquinas): https://github.com/vitorglemos/mongocluster/blob/main/primary-node/parallel_mongo.py
  ```python
  python3 parallel_mongo.py 
  ```
Caso seja necessário trocar o nome dos nós ou realizar apenas o teste em um deles, é possível modifica-los no trecho :
 ```python
hostnames = ['config-server', 'worker-sl1', 'worker-sl2']
```
Neste array, é necessário colocar o nome das máquinas (hosts) para que o acesso via ssh seja feito. 

**Para as máquinas workers**, o script utilizado se encontra neste link: https://github.com/vitorglemos/mongocluster/tree/main/secondary-node

Caso não tenha uma credencial no Spotify para testar e enviar requests, é possivel substituir este comando no **parallel_mongo.py** do master:
- No lugar de:
 ```python
 command = f'python3 /home/your_user/script/request.py --inicio {inicio} --fim {fim} --genre 1'
 ```
- Use:
 ```python
 command = f'python3 /home/your_user/script/request.py --inicio {inicio} --fim {fim} --genre 0'
 ```
## Passo 4 - Resultado das Consultas

O resultado das consultas também pode ser conferido nesta pasta do Github: https://github.com/vitorglemos/mongocluster/tree/main/query-results
Esta pasta contém separadamente o que cada consulta retornou.

### O que são os arquivos nesta pasta?
- filter-q-worker-sl0.json: retorno do worker-sl0 para a consulta com filtro
- filter-q-worker-sl1.json: retorno do worker-sl1 para a consulta com filtro
- filter-q-worker-sl2.json: retorno do worker-sl2 para a consulta com filtro
- full-q-worker-sl0.json: retorno do worker-sl0 para a consulta sem filtro (retornar todos os dados)
- full-q-worker-sl1.json: retorno do worker-sl1 para a consulta sem filtro (retornar todos os dados)
- full-q-worker-sl2.json: retorno do worker-sl2 para a consulta sem filtro (retornar todos os dados)

É possível também ter um resumo dos dados retornados (filtrados por ISRCS) utilizados na apresentação: https://github.com/vitorglemos/mongocluster/blob/main/TABELA_EXCEL_55ISRCS.xlsx
