# Importa a classe Main do arquivo Engine.py
from Engine import *

if __name__ == "__main__":
    # Cria uma instancia da classe Main 
    app = Main()
    
    # Define um comportamento de duplo clique com o botão esquerdo do mouse para o objeto app.tv
    # Quando o evento ocorrer, a função popup_item será chamada com o valor do item selecionado
    app.tv.bind('<Double-Button-1>', lambda event: popup_item(app.tv.item(app.tv.focus(), option ='values')))
    
    # Define um comportamento para a tecla Enter para o objeto app.tv
    # Quando o evento ocorrer, a função popup_item será chamada com o valor do item selecionado
    app.tv.bind('<Return>', lambda event: popup_item(app.tv.item(app.tv.focus(), option ='values')))

    # Inicia a aplicação
    app.run()