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
linhas_editadas = []

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## PEGA AS COORDENADAS DO PDB E CHAMA A EDIÇÃO PARA O ESTILO DO ORCA ##
def Pdb_Manipulacao_Inicial(caminho,nome_certo,Moleculas,Numero_Atm,Metodo):
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
    Pdb_Manipulacao(caminho,nome_completo,Linhas,Numero_Atm,Metodo)

def Pdb_Manipulacao(caminho,nome_completo,Linhas,Numero_Atm,Metodo):
    ## CONTADORES ##
    Atm = 0
    Molecula_Alvo = 0

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

    for i in coordenadas:
            linhas_editadas.append(f"   {elementos[coordenadas.index(i)]}     {i[0]:>10}     {i[1]:>10}     {i[2]:>10}\n")

    with open(caminho + "Resultados/" + nome_completo,"w") as outfile:
        outfile.write(Metodo)
        outfile.writelines("\n* xyz 0 1\n")
        for i in linhas_editadas:
            outfile.write(i)
        outfile.writelines("*\n")

    ## DEFINE O NUMERO DE MOLECULAS A VERIFICAR ##
    Numero_Mol = ((len(linhas_editadas))/Numero_Atm)

    ## CHAMA O METODO PARA EDITARMOS OS ARQUIVOS ##
    for i in range(int(Numero_Mol)):
        Molecula_Alvo += 1
        A_e_B(linhas_editadas,Numero_Atm,Metodo,caminho,nome_completo,Atm,Molecula_Alvo,alc[i])
    
    
def A_e_B (linhas_editadas,Numero_Atm,Metodo,caminho,nome_original,Atm,Molecula_Alvo,letra):

    ## LISTAS PARA INSERIRMOS AS LINHAS ##
    lista = []
    lista2 = []
    lista3 = []
    Molecula = 1

    nome = nome_original.removesuffix(".inp")
    nome_completo = nome + letra + ".inp"

    for linha in linhas_editadas:
        
        ## IDENTIFICA QUE CHEGAMOS NA PRÓXIMA MOLECULA ##
        if Atm == Numero_Atm :
            Molecula += 1
            Atm = 0

        ## ADICIONA A LINHA NA LISTA SE CHEGAMOS NA MOLECULA ALVO ##
        if Molecula == Molecula_Alvo:
            ## ADICIONA LINHA NA LISTA ##
            lista.append(linha)
            ## PASSA PARA O PRÓXIMO ÁTOMO ##
            Atm += 1
            ## VERIFICA SE ACABOU A MOLECULA, PASSA PARA A PROXIMA MOLECULA E ENCERRA O LOOP ##
            if Atm == Numero_Atm:
                Atm = 0
                Molecula += 1
                
        ## INICIA A EDIÇÃO SE NÃO ESTAMOS NA MOLECULA ALVO ##
        elif Molecula < Molecula_Alvo or Molecula > Molecula_Alvo:
            ## EDITA A LINHA DA MOLECULA##
            linha_rep = linha.replace(linha[3:5],linha[3]+":")
            ## ADICIONA A LINHA DA MOLECULA NA LISTA CORRETA ##
            if  Molecula < Molecula_Alvo:
                lista2.append(linha_rep)
            elif  Molecula > Molecula_Alvo:
                lista3.append(linha_rep)
            ## PASSA PARA O PRÓXIMO ÁTOMO ##
            Atm += 1   

    ## ESCREVE O ARQUIVO ##
    with open(caminho + "Resultados/" + nome_completo,"w") as outfile:
        outfile.write(Metodo)
        outfile.writelines("\n* xyz 0 1\n")
        outfile.writelines([str(i) for i in lista2])
        outfile.writelines([str(i) for i in lista])
        outfile.writelines([str(i) for i in lista3])
        outfile.writelines("*\n")
