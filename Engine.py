import json
from os import path
import requests
from tkinter import PhotoImage
from tkinter import *
from io import BytesIO
from urllib.request import urlopen
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image


# Cores globais
width_entry = 30
bg_color = "gray90"
box_color = "gray75"
bt_color = "gray90"


def open_json(name) -> dict:
    f = open(name, 'r')
    vars = json.load(f)
    f.close()
    return vars
    
# ------ Funções ------

# Função para mover os separadores na GUI
def move(event): 
    # Determina a coluna e a região do evento de mouse
    column = Main.tv.identify("column", event.x, event.y)
    region = Main.tv.identify("region", event.x, event.y)

    # Se o evento odorreu em um separador, move de acordo com a coluna
    if region == 'separator':
        if column == '#0':
            Main.s1.place(x=(event.x-200))
        if column == '#1':
            Main.s2.place(x=(event.x-600))
        
# Função para ordenar a lista de produtos do Treeview
def treeview_sort_column(tv, col, reverse):
    # Cria uma lista com os valores da coluna e os identificadores da linha de cada item no Treeview
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    
    # Remove o foco e a seleção dos itens no Treeview
    tv.focus('')
    tv.selection_remove(tv.selection())
    
    try:
        # Classifica a lista usando os valores da coluna como chave de classificação
        # Inverte a classificação se a coluna se o valor de reverse for True
        l.sort(key=lambda t: float(t[0]), reverse=reverse)
    except ValueError:
        # Se o valor da coluna não puder ser convertido em um número flutuante, classifica a lista como string
        l.sort(reverse=reverse)
       
    # Limpa o Treeview e insere os itens da lista ordenados na árvore
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # Atribui um comando ao cabeçalho da coluna para permitir que a classificação seja invertida na próxima vez que o usuário clicar no cabeçalho	
    tv.heading(col, command=lambda _col=col: treeview_sort_column(tv, _col, not reverse))


def pos(size):     
    """Calcula as coordenadas x e y para centralizar uma janela na tela.
    
    size: uma string com o tamanho da janela no formato "largura x altura"
    """

    # Obtém as dimensões da tela
    screen_width  = Main.window.winfo_screenwidth()
    screen_height = Main.window.winfo_screenheight()

    # Divide a string size em largura e altura
    width = int(size.split('x')[0])
    height = int(size.split('x')[1])
    
    # Calcula as coordenadas x e y para centralizar a janela
    x = (screen_width/2)  - (width/2)
    y = (screen_height/2)  - (height/2)
    
    # Retorna as coordenadas x e y
    return (x,y)

    
# ------ Pop-ups ------

# Pop-up item
def popup_item(values, event=None):

    if (values==''):
        pass
    else:
        # Cria uma nova janela pop-up e configura suas dimensões e título
        pop = Toplevel(bg=bg_color)
        size = '500x200'
        pop.geometry(size)
        pop.title("Detalhes")

        # Cria variáveis de texto e número para os campos de entrada
        txtSalvar = StringVar()
        Quantidade  = IntVar()

        # Cria os widgets da interface
        lblnome        = Label(pop, text="Nome:", bg=bg_color)
        lblnome2       = Label(pop, text=values[1], bg=bg_color)
        lblpreco       = Label(pop, text="Preço:", bg=bg_color)
        lblpreco2      = Label(pop, text=values[2], bg=bg_color)
        lblsalvar      = Label(pop, text="Salvar como:", bg=bg_color)
        lblquantidade  = Label(pop, text="Quantidade:", bg=bg_color)
        entQuantidade  = Entry(pop, textvariable=Quantidade, width=5, bg=box_color)
        entSalvar      = Entry(pop, textvariable=txtSalvar, width=width_entry, bg=box_color)

        btnSalvar      = Button(pop, width = 40, text="Salvar", bg=bt_color)

        # Posiciona os widgets na janela pop-up
        lblnome.place(relx=0.4, rely=0.2, anchor='center')
        lblnome2.place(relx=0.6, rely=0.2, anchor='center')
        lblpreco.place(relx=0.4, rely=0.32, anchor='center')
        lblpreco2.place(relx=0.55, rely=0.32, anchor='center')
        lblquantidade.place(relx=0.4, rely=0.45, anchor='center')
        entQuantidade.place(relx=0.55, rely=0.45, anchor='center')
        lblsalvar.place(relx=0.4, rely=0.6, anchor='center')
        entSalvar.place(relx=0.7, rely=0.6, anchor='center')

        btnSalvar.place(relx=0.5, rely=0.8, anchor='center')

        def salvar(event=None):
            """
            Lê os dados do arquivo JSON e adiciona um novo item usando os valores dos campos de entrada.
            """
            file_data = []
            
            # Cria o arquivo JSON se ele não existir
            if path.isfile('items.json') is False:
              a = open('items.json', 'w')

            with open('items.json', 'r+', encoding='utf-8') as file:
                try:
                    # Tenta carregar os dados do arquivo como um dicionário
                    file_data = json.loads(file.read())
                    
                    # Adiciona um novo item ao dicionário usando os valores dos campos de entrada como chaves
                    file_data[txtSalvar.get()]={'referenceProductId': values[0], 'quantity': entQuantidade.get(), 'slug': values[3], 'image_thumbnail': values[4]}
                    file = open('items.json', 'w+')
                    
                    # Grava o dicionário no arquivo JSON
                    json.dump(file_data, file,  indent = 1)
                except:
                    # Caso o arquivo esteja vazio, cria um novo dicionário e adiciona um novo item
                    json.dump({txtSalvar.get(): {'referenceProductId': values[0], 'quantity': entQuantidade.get(), 'slug': values[3], 'image_thumbnail': values[4]}}, file)

            # Fecha a janela pop-up
            pop.destroy()

        # Associa a tecla Enter ao botão Salvar
        entSalvar.bind('<Return>', salvar)
        # Associa o botão salvar ao comando salvar
        btnSalvar.configure(command=salvar)

        # Posiciona a janela pop-up na tela
        pop.geometry('+%d+%d' % (pos(size)))
   
