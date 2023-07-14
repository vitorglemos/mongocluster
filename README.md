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

O arquivo da collection no Mongo foi exportado e inserido neste Drive (já que o Github limita o envio de arquivos maiores do que 25MB). Essa é uam versão resumida da base de dados, contendo um total de 1761 ISRCS para busca. 
