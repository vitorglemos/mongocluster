# Trabalho - Gerência de Grandes Volumes de Dados
## Passo 1 - Obteção dos Dados

Para obter os dados de ISRC e característica das músicas (track_name), foi realizado um script que se conecta a API do Spotify. Para facilitar o processo de testes, o arquivo de DB do Mongo foi adicionado ao drive: 

## Passo 2 - Instalação do Ambiente Ubuntu

Para a criação das máquinas, foi utilizado o Virtual Box com 4 máquinas virtuais utilizando o Ubuntu. 
Neste link: https://github.com/vitorglemos/mongocluster/tree/main/mongo-cluster-scripts é possível encontrar os scripts utilizados para
a instalação do Mongo no ambiente de testes. 

Além disso, é necessário configurar os arquivos de /etc/mongod.conf, /etc/hostname e /etc/host para que cada máquina consiga se reconhecer na rede.
Para facilitar os testes, foram disponibilizados todos os arquivos de configuração utilizados em cada máquina: https://github.com/vitorglemos/mongocluster/tree/main/mongo-cluster-config

## Passo 3 - Importando a Base de Dados para o Mongo

O arquivo da collection no Mongo foi exportado e inserido neste Drive (já que o Github limita o envio de arquivos maiores do que 25MB). Essa é uam versão resumida da base de dados, contendo um total de 1761 ISRCS para busca. Para import, é possivel utilizar o comando abaixo numa máquina primary node do MongoDB:
```shell
mongoimport --host 127.0.0.1 --port 27017 --username admin --password admin --authenticationDatabase admin -db spotify --collection Spotifyv2 --file mongoSpotify.json
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
