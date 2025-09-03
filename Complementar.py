from pathlib import Path
from tkinter.filedialog import askopenfilenames

## ABRE O ARQUIVO ##
def abrir():
    filename = askopenfilenames()
    return filename

## COPIA O ARQUIVO QUE ESTÁ SENDO EDITADO PARA A PASTA DE RESULTADOS ##
def Copia(caminho,Novo_Metodo,inicio,Moleculas,nome):

    ## ESCREVE O ARQUIVO DE SAIDA ##
    with open(caminho + "Resultados/" + nome,"w") as outfile:
        outfile.write(Novo_Metodo)
        outfile.writelines("\n")
        outfile.write(inicio)
        outfile.writelines(Moleculas)
    ## ADICIONA O ARQUIVO NA LISTA PARA GERAR O EXECUTÁVEL ##
    return nome

## GERA O EXECUTAVEL PARA O ORCA ##
def Executavel(Arquivos_gerados,caminho):
    ## CAMINHO PARA O EXECUTAVEL QUE CHAMA O ORCA ##
    Executavel_Orca = Path(caminho + "Resultados/" + "Energias" + ".ps1")
    ## ESCREVE O ARQUIVO EXECUTÁVEL DO ORCA ##
    with open(Executavel_Orca,"w") as outfile:
        for i in Arquivos_gerados:
            out = i.removesuffix(".inp")
            outfile.write("C:\orca503\orca.exe " + i + " > " + out + ".out \n")