# Pop-up para buscar produtos
def popup_search():
    
    # Cria uma janela pop-up
    pop = Toplevel(bg=bg_color)
    pop.title("Buscar Produto")
    size = '400x150'
    width_entry = 30
    pop.geometry(size)

    # Cria variáveis que armazenarão o texto inserido pelo usuário.
    txtNome         = StringVar()
 
    # Labels
    lblnome        = Label(pop, text="Nome", bg=bg_color)

    # Botão
    btnSearch     = Button(pop, width = 40, text="Buscar", bg=bt_color)

    # Campo de entrada
    entNome        = Entry(pop, textvariable=txtNome, width=width_entry, bg=box_color)

    # Posiciona os widgets na janela pop-up
    # Labels 
    lblnome.place(relx=0.25, rely=0.3, anchor='center')
    
    # Campos de entrada
    entNome.place(relx=0.55, rely=0.3, anchor='center')
    
    # Botão de busca
    btnSearch.place(relx=0.5, rely=0.8, anchor='center')

    # Define o foco no campo de entrada
    entNome.focus_set()

    def search_command(event=None):
        global img
        img=[]
        i = 0
        
        # Abre o arquivo JSON que contém as variáveis de acesso à API
        vars = open_json('variables.json')

        # Armazena o termo de busca digitado pelo usuário
        search_term = txtNome.get()

        # Envia a requisição à API com o termo de busca
        searched_items = requests.get('https://api.supermercadonow.com/search/v1/bulksearch?query={}&stores=beltrame-supermercados-santa-maria&size=50&page=1'.format(search_term), headers=vars['beltrame-headers']).json()
        
        values=[]

        # Remove os itens antigos da Treeview caso haja algum
        for j in Main.tv.get_children():
            Main.tv.delete(j)
            
        # Adiciona os itens retornados pela API à Treeview
        for item in searched_items['items']:

            # Obtém a URL da imagem do item e a converte para um objeto ImageTk
            img_url = item['image_thumbnail']
            response = requests.get(img_url)
            img_data = response.content
            image = Image.open(BytesIO(img_data))
            resized = image.resize((120, 120))
            img.append(ImageTk.PhotoImage(resized))

            # Adiciona os valores do item à lista values            
            values.append(item['product_store_id'])
            values.append(item['name'])
            values.append('R${}'.format(item['price']))
            values.append(item['slug'])
            values.append(item['image_thumbnail'])
            Main.tv.insert('', END, values=values, image=img[i])
            values.clear()
            i=i+1

        # Fecha a janela pop-up
        pop.destroy()

    # Associa a tecla Enter ao botão Search
    entNome.bind('<Return>', search_command)
    
    # Associa o botão salvar à função search_command
    btnSearch.configure(command=search_command)

    # Posiciona a janela pop-up na tela
    pop.geometry('+%d+%d' % (pos(size)))

