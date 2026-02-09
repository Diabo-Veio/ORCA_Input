import tkinter as tk
from tkinter import PhotoImage
from Escolha import *
from tkinter.ttk import *
from tkinter import messagebox
import sys
import os

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## GAMBIARRA PARA PEGAR O CAMINHO ABSOLUTO DA IMAGEM E ADICIONAR O .EXE (funciona no pyinstaller)##
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

class App(tk.Tk):
    
    # __init__ function for class tkinterApp 
    def __init__(self):
        tk.Tk.__init__(self)
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
        self.n = 0

        self.Parametro = tk.IntVar(value=0)
        self.Metodo = tk.IntVar(value=0)
        self.Alterar_Nucleos = tk.BooleanVar(value=False)
        self.Alterar_Ram = tk.BooleanVar(value=False)

        self.Numero_Atm = ""
        self.arquivos = []
        self.caminho = ""

        self.bloco_central = []
        self.hipoteses = []
        #-----------------------------------------------------------------------------------#
        #-----------------------------------------------------------------------------------#
        ## BOTÃO PARA ESCOLHER O ARQUIVO ##
        self.button1 = tk.Button(self,text="selecionar arquivos", command= lambda:self.Escolher_Arquivo())
        self.button1.grid(column=0,row=self.n,columnspan=2)
        self.n+=1

        ## SEPARADOR PARA ORGANIZAR ##
        self.separator1 = Separator(self, orient="horizontal")
        self.separator1.grid(column=0,row=self.n,sticky='ew',columnspan=2)
        self.n+=1

        #-----------------------------------------------------------------------------------#
        #-----------------------------------------------------------------------------------#
        ## BOTÃO PARA DEFINIR O NUMERO DE ÁTOMOS ##
        tk.Radiobutton(self, text="Número de átomos", variable= self.Parametro,value=1, command=lambda:self.Alt_Parametro()).grid(column=0,row=self.n,columnspan=2)
        self.n+=1
        ## ETIQUETA PARA IDENTIFICAR O CAMPO DE DIGITAÇÃO ##
        self.label1 = tk.Label(self,text="Número de átomos")
        ## CAMPO PARA DIGITAR O NUMERO DE ATOMOS ##
        self.entrada1 = tk.Entry(self)
        self.entrada1A = tk.Entry(self)
        ## BOTÃO PARA DEFINIR O NUMERO DE MOLECULAS ##
        tk.Radiobutton(self, text="Número de moléculas", variable= self.Parametro,value=2, command=lambda:self.Alt_Parametro()).grid(column=0,row=self.n,columnspan=2)
        self.n+=1
        ## ETIQUETA PARA IDENTIFICAR O CAMPO DE DIGITAÇÃO ##
        self.label2 = tk.Label(self,text="Número de moléculas")
        ## CAMPO PARA DIGITAR O NUMERO DE ATOMOS ##
        self.entrada2 = tk.Entry(self)
        self.entrada2A = tk.Entry(self)

        #-----------------------------------------------------------------------------------#
        #-----------------------------------------------------------------------------------#
    
        tk.Label(self,text="Dimeros").grid(column=0,row=self.n)
        tk.Label(self,text="Bloco Central").grid(column=1,row=self.n)
        self.n+=1
        ## VARIAVEIS COM OS ITENS DAS LISTAS ##
        self.list_bloco_central = tk.Variable()
        self.list_hipoteses= tk.Variable()
        ## LISTAS PARA DEFINIR O BLOCO CENTRAL ##
        self.bc = tk.Listbox(self,listvariable=self.list_bloco_central,selectmode=tk.MULTIPLE)
        self.hip = tk.Listbox(self,listvariable=self.list_hipoteses,selectmode=tk.MULTIPLE)
        ## iMPRIME AS LISTAS NA TELA ##
        self.bc.grid(column=0,row=self.n)
        self.hip.grid(column=1,row=self.n)
        self.n+=1
        ## BOTÕES PARA TROCAR DE LISTA ##
        tk.Button(self,text="⇨",command=lambda:self.trocar("bc")).grid(column=0,row=self.n,sticky='ew')
        tk.Button(self,text="⇦",command=lambda:self.trocar("hip")).grid(column=1,row=self.n,sticky='ew')
        self.n1=self.n+1
        self.n+=3

        ## SEPARADOR PARA ORGANIZAR ##
        self.separator1 = Separator(self, orient="horizontal")
        self.separator1.grid(column=0,row=self.n,sticky='ew',columnspan=2)
        self.n+=1
        #-----------------------------------------------------------------------------------#
        #-----------------------------------------------------------------------------------#
        ## BOTÕES PARA ESCOLHA DO METODO ##
        tk.Radiobutton(self, text="Dimero Sem Iodo", variable= self.Metodo,value=1).grid(column=0,row=self.n,columnspan=2)
        self.n+=1
        tk.Radiobutton(self, text="Cluster Sem Iodo", variable= self.Metodo,value=2).grid(column=0,row=self.n,columnspan=2)
        self.n+=1
        tk.Radiobutton(self, text="Dimero com Iodo", variable= self.Metodo,value=3).grid(column=0,row=self.n,columnspan=2)
        self.n+=1
        tk.Radiobutton(self, text="Cluster com Iodo", variable= self.Metodo,value=4).grid(column=0,row=self.n,columnspan=2)
        self.n+=1
        ## SEPARADOR PARA ORGANIZAR ##
        self.separator2 = Separator(self, orient="horizontal")
        self.separator2.grid(column=0,row=self.n,sticky='ew',columnspan=2)
        self.n+=1
        #-----------------------------------------------------------------------------------#
        #-----------------------------------------------------------------------------------#

        ## BOTÃO PARA ALTERAR O NUMERO DE NÚCLEOS ##
        tk.Checkbutton(self,text="Alterar número de nucleos", variable = self.Alterar_Nucleos,command=lambda:self.Alt_Nucleos()).grid(column=0,row=self.n,columnspan=2)
        self.entrada3 = tk.Entry(self)
        self.n2=self.n+1
        self.n+=2

        ## BOTÃO PARA ALTERAR A RAM ##
        tk.Checkbutton(self,text="Alterar memória ram", variable = self.Alterar_Ram,command=lambda:self.Alt_Ram()).grid(column=0,row=self.n,columnspan=2)
        self.entrada4 = tk.Entry(self)
        
        self.n+=2

        ## BOTÃO GERAR OS OUTPUTS ##
        self.button2 = tk.Button(self,text="Gerar arquivos", command= lambda:self.Gerar()).grid(column=0,row=self.n,columnspan=2)
        self.n+=1

    def trocar(self,lista):
        if lista == "bc":
            self.selected_indices = self.bc.curselection()

            for i in self.selected_indices:
                self.hipoteses.append(self.bc.get(i))
                self.bloco_central.remove(self.bc.get(i))

            self.list_hipoteses.set(self.hipoteses)
            self.list_bloco_central.set(self.bloco_central)

        if lista == "hip":
            self.selected_indices = self.hip.curselection()

            for i in self.selected_indices:
                self.bloco_central.append(self.hip.get(i))
                self.hipoteses.remove(self.hip.get(i))
            self.list_bloco_central.set(self.bloco_central)
            self.list_hipoteses.set(self.hipoteses)

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#
    def Alt_Parametro(self):
        if(self.Parametro.get() == 1):
            self.label2.grid_forget()
            self.entrada2.grid_forget()

            self.label1.grid(column=0,row=self.n1,columnspan=2)
            self.entrada1.grid(column=0,row=self.n1)
            self.entrada1A.grid(column=1,row=self.n1)

        if(self.Parametro.get() == 2):
            self.label1.grid_forget() 
            self.entrada1.grid_forget()

            self.label2.grid(column=0,row=self.n1,columnspan=2)
            self.entrada2.grid(column=0,row=self.n1)
            self.entrada2A.grid(column=1,row=self.n1)

    ## MOSTRA/ESCONDE CAMPO PARA MUDANÇA DE NÚCLEOS ##
    def Alt_Nucleos(self):
        if(self.Alterar_Nucleos.get()):
            self.entrada3.grid(column=0,row=self.n2,columnspan=2)
        else:
            self.entrada3.grid_forget()

    ## MOSTRA/ESCONDE CAMPO PARA MUDANÇA DE RAM ##
    def Alt_Ram(self):
        if(self.Alterar_Ram.get()):
            self.entrada4.grid(column=0,row=self.n2+2,columnspan=2)
        else:
            self.entrada4.grid_forget()

    ## METODO PARA CHAMAR A EDIÇÃO DE STRINGS ##
    def Escolher_Arquivo(self):

        self.arquivos = abrir()
        nome = ""
        for molecula in self.arquivos:
            nome = molecula.split("/", -1)
            nome_certo = nome[-1] if len(nome) > 1 else ""
            nome.remove(nome_certo)
            self.bloco_central.append(nome_certo)
        
        self.list_bloco_central.set(self.bloco_central)
        
        for i in nome:
                self.caminho += i + '/'


    ## METODO PARA CHAMAR A EDIÇÃO DE STRINGS ##
    def Gerar(self):

        if(self.Parametro.get() == 1):
            ## LÊ O NUMERO DE ATOMOS
            self.Numero_Atm = self.entrada1.get()
            self.Numero_Atm2 = self.entrada1A.get()
        elif(self.Parametro.get() == 2):
            ## LÊ O NUMERO DE MOLECULAS
            self.Numero_Atm = self.entrada2.get()
            self.Numero_Atm2 = self.entrada2A.get()

        if self.arquivos != []:
            ## ZERA AS VARIAVEIS PARA ATRIBUIR NOVOS VALORES ##
            self.Nucleos = 0
            self.Ram = 0
            ## DEFINE O NUMERO DE NÚCLEOS E MEMÓRIA RAM ##
            if(self.Alterar_Nucleos):
                self.Nucleos = self.entrada3.get()
            if(self.Alterar_Ram):
                self.Ram = self.entrada4.get()

            i = 0
            ## CHAMA O METODO UM VEZ POR ARQUIVO ##
            for arquivo in self.bloco_central:
                
                ## LÊ O CAMINHO PARA O ARQUIVOS ##
                f = open(self.caminho+arquivo)
                ## LÊ O CONTEUDO DO ARQUIVO EM QUESTÃO ##
                Molecula = f.read()
                if(arquivo.endswith(".inp")):
                    ## CHAMA O METODO PARA EDIÇÃO DAS LINHAS ##
                    a = tipo("inp",Molecula,arquivo,int(self.Numero_Atm),self.Parametro.get(),self.Metodo.get(),self.Alterar_Nucleos.get(),self.Nucleos,self.Alterar_Ram.get(),self.Ram,self.caminho)
                    ## CHAMA O ERRO SE O ARQUIVO SELECIONADO NÃO FOR VALIDO ##
                    if a == 1:
                        messagebox.showerror(title="Erro",message="Selecione o arquivo correto")
                elif(arquivo.endswith(".pdb")):
                    tipo("pdb",Molecula,arquivo,int(self.Numero_Atm),self.Parametro.get(),self.Metodo.get(),self.Alterar_Nucleos.get(),self.Nucleos,self.Alterar_Ram.get(),self.Ram,self.caminho)
            
            
            for arquivo in self.hipoteses:
                ## LÊ O CAMINHO PARA O ARQUIVOS ##
                f = open(self.caminho+arquivo)
                ## LÊ O CONTEUDO DO ARQUIVO EM QUESTÃO ##
                Molecula = f.read()
                if(arquivo.endswith(".inp")):
                    ## CHAMA O METODO PARA EDIÇÃO DAS LINHAS ##
                    a = tipo("inp",Molecula,arquivo,int(self.Numero_Atm2),self.Parametro.get(),self.Metodo.get(),self.Alterar_Nucleos.get(),self.Nucleos,self.Alterar_Ram.get(),self.Ram,self.caminho)
                    ## CHAMA O ERRO SE O ARQUIVO SELECIONADO NÃO FOR VALIDO ##
                    if a == 1:
                        messagebox.showerror(title="Erro",message="Selecione o arquivo correto")
                elif(arquivo.endswith(".pdb")):
                    tipo("pdb",Molecula,arquivo,int(self.Numero_Atm2),self.Parametro.get(),self.Metodo.get(),self.Alterar_Nucleos.get(),self.Nucleos,self.Alterar_Ram.get(),self.Ram,self.caminho)
    
        else: Nova_Aba()

## ERRO DO FAUSTÃO ##
class Nova_Aba():
    def __init__(self):
        self.abrir()
    def abrir(self):
        ## ABRE NOVA ABA ##
        self.new_window = tk.Toplevel()
        self.new_window.title("INFORMAÇÕES INCOMPLETAS")
        self.new_window.geometry("253x275") 
        ## ABRE A IMAGEM E MUDA O TAMANHO ##
        self.image_orig = PhotoImage(file=resource_path("erro.png"))
        self.image = self.image_orig.subsample(2, 2)
        ## COLOCA A IMAGEM NA TELA ##
        self.image_label = tk.Label(self.new_window, image=self.image)
        self.image_label.grid(column=0,row=0,sticky="W")
        self.image_label.image = self.image
        self.label = tk.Label(self.new_window,text="Arquivos ou Nº de Átomos Faltando")
        self.label.grid(column=0,row=1)

## INICIA O LOOP DA INSTANCIA DO TKINTER ##

app = App()
app.title("Pontuador")
app.mainloop()
