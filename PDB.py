from io import StringIO
from string import ascii_uppercase as alc
from pathlib import Path
import os
import errno
import re

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## VARIAVEL GLOBAL PARA ARMAZENAR O NOME DOS ARQUIVOS ##
Arquivos_gerados = []
coordenadas = []
elementos = []

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## PEGA AS COORDENADAS DO PDB E CHAMA A EDIÇÃO PARA O ESTILO DO ORCA ##
def Pdb_Manipulacao_Inicial(caminho,nome_certo,Moleculas,Numero_Atm,Metodo,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram):
    ## LÊ O PDB ##
    Texto = StringIO(Moleculas)
    ## LISTA PARA EDIÇÃO ##
    Linhas = []

    ## LÊ TODAS AS LINHAS E PEGA AS QUE TEM AS COORDENADAS ## 
    while True:
        linha = Texto.readline()
        if linha[0:3] == "HET":
            Linhas.append(linha)
        if linha[0:3] == "CON":
            break

    ## CRIA NOME DO ARQUIVO ##
    nome_completo = nome_certo + ".inp"
    
    ## CHAMA A EDIÇÃO PARA PADRONIZAR NO ESTILO DO ORCA ##
    Pdb_Manipulacao(caminho,nome_completo,Linhas,Metodo)

def Pdb_Manipulacao(caminho,nome_completo,Linhas,Metodo):

    for linha in Linhas:
        correto = []
        regiao_coordenadas = linha[32:56]
        temp = re.findall(r"[-+\s]?(?:\d*\.*\d+)", regiao_coordenadas)
        elemento = linha[77:78]
        elementos.append(elemento)
        for i in temp:
            a = i + "00"
            correto.append(a)
        coordenadas.append(correto)

    with open(caminho + "Resultados/" + nome_completo,"w") as outfile:
        outfile.write(Metodo)
        outfile.writelines("\n* xyz 0 1\n")
        for i in coordenadas:
            outfile.write(f"   {elementos[coordenadas.index(i)]}     {i[0]:>10}     {i[1]:>10}     {i[2]:>10}\n")
        outfile.writelines("*\n")
    