# Pop-up lista
def popup_lista():
    # Lista para armazenar as imagens dos produtos
    global imge
    imge=[]
    i = 0
    
    # Cria uma janela pop-up
    pop = Toplevel(bg=bg_color)
    pop.title("Minha Lista de Produtos")
    size = '870x650'
    width_entry = 30
    pop.geometry(size)

    # Criação das colunas e respectivos nomes na tabela
    columns = ("id", "Produto", "Quantidade a ser comprada")
    
    # Criação da tabela para exibir os produtos
    tv = ttk.Treeview(pop, columns=columns, height=5)

    # Configuração da altura da linha da tabela (depende do tamanho fixado para a imagem)
    s = ttk.Style()
    s.configure('Treeview', rowheight=110)

    # Nome das colunas da tabela
    tv.heading("#0", text="Imagem do produto")
    for col in columns:
        tv.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tv, _col, False))
    
    # Configuração da largura das colunas
    tv.column(1, width = 400)
    tv.column(2, width = 250, anchor = 'center')
   
    
    # Exibição das colunas com o nome e quantidade do produto
    tv["displaycolumns"]=(1,2)

    # Separadores verticais entre as colunas
    s1 = ttk.Separator(tv, orient='vertical')
    s2 = ttk.Separator(tv, orient='vertical')  

    # Posicionamento dos separadores
    s1.place(relx=0.233, rely=0.045, width=1, relheight=0.95)
    s2.place(relx=0.704, rely=0.045, width=1, relheight=0.95)

    # Criação do scroll
    scroll = ttk.Scrollbar(pop, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=scroll.set)

    # Botões
    btnDeletar      = Button(pop, bg=bt_color, width = 40, text="Deletar Produto", command=lambda :delete_command(tv))
    btnModificar    = Button(pop, bg=bt_color, width = 40, text="Modificar Produto", command=lambda :popup_update(tv))


    # Associando os objetos a grid da janela
    tv.grid(row=0, column=2, rowspan=20, columnspan=6)

    # Botões
    btnDeletar.grid(row=21, column=4, columnspan=1)
    btnModificar.grid(row=21, column=5, columnspan=1)

    # Posicionamento dos botões
    btnDeletar.grid_configure(sticky='S', padx=25, pady=25)
    btnModificar.grid_configure(sticky='S', padx=25, pady=25)

    # Posicionamento do scroll
    scroll.grid(row=0, column=8, rowspan=20)

    # Configuração do scroll
    scroll.grid_configure(padx=0, pady=0, sticky='NS')

    # Atualiza a janela pop-up
    pop.update()

    # Limpa os itens antigos da Treeview
    for j in tv.get_children():
        tv.delete(j)

    # Verifica se o arquivo items.json existe
    if path.isfile('items.json') is False:
        # Exibe uma mensagem de erro caso o arquivo não exista
        messagebox.showerror(title="Erro", message="Sua lista está vazia!")
        with open('items.json', 'w', encoding='utf-8') as file:
            json.dump({}, file, indent=4)

    # Abre o arquivo items.json em modo de leitura e escrita
    with open('items.json', 'r+', encoding='utf-8') as file:
        try:
            # Tenta ler o conteúdo do arquivo
            file_data = json.loads(file.read())
        except:
            # Exibe uma mensagem de erro caso o arquivo exista porem esteja vazio
            messagebox.showerror(title="Erro", message="Sua lista está vazia!")

    # Cria uma lista para armazenar os valores dos itens
    values=[]
    
    # Popula a Treeview com os itens do arquivo items.json
    for key, item in file_data.items():
        
        # Obtém a URL da imagem do produto e transforma em um objeto ImageTk
        img_url = item['image_thumbnail']
        response = requests.get(img_url)
        img_data = response.content
        image = Image.open(BytesIO(img_data))
        resized = image.resize((120, 120))
        imge.append(ImageTk.PhotoImage(resized))
        
        # Adiciona os dados do produta na lista de valores
        values.append(item['referenceProductId'])
        values.append(key)
        values.append(item['quantity'])
        values.append(item['slug'])
        values.append(item['image_thumbnail'])
        
        # Insere os valores e a imagem no fim da Treeview
        tv.insert('', END, values=values, image=imge[i])
        
        # Limpa a lista de valores para a próxima iteração
        values.clear()
        i=i+1

    # Função chamada ao clicar no botão de "deletar produto"
    def delete_command(tv, event=None):
        # Verifica se algum item foi selecionado
        row_selected = tv.focus()
        
        if (row_selected==''):
            # Exibe uma mensagem de erro caso nenhum item tenha sido selecionado
            messagebox.showerror(title="Erro", message="Selecione um item!")
        else:
            # Inicializa o dicionário de dados para ser preenchido com os itens que não foram deletados
            file_data = {}
         
            # Deleta o item selecionado
            tv.delete(row_selected)

            # Itera sobre os itens da Treeview para atualiza-los
            for j in tv.get_children():
                # Valores que não foram deletados
                values = tv.item(j, option ='values')
                # Itera valores
                file_data[values[1]]={'referenceProductId': values[0], 'quantity': values[2], 'slug': values[3], 'image_thumbnail': values[4]}
        
            # Abre o arquivo items.json em modo de leitura e escrita
            file = open('items.json', 'w+')
            # Escreve os dados no arquivo
            json.dump(file_data, file,  indent = 1)
        
            # Fecha o pop-up
            pop.destroy()
    
    # Posiciona a janela pop-up no centro da tela
    pop.geometry('+%d+%d' % (pos(size)))

