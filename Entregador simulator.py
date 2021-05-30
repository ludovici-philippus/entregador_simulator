import tkinter.ttk
from tkinter import *
from functools import partial

#Variáveis
janela = Tk()
dinheiro = DoubleVar()
fome = 0
sede = 0
sono = 0
trabalho = DoubleVar()
trabalhadores = 1
entregas_da_vez = 0

JANELA = "800x600"

dinheiro.set(200)

# Funções
def resete_label():
    # Reseta todos os textos em labels.
    lb_dinheiro["text"] = f"R$ {dinheiro.get()}"
    lb_trabalhadores["text"] = f"Trabalhadores: {trabalhadores}"
    lb_fome["text"] = f"Fome: {fome}"
    lb_sede["text"] = f"Sede: {sede}"
    lb_sono["text"] = f"Sono: {sono}"
    barra_entregas["maximum"] = entregas_da_vez/trabalhadores


def morrer(causa):
    # Mata o jogador.
    morreu_de_sono = Toplevel()
    morreu_de_sono.title(f"Você morreu de {causa}.")
    Label(morreu_de_sono, font=72, text=f"Você morreu de {causa} :(").pack()
    janela.after(3000, lambda: janela.destroy())

def checar_morte():
    # Verifica se o jogador morreu.
    if sono >= 100:
        morrer("sono")
    
    elif fome >= 100:
        morrer("fome")
    
    elif sede >= 100:
        morrer("sede")
    
    elif dinheiro.get() <= 0:
        morrer("falido")


def trabalhar(entregas):
    # Bota o jogador pra trabalhar.
    global fome, sede, sono, entregas_da_vez
    if entregas_da_vez != entregas:
        trabalho.set(0)
    entregas_da_vez = entregas
    resete_label()
    if trabalho.get() >= int(entregas / trabalhadores):
        if trabalhadores > 1:
            dinheiro.set(dinheiro.get() - 20 * (trabalhadores - 1))
        dinheiro.set(dinheiro.get() + (2.50 * entregas))

        sono += int(35 * (entregas / 20) / trabalhadores)
        fome += int(15 * (entregas / 30) / trabalhadores)
        sede += int(20 * (entregas / 30) / trabalhadores)

        checar_morte()

        trabalho.set(0)
        janela.update()
        resete_label()
    else:
        trabalho.set(trabalho.get() + 1)
        janela.update()

def contratar():
    # Faz o jogador mover a economia contratando mais trabalhadores.
    global trabalhadores
    if dinheiro.get() > 150:
        dinheiro.set(dinheiro.get() - 150)
        trabalhadores += 1
        janela.update()
        resete_label()
    else:
        popup = Toplevel()
        popup.title("Tá pobre, mlk.")
        Label(popup, font=72, text="Tá sem dinheiro.").pack()

def dormir():
    global sono, fome, sede
    if sono > 0:
        sono = 0
        fome += 10
        sede += 20
        dinheiro.set(dinheiro.get() - 30)
        checar_morte()
        resete_label()

def beber_agua():
    global sede
    if sede > 0:        
        dinheiro.set(dinheiro.get() - 5)
        if sede < 30:
            sede = 0
        else:
            sede -= 30
        checar_morte()
        resete_label()

def comer():
    global fome, sede
    if fome > 0:
        dinheiro.set(dinheiro.get() - 10)

        if fome < 20:
            fome = 0
        else:
            fome -= 20
        sede += 5
        checar_morte()
        resete_label()



# Criação de botões e textos.
tb_entregador = Button(janela, width=20, text="Fazer vinte entregas")
tb_entregador["command"] = partial(trabalhar, 20)
tb_entregador.place(x=10, y=50)

tb_entregar_cinquenta = Button(janela, width=20, text="Fazer cinquenta entregas")
tb_entregar_cinquenta["command"] = partial(trabalhar, 50)
tb_entregar_cinquenta.place(x=10, y=80)

tb_entregar_oitenta = Button(janela, width=20, text="Fazer oitenta entregas")
tb_entregar_oitenta["command"] = partial(trabalhar, 80)
tb_entregar_oitenta.place(x=10, y=110)

tb_entregar_cem = Button(janela, width=20, text="Fazer cem entregas")
tb_entregar_cem["command"] = partial(trabalhar, 100)
tb_entregar_cem.place(x=10, y=140)

tb_entregar_duzentos = Button(janela, width=20, text="Fazer duzentas entregas")
tb_entregar_duzentos["command"] = partial(trabalhar, 200)
tb_entregar_duzentos.place(x=10, y=170)

tb_entregar_quinhentos = Button(janela, width=20, text="Fazer quinhentas entregas")
tb_entregar_quinhentos["command"] = partial(trabalhar, 500)
tb_entregar_quinhentos.place(x=10, y=200)

tb_entregar_mil = Button(janela, width=20, text="Fazer mil entregas")
tb_entregar_mil["command"] = partial(trabalhar, 1000)
tb_entregar_mil.place(x=10, y=230)

tb_comer = Button(janela, width=20, text="Comer", command=comer)
tb_comer.place(x=600, y=50)

tb_beber_agua = Button(janela, width=20, text="Beber água", command=beber_agua)
tb_beber_agua.place(x=600, y=80)

tb_dormir = Button(janela, width=20, text="Dormir", command=dormir)
tb_dormir.place(x=600, y=110)



tb_contratar = Button(janela, width=20, text="Contratar novo trabalhador!", command=contratar)
tb_contratar.place(x=350, y=540)

lb_dinheiro = Label(janela, font=72, text=f"R$ {dinheiro.get()}")
lb_dinheiro.place(x=700, y=550)

lb_trabalhadores = Label(janela, font=72, text=f"Trabalhadores: {trabalhadores}")
lb_trabalhadores.place(x=360, y=575)

lb_fome = Label(janela, font=72, text=f"Fome: {fome}")
lb_fome.place(x=700, y=425)

lb_sede = Label(janela, font=72, text=f"Sede: {sede}")
lb_sede.place(x=700, y=450)

lb_sono = Label(janela, font=72, text=f"Sono: {sono}")
lb_sono.place(x=700, y=475)

barra_entregas = tkinter.ttk.Progressbar(janela, length=200, variable=trabalho, maximum=entregas_da_vez/trabalhadores)
barra_entregas.pack()


janela.title("O entregador")
janela.geometry(JANELA)
janela.resizable(False, False)
janela.mainloop()