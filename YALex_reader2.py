import graphviz

# read slr-1.yal file and return a list of tokens
EPSILON = 'ε'
CONCAT = "."
UNION = "|"
STAR = "*"
QUESTION = "?"
PLUS = "+"
LEFT_PARENTHESIS = "("
RIGHT_PARENTHESIS = ")"

OPERADORES = [EPSILON, CONCAT, UNION, STAR, QUESTION,
              PLUS, LEFT_PARENTHESIS, RIGHT_PARENTHESIS]

with open("slr-4.yal", "r") as file:
    content = file.read()


def split(line):
    # withouth using any library
    result = []
    word = ""
    for char in line:
        if char == " ":
            result.append(word)
            word = ""
        else:
            word += char
    result.append(word)

# function to look in string for a char and return the index


def find(string, char):
    for index, char_ in enumerate(string):
        if char_ == char:
            return index
    return -1

# function to look in string for a string given and return the index


def find2(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return index
    return -1

# function to look in string for a string given and if it is found then return true else return false


def find3(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return True
    return False

# delete white spaces withouth using any library like re or split or replace


def delete_white_spaces(string):
    result = ""
    for char in string:
        if char != " ":
            result += char
    return result

# delete white spaces withouth using any library like re or split or replace. But if white spaces are between '' or "" then don't delete them


def delete_white_spaces2(string):
    result = ""
    for index, char in enumerate(string):
        if char == " ":
            if index == 0 or index == len(string) - 1:
                continue
            elif string[index - 1] != "'" and string[index + 1] != "'" and string[index - 1] != '"' and string[index + 1] != '"':
                continue
        result += char
    return result


def is_letter(char):
    ascii_val = ord(char)  # Obtener el valor ASCII del caracter
    return (ascii_val >= 65 and ascii_val <= 90) or (ascii_val >= 97 and ascii_val <= 122)


def is_digit(char):
    ascii_val = ord(char)  # Obtener el valor ASCII del caracter
    return ascii_val >= 48 and ascii_val <= 57


while '(*' in content:
    content = content[:find2(content, '(*')] + \
        content[find2(content, "*)") + 2:]

while '\n' in content:
    content = content[:find(content, '\n')] + \
        " " + content[find(content, '\n') + 1:]


alfabeto_minusculas = 'a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z'
alfabeto_mayusculas = 'A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z'
numeros = '0|1|2|3|4|5|6|7|8|9'

variables = {}
tokens = {}

while 'let' in content:
    index = find2(content, 'let ')
    content = content[index + 3:]
    name = content[:find(content, '=')]
    name = delete_white_spaces(name)
    if find2(content, 'let ') == -1:
        value = content[find2(content, '=') + 1: find2(content, 'rule tokens')]
        value = delete_white_spaces2(value)
        variables[name] = value
        content = content[find2(content, 'rule tokens'):]
    else:
        value = content[find2(content, '=') + 1:find2(content, 'let ')]
        value = delete_white_spaces2(value)
        variables[name] = value
        content = content[find2(content, 'let '):]

newVariables = {}
keys_array = list(variables.keys())


def find4(string, index, string_to_find):
    for i in range(index, len(string)):
        if string[i:i + len(string_to_find)] == string_to_find:
            return i
    return -1


def my_replace(original_str, old_substring, new_substring):
    result_str = ""  # Inicializar el string de resultado
    # Obtener la longitud de la subcadena a reemplazar
    sub_len = len(old_substring)
    i = 0  # Inicializar el índice del string original

    while i < len(original_str):
        # Buscar la siguiente ocurrencia de la subcadena a reemplazar
        j = find4(original_str, i, old_substring)

        # Si no se encontró ninguna ocurrencia más, agregar el resto del string original al resultado y salir del loop
        if j == -1:
            result_str += original_str[i:]
            break

        # Agregar el segmento del string original que está antes de la ocurrencia de la subcadena a reemplazar al resultado
        result_str += original_str[i:j]

        # Agregar la subcadena de reemplazo al resultado
        result_str += new_substring

        # Actualizar el índice para continuar la búsqueda después de la ocurrencia actual de la subcadena a reemplazar
        i = j + sub_len

    return result_str


# check if a string contains another string, but it cant be followed by a letter or a number
arr = ['(', ')', '[', ']', '{', '}', ',', ';', ':', '+', '-',
       '*', '/', '%', '=', '<', '>', '!', '&', '|', '^', '~', ' ']


def find_replace(string, string_to_replace, string_to_replace_with):
    # dividir el string original en un array de strings
    words = []
    word = ""
    for char in string:
        if is_letter(char) or is_digit(char):
            word += char
        else:
            if word != "":
                words.append(word)
                word = ""
            words.append(char)
        # else:
        #     word += char
    if word != "":
        words.append(word)

    resultado = ""
    # print(words)
    for word in words:
        if word == string_to_replace:
            resultado += string_to_replace_with
        else:
            resultado += word
    return resultado


for key, value in variables.items():
    for key2 in keys_array:
        value = find_replace(value, key2, variables[key2])
    variables[key] = value
    newVariables[key] = value

# check for values and if 'A'-'Z' is fount change it to alfabeto_mayusculas, the same for 'a'-'z' and '0'-'9'
for key, value in newVariables.items():
    if find3(value, "'A'-'Z''a'-'z'"):
        value = my_replace(value, "'A'-'Z''a'-'z'",
                           alfabeto_mayusculas + '|' + alfabeto_minusculas)
    if find3(value, "'A'-'Z'"):
        value = value.replace("'A'-'Z'", alfabeto_mayusculas)
    if find3(value, "'a'-'z'"):
        value = value.replace("'a'-'z'", alfabeto_minusculas)
    if find3(value, "'0'-'9'"):
        value = value.replace("'0'-'9'", numeros)
    if find3(value, "' ''\\t''\\n'"):
        value = value.replace("' ''\\t''\\n'", ' ' + '|' + '\t' + '|' + '\n')
    if find3(value, '"\\s\\t\\n"'):
        value = value.replace('"\\s\\t\\n"', ' ' + '|' + '\t' + '|' + '\n')
    if find3(value, "'+''-'"):
        value = value.replace("'+''-'", "'+'" + '|' + "'-'")
    if find3(value, '"0123456789"'):
        value = value.replace('"0123456789"', numeros)
    newVariables[key] = value

# delete [ and ] from the values
for key, value in newVariables.items():
    if find3(value, '['):
        value = my_replace(value, '[', '(')
    if find3(value, ']'):
        value = my_replace(value, ']', ')')
    newVariables[key] = value

OPERADORES2 = [EPSILON, CONCAT, UNION, STAR, QUESTION,
               PLUS, RIGHT_PARENTHESIS]
# validate where to add a concatenation operator. Add . after ] if it is not fallow by an operator or the end of the string


def validate_concatenation(value):
    array = []
    for char in value:
        array.append(char)

    res = ""
    while array:
        char = array.pop(0)
        if char == ')':
            if array:
                if array[0] not in OPERADORES2:
                    res += char + CONCAT
                else:
                    res += char
            else:
                res += char
        elif char == "'":
            if array:
                if len(array) > 3:

                    if array[1] == "'":
                        if array[2] not in OPERADORES2:
                            res += char + array.pop(0) + array.pop(0) + CONCAT
                        else:
                            res += char + array.pop(0) + array.pop(0)
        elif char == '*' or char == '?' or char == '+':
            if array:
                if array[0] not in OPERADORES2:
                    res += char + CONCAT
                else:
                    res += char
            else:
                res += char
        else:
            res += char
    return res


for key, value in newVariables.items():
    newVariables[key] = validate_concatenation(value)


class Simbolo:
    def __init__(self, simbolo, is_operator=False):
        self.val = simbolo
        self.id = ord(simbolo)
        self.is_operator = is_operator


definicion_regular = {}


def convert_to_Simbolo(string):
    array = []
    for char in string:
        array.append(char)

    res = []
    while array:
        char = array.pop(0)
        if char == "'":
            res.append(Simbolo(array.pop(0)))
            array.pop(0)
        elif char in OPERADORES:
            res.append(Simbolo(char, True))
        else:
            res.append(Simbolo(char))
    return res


for key, value in newVariables.items():
    definicion_regular[key] = convert_to_Simbolo(value)

print(newVariables)


def shunting_yard(infix):
    # precedencia de los operadores
    precedence = {'|': 1, '.': 2, '?': 3, '*': 3, '+': 3}
    # pila de operadores
    stack = []
    # cola de salida
    postfix = []
    for c in infix:
        # Si se encuentra un ( se agrega a la pila
        if c.val == '(' and c.is_operator == True:
            stack.append(c)
        # Si se encuentra un ) se sacan los operadores de la pila hasta encontrar un (
        elif c.val == ')' and c.is_operator == True:
            while stack[-1].val != '(' and stack[-1].is_operator == True:
                postfix.append(stack.pop())
            stack.pop()
        # Si se encuentra un operador se sacan los operadores de la pila hasta encontrar un operador de menor precedencia
        elif c.val in precedence and c.is_operator == True:
            while stack and stack[-1].val != '(' and stack[-1].is_operator == True and precedence[c.val] <= precedence[stack[-1].val]:
                postfix.append(stack.pop())
            stack.append(c)
        # Si se encuentra un simbolo se agrega a la cola de salida
        else:
            postfix.append(c)
    # Se sacan los operadores restantes de la pila y se agregan a la cola de salida
    while stack:
        postfix.append(stack.pop())

    return postfix


definicion_regular_postfix = {}
for key, value in definicion_regular.items():
    definicion_regular_postfix[key] = shunting_yard(value)

# for key, value in definicion_regular_postfix.items():
#     print(key + '\n')
#     for item in value:
#         print(item.val, item.is_operator)


class Node:
    def __init__(self, data):
        self.id = id(self)
        self.data = data
        self.left = None
        self.right = None

# La función build_tree crea el árbol de expresiones regulares a partir de una expresión regular en notación postfija


def build_tree(postfix):
    # Se crea una pila vacía
    stack = []
    # Se recorre la expresión regular
    for c in postfix:
        # Si se encuentra un simbolo alfanumerico se crea un nodo con el simbolo y se agrega a la pila
        if not c.is_operator:
            print(c.val, c.is_operator)
            stack.append(Node(c))
        # Si se encuentra un operador unario se crea un nodo con el operador y se saca un nodo de la pila y se agrega como hijo del nodo creado
        elif c.val == '*' or c.val == '?' or c.val == '+':
            node = Node(c)
            node.left = stack.pop()
            stack.append(node)
        # Si se encuentra un operador se crea un nodo con el operador y se sacan los dos nodos de la pila y se agregan como hijos del nodo creado
        else:
            node = Node(c)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    return stack.pop()


# La función draw_tree crea un arbol a partir de un nodo raiz de una expresión regular en notación postfija

def draw_tree(root):
    # Se crea un grafo dirigido
    dot = graphviz.Digraph()
    # Se recorre el árbol de expresiones regulares

    def traverse(node):
        # Si el nodo no es nulo se crea un nodo con el id del nodo y el dato del nodo y se agregan las aristas correspondientes
        if node:
            dot.node(str(id(node)), node.data.val)
            # Si el nodo tiene un hijo izquierdo se crea una arista entre el nodo y el hijo izquierdo
            if node.left:
                dot.edge(str(id(node)), str(id(node.left)))
            # Si el nodo tiene un hijo derecho se crea una arista entre el nodo y el hijo derecho
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)))
            # Se recorre el hijo izquierdo y el hijo derecho utilizando recursividad
            traverse(node.left)
            traverse(node.right)

    traverse(root)
    return dot


def show_tree(postfix, nombre):
    tree = build_tree(postfix)
    dot = draw_tree(tree)
    dot.format = 'png'
    dot.render('arboles/' + nombre, view=False)


# dot = draw_tree(arbol_numeros)
# show_tree(definicion_regular_postfix['number'], 'number')

for key, value in definicion_regular_postfix.items():
    show_tree(value, key)

# org = definicion_regular['number']
# val0 = []
# for item in org:
#     val0.append([item.val, item.is_operator])
# val = definicion_regular_postfix['number']
# r = []
# for item in val:
#     r.append([item.val, item.is_operator])

# print(val0)
# print(r)

# print(content)