# Pop-up atualizar
def popup_update(tv, event=None):
    '''
    Abre uma janela para atualizar o nome e a quantidade de um produto selecionado na lista de compras
    '''
    
    # Obtém o item selecionado na Treeview
    row_selected = tv.focus()
    # Verifica se algum item foi selecionado
    if (row_selected==''):
        messagebox.showerror(title="Erro", message="Selecione um item!")
    else:
        # Obtém os valores do item selecionado
        values = tv.item(row_selected, option ='values')

        # Cria uma janela pop-up
        pop = Toplevel(bg=bg_color)
        size = '500x200'
        pop.title("Modificar Produto")
        width_entry = 30
        pop.geometry(size)

        # Variáveis para armazena os valores do novo nome e quantidade
        txtSalvar        = StringVar()
        Quantidade       = IntVar()

        # Cria os labels do pop-up
        lblnome        = Label(pop, text="Nome:", bg=bg_color)
        lblnome2       = Label(pop, text=values[1], bg=bg_color)
        lblquantidade  = Label(pop, text="Quantidade atual:", bg=bg_color)
        lblquantidade2 = Label(pop, text=values[2], bg=bg_color, anchor='w')
        lblsalvar      = Label(pop, text="Salvar como:", bg=bg_color)
        lblquantidade3 = Label(pop, text="Nova quantidade:", bg=bg_color)
        
        # Entradas de dados
        entQuantidade  = Entry(pop, textvariable=Quantidade, width=5, bg=box_color)
        entSalvar      = Entry(pop, textvariable=txtSalvar, width=width_entry, bg=box_color)

        # Cria o botão de salvar as alterações
        btnSalvar      = Button(pop, width = 40, text="Salvar", bg=bt_color)

        # Posiciona os elementos na janela pop-up
        lblnome.place(relx=0.4, rely=0.2, anchor='center')
        lblnome2.place(relx=0.6, rely=0.2, anchor='center')
        lblquantidade.place(relx=0.4, rely=0.32, anchor='center')
        lblquantidade2.place(relx=0.55, rely=0.32, anchor='center')
        lblquantidade3.place(relx=0.4, rely=0.45, anchor='center')
        entQuantidade.place(relx=0.55, rely=0.45, anchor='center')
        lblsalvar.place(relx=0.4, rely=0.6, anchor='center')
        entSalvar.place(relx=0.7, rely=0.6, anchor='center')

        btnSalvar.place(relx=0.5, rely=0.8, anchor='center')
        
        # Define a funlção salvar, que é executada ao pressionar o botão
        def salvar(event=None):
            file_data = {}
            
            values = tv.item(row_selected, option ='values')
            file_data[txtSalvar.get()]={'referenceProductId': values[0], 'quantity': entQuantidade.get(), 'slug': values[3], 'image_thumbnail': values[4]}
            tv.delete(row_selected)
            
            # Adiciona os itesn que não foram deletados ao file_data
            for j in tv.get_children():
                # Valores que não foram deletados
                values = tv.item(j, option ='values')
                # Itera valores
                file_data[values[1]]={'referenceProductId': values[0], 'quantity': values[2], 'slug': values[3], 'image_thumbnail': values[4]}
            file = open('items.json', 'w+')
            json.dump(file_data, file,  indent = 1)

            # Fecha o pop-up
            pop.destroy()

            value = []
            i = 0
            
            for key, item in file_data.items():
                
                # Obtém a URL da imagem redimensiona a imagem
                img_url = item['image_thumbnail']
                response = requests.get(img_url)
                img_data = response.content
                image = Image.open(BytesIO(img_data))
                resized = image.resize((120, 120))
                imge.append(ImageTk.PhotoImage(resized))

                # Insere os valores na Treeview      
                value.append(item['referenceProductId'])
                value.append(key)
                value.append(item['quantity'])
                value.append(item['slug'])
                value.append(item['image_thumbnail'])
                tv.insert('', END, values=value, image=imge[i])
                value.clear()
                i=i+1

        # Atribui o evento de salvar ao botão e ao pressionar a tecla Enter    
        entSalvar.bind('<Return>', salvar)
        # Atribui o evento de salvar ao botão
        btnSalvar.configure(command=salvar)

        # Posiciona a janela pop-up no centro da tela
        pop.geometry('+%d+%d' % (pos(size)))
      
# Classe que define a interface gráfica da aplicação
class Main():
      
    x_pad = 5
    y_pad = 3
    
    # Cria a janela principal
    window = Tk()

    window.call('wm', 'iconphoto', window._w, ImageTk.PhotoImage(Image.open('icon.ico')))
    window.title("Seleção de produtos")
    window["bg"]=bg_color
    
    # Define os nomes e as colunas da Treeview
    columns = ("id", "Produto", "Preço(Unitário)")
    
    # Cria a Treeview
    tv = ttk.Treeview(window, columns=columns, height=5)

    # Define o tamanho da linha da Treeview
    s = ttk.Style()
    s.configure('Treeview', rowheight=110)

    # Define o título da primeira coluna da TreeView
    tv.heading("#0", text="Imagem do produto")
    # Associa a função de sort alfabético das colunas com a Treeview
    for col in columns:
        tv.heading(col, text=col, command=lambda _col=col: treeview_sort_column(Main.tv, _col, False))
    
    # Define o tamanho das colunas da Treeview
    tv.column(1, width = 400)
    tv.column(2, width = 250)
   
    # Exibe as colunas de produto e preço na Treeview
    tv["displaycolumns"]=(1,2)

    # Cria dois separadores verticais
    s1 = ttk.Separator(tv, orient='vertical')
    s2 = ttk.Separator(tv, orient='vertical')  

    # Posiciona os separadores na Treeview
    s1.place(relx=0.233, rely=0.045, width=1, relheight=0.95)
    s2.place(relx=0.704, rely=0.045, width=1, relheight=0.95)
    
    # --- Criando os objetos que estarão na janela ---   
    # Botoes
    btnBuscar      = Button(window, bg=bt_color, width = 40, text="Buscar Produto", command=popup_search)
    btnLista       = Button(window, bg=bt_color, width = 40, text="Minha Lista", command=popup_lista)
  
    # Separadores
    separator      = ttk.Separator(window, orient='horizontal')
    separator2     = ttk.Separator(window, orient='horizontal')
    
    # Scrollbar
    scroll = ttk.Scrollbar(window, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=scroll.set)

    # --- Associando os objetos a grid da janela ---
    # Botões
    btnBuscar.grid(row=0, column=0, columnspan=2)
    btnLista.grid(row=1, column=0, columnspan=2)

    # 2
    separator.grid(row=15,column=0,columnspan=2, ipadx=150)
   
    # Treeview
    tv.grid(row=0, column=2, rowspan=20, columnspan=6)

    # Scrollbar
    scroll.grid(row=0, column=8, rowspan=20)

    # Calcula a posição inicial da janela na tela
    screen_width  = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Atualiza a janela para obter as dimensões atualizadas
    window.update()
    
    # Obtém as dimensões da janela
    width         = window.winfo_width()
    height        = window.winfo_height()

    # Permite mover a lista de itens com o mouse
    tv.bind("<B1-Motion>", move) 
    
    # Calcula as posições x e y para centralizar a janela
    x = (screen_width/2)  - (width/2)
    y = (screen_height/2)  - (height/2)
    window.geometry('+%d+%d' % (x, y))

    # Organizando a interface gráfica da aplicação
    for child in window.winfo_children():
        widget_class = child.__class__.__name__
        if widget_class == "Button":
            child.grid_configure(sticky='WE', padx=x_pad, pady=y_pad)
        elif widget_class == "Listbox":
            child.grid_configure(padx=0, pady=0, sticky='NS')
        elif widget_class == "Scrollbar":
            child.grid_configure(padx=0, pady=0, sticky='NS')
        else:
            child.grid_configure(padx=x_pad, pady=y_pad, sticky='N')

    # Executa a janela principal
    def run(self):
        Main.window.mainloop()
