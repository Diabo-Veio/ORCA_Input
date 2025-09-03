from INP import *
from PDB import *

## VARIAVEL GLOBAL PARA ARMAZENAR O NOME DOS ARQUIVOS ##
caminho = ""
## GLOBAL PARA DEFINIR O METODO E USAR NA EDIÇÃO E CÓPIA ##
Novo_Metodo = ""
## METODOS ##
Metodo_1 = '''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 22 end 
%maxcore 3000
%scf Guess Pmodel end'''
Metodo_2 = '''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 19 end 
%maxcore 3000
%scf Guess Pmodel end'''
Metodo_3 = '''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 22 end 
%maxcore 3000
%scf Guess Hueckel end'''
Metodo_4 = '''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 19 end 
%maxcore 3000
%scf Guess Hueckel end'''

def tipo(tipo_arquivo,Moleculas,nome_original,Numero_Atm,Metodo_escolhido,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram):
    global caminho
    caminho = ""

    ## DEFINE O METODO ##
    if Metodo_escolhido == 1:
        Metodo = Metodo_1
    elif Metodo_escolhido == 2:
        Metodo = Metodo_2
    elif Metodo_escolhido == 3:
        Metodo = Metodo_3
    elif Metodo_escolhido == 4:
        Metodo = Metodo_4
    
    ## EDITA O METODO PARA MODIFICAR OS NUCLEOS E RAM ##
    if(Alterar_Nucleos):
        Metodo = Metodo.replace(Metodo[72:74], Nucleos)
        if(Alterar_Ram):
            Metodo = Metodo.replace(Metodo[89:93], Ram)
    elif(Alterar_Ram):
        Metodo = Metodo.replace(Metodo[89:93], Ram)

    ## REMOVE O SUFIXO ##
    if tipo_arquivo == "pdb":
        nome = nome_original.removesuffix(".pdb")
    else:
        nome = nome_original.removesuffix(".inp")

    ## DEFINE O CAMINHO PARA O ARQUIVO ##
    res = nome.split("/", -1)
    nome_certo = res[-1] if len(res) > 1 else ""
    res.remove(nome_certo)
    for i in res:
        caminho += i + '/'

    ##VERIFICA SE JA EXISTE UMA PASTA DE RESULTADOS ##
    if not os.path.exists(caminho + "Resultados"):
        try:
            ## CRIA A PASTA DE RESULTADOS SE NÃO EXISTIR ##
            os.mkdir(os.path.dirname(caminho + "Resultados/"))
        except OSError as exc:
            ## CASO DE ALGUM ERRO ##
            if exc.errno != errno.EEXIST:
                raise

    ## VERIFICA SE O ARQUIVO É PDB ##
    if tipo_arquivo == "pdb":
        Pdb_Manipulacao_Inicial(caminho,nome_certo,Moleculas,Numero_Atm,Metodo)
    
    ## VERIFICA SE O ARQUIVO INP ESCOLHIDO É VALIDO (RECEM SAÍDO DO AVOGRADO) ##
    elif tipo_arquivo == "inp" and Moleculas[:73] == Metodo_original:
        Inp_Manipulacao_Inicial(caminho,nome_certo,Moleculas,Numero_Atm,Metodo)        
        return 0
    else:
        ## RETORNA 1 NA FUNÇÃO CASO O ARQUIVO SEJA INVALIDO PARA LEVANTARMOS UM ERRO NO INTERFACE.PY ##
        return 1
    