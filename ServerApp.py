import requests
import json

def open_json(name) -> dict:
    f = open(name, 'r')
    data = json.load(f)
    f.close()
    return data

# Cria uma classe para representar um item
class Item:
    def __init__(self, name, referenceProductId, quantity):
        self.name = name
        self.referenceProductId = referenceProductId
        self.quantity = quantity

    def __str__(self):
        return f'{self.name} {self.referenceProductId} {self.quantity}'

# Cria uma classe para representar uma lista de compras da Alexa
class AlexaList:
    def __init__(self, link, headers, sample=False):
        self.link = link
        self.headers = headers
        self.sample = sample
        # Código para requisitar a lista de compras da Alexa caso sample=False
        if sample == False:
            self.request()
        # Caso sample=True, carrega a lista de compras de exemplo
        else:
            self.items = [{'completed': False, 'createdDateTime': 1670535027116, 'customerId': 'A2W2G623MOT6I', 'id': '70ac9343-e883-4176-af61-ca9cbc9934fd', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670535027116, 'value': 'queijo', 'version': 1}, {'completed': False, 'createdDateTime': 1670535023835, 'customerId': 'A2W2G623MOT6I', 'id': '54e1cc46-dd91-4ce9-ae83-b55b132a2973', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670535023835, 'value': 'presunto', 'version': 1}, {'completed': False, 'createdDateTime': 1670535019794, 'customerId': 'A2W2G623MOT6I', 'id': 'e81ac772-0c26-434e-8ac1-41cefd2fdde1', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670535019794, 'value': 'requeijão', 'version': 1}, {'completed': False, 'createdDateTime': 1670535015990, 'customerId': 'A2W2G623MOT6I', 'id': '75b71c01-bf25-4e49-8bcb-78debc3b8e7a', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670535015990, 'value': 'molho de tomate', 'version': 1}, {'completed': False, 'createdDateTime': 1670535011392, 'customerId': 'A2W2G623MOT6I', 'id': 'ac243684-f4e4-48f1-ae6a-571b166ba3fd', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670535011392, 'value': 'creme de leite', 'version': 1}, {'completed': False, 'createdDateTime': 1670535007471, 'customerId': 'A2W2G623MOT6I', 'id': '4aad82ec-e5a4-4c1c-bdae-b9cd40c51a09', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670535007471, 'value': 'azeite', 'version': 1}, {'completed': False, 'createdDateTime': 1670535003592, 'customerId': 'A2W2G623MOT6I', 'id': 'd6d47bc5-835c-4619-86b3-27c04a1ffa47', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670535003592, 'value': 'leite condensado', 'version': 1}, {'completed': False, 'createdDateTime': 1670534999525, 'customerId': 'A2W2G623MOT6I', 'id': 'f8478b1b-5784-4190-a6d8-1f356529cabb', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670534999525, 'value': 'batata', 'version': 1}, {'completed': False, 'createdDateTime': 1670534996001, 'customerId': 'A2W2G623MOT6I', 'id': 'd6122810-87dc-4ed8-98fc-a6588e4a1100', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670534996001, 'value': 'cebola', 'version': 1}, {'completed': False, 'createdDateTime': 1670534992116, 'customerId': 'A2W2G623MOT6I', 'id': 'd24a5315-7942-4030-84a1-822c511f189e', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670534992116, 'value': 'banana', 'version': 1}, {'completed': False, 'createdDateTime': 1670534988609, 'customerId': 'A2W2G623MOT6I', 'id': 'b2bbbde5-185e-4c00-8587-61fc27817488', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670534988609, 'value': 'refrigerante', 'version': 1}, {'completed': False, 'createdDateTime': 1670534983983, 'customerId': 'A2W2G623MOT6I', 'id': '7cb3aa7f-95ac-45b0-8729-ddbe627279d4', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670534983983, 'value': 'cerveja', 'version': 1}, {'completed': True, 'createdDateTime': 1670422926118, 'customerId': 'A2W2G623MOT6I', 'id': 'f94d3876-0264-42af-a200-8c1cdb28be9b', 'listId': 'A2W2G623MOT6I-SHOP', 'shoppingListItem': True, 'updatedDateTime': 1670504246036, 'value': 'presunto', 'version': 2}]

    def request(self):
        self.items = requests.get(self.link,headers=self.headers).json()['list']

    def __str__(self):
        s = ''
        for item in self.items:
            s += item['value'] + '\n'
        return s

# Cria uma classe para representar o carrinho de compras
class Cart:
    def __init__(self, link, headers, json):
        self.link = link
        self.headers = headers
        self.json = json
        self.request()
    
    def request(self):
        self.items = requests.post(self.link,headers=self.headers,json=self.json).json()['carts'][self.json['storeSlugs'][0]]['itemsMap']

    def update_item(self, item: Item, amount: int):
        requests.patch(self.link+'/beltrame-supermercados-santa-maria/items/{}'.format(item.referenceProductId), headers=self.headers,json={"amount": int(amount)}).json()
        self.request()

    def get_totalPrice(self):
        return requests.post(self.link+'/complete',headers=self.headers,json=self.json).json()['carts'][self.json['storeSlugs'][0]]['totalPrice']

    def clear(self):
        self.request()
        for referenceProductId in self.items.keys():
            requests.patch(self.link+'/'+self.json['storeSlugs'][0]+'/items/{}'.format(referenceProductId), headers=self.headers, json={"amount": -int(self.items[referenceProductId]['quantity'])}).json()
        self.request()

    def test(self):
        self.request()
        for item in self.items:
            it = requests.patch(self.link+'/'+self.json['storeSlugs'][0]+'/items/{}'.format(item), headers=self.headers, json={"amount": 0}).json()
            for i in it:
                print(i, it[i])
            return

    def __str__(self):
        s = ''
        if len(self.items) == 0:
            return 'Carriho vazio'
        for referenceProductId in self.items.keys():
            s += self.items[referenceProductId]['name'] + '  ' + str(self.items[referenceProductId]['quantity']) + '\n'
        s += 'Total: R${:.2f}'.format(self.get_totalPrice())
        return s

# Carrega as variáveis
vars = open_json('variables.json')

# Lê a lista de compras da Alexa
alexa_list = AlexaList(vars['amazon-link'], vars['amazon-headers'])

print("Lista de compras da Alexa:")
print(alexa_list)

# Cria um dicionário de objetos com os itens cadastrados
items = open_json('items.json')
for item in items.keys():
    items[item] = Item(item,items[item]['referenceProductId'],items[item]['quantity'])

# Cria um carrinho
cart = Cart('https://api.supermercadonow.com/carts/v1/carts',vars['beltrame-headers'],{"storeSlugs":["beltrame-supermercados-santa-maria"]})

# Adiciona os itens ao carrinho
for item in alexa_list.items:
    if item['value'] in items.keys() and not item['completed']:
        try:
            if len(cart.items) > 0 and int(cart.items[items[item['value']].referenceProductId]['quantity']) >= int(items[item['value']].quantity):
                continue
        except KeyError:
            pass
        if items[item['value']].referenceProductId in cart.items.keys():
            cart.update_item(items[item['value']], int(int((items[item['value']].quantity)) - int(cart.items[items[item['value']].referenceProductId]['quantity'])))
        else:
            cart.update_item(items[item['value']], items[item['value']].quantity)

# Imprime o carrinho   
print(cart)

# Limpa o carrinho e imprime novamente (para testar)
cart.clear()
print('\n{}'.format(cart))