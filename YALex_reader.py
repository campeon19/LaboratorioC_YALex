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

with open("slr-1.yal", "r") as file:
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

# if a variable has a value that is a variable, then replace the variable with the value of the variable.
# it must search for the variable name concidering that it can appear in the middle of the string
# for example: variable + '+'

keys_array = list(variables.keys())
# keys_array = reversed(keys_array)

# for value in variables.values():
#     # name = ''
#     for key in keys_array:
#         if find3(value, key):
#             value = value.replace(key, variables[key])
#             # name = key
#     newVariables[name] = value

# function to replace a string with another string in a string (like .replace but withouth using it)


# def replace(string, string_to_replace, string_to_replace_with):
#     result = ""
#     for index, char in enumerate(string):
#         print(string)
#         if string[index:index + len(string_to_replace)] == string_to_replace:
#             result += string_to_replace_with
#             for i in range(len(string_to_replace) - 1):
#                 string = string[:index + 1] + string[index + 2:]
#             print(string)
#         else:
#             result += char
#     return result

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


# for key, value in variables.items():
#     for key2 in keys_array:
#         if find3(value, key2):
#             value = value.replace(key2, variables[key2])
#             # name = key
#     newVariables[key] = value


# check if a string contains another string, but it cant be followed by a letter or a number
arr = ['(', ')', '[', ']', '{', '}', ',', ';', ':', '+', '-',
       '*', '/', '%', '=', '<', '>', '!', '&', '|', '^', '~', ' ']


# def find5(string, _string):
#     for index, char in enumerate(string):
#         if string[index:index + len(_string)] == _string:
#             print(string[index:index + len(_string) + 1])
#             if (index + len(_string) + 1) < len(string):
#                 print(string[index + len(_string)])
#                 if string[index + len(_string)] in arr:
#                     return True
#     return False

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
        # if find5(value, key2):
        #     value = my_replace(value, key2, variables[key2])
        #     # name = key
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
for key, value in newVariables.items():
    index_iter = 0
    for index, char in enumerate(value):
        if char == ')':
            # check if the next char is not the end of the string
            # print(index)
            # print(char, value[index + 1])
            if index_iter + 1 < len(value):
                if value[index_iter + 1] not in OPERADORES2:
                    value = value[:index_iter + 1] + \
                        CONCAT + value[index_iter + 1:]
                    index_iter += 1
        index_iter += 1
    newVariables[key] = value


# for key, value in newVariables.items():
#     for char in value:
#         if char in alfabeto_mayusculas + alfabeto_minusculas + numeros:
#             if value[value.index(char) - 1] not in alfabeto_mayusculas + alfabeto_minusculas + numeros + ')':
#                 value = value[:value.index(char)] + \
#                     CONCAT + value[value.index(char):]
#             if value[value.index(char) + 1] not in alfabeto_mayusculas + alfabeto_minusculas + numeros + '(':
#                 value = value[:value.index(char) + 1] + \
#                     CONCAT + value[value.index(char) + 1:]
#     newVariables[key] = value

# delete [ and ] from the values
# for key, value in newVariables.items():


class Simbolo:
    def __init__(self, simbolo, is_operator=False):
        self.c_id = simbolo
        self.id = ord(simbolo)


definicion_regular = {}

# for key, value in newVariables.items() save key in definicion_regular and for every char in value create a Simbolo and save it in definicion_regular[key]
# if the char is in OPERADORES, but is not surrounded by ' ', then it is an operator, otherwise it is a char
# for key, value in newVariables.items():
#     definicion_regular[key] = []
#     for index, char in enumerate(value):
#         if char in OPERADORES and value[index - 1] != "'" and value[index + 1] != "'":
#             definicion_regular[key].append(Simbolo(char, True))
#         else:
#             definicion_regular[key].append(Simbolo(char))


# for key, value in newVariables.items():
#     definicion_regular[key] = []
#     index_iter = 0
#     for index, char in enumerate(value):
#         if char == "'" and value[index + 1] in OPERADORES an:

#         if char in OPERADORES and value[index - 1] != "'" and value[index + 1] != "'":
#             definicion_regular[key].append(Simbolo(char, True))
#         else:
#             definicion_regular[key].append(Simbolo(char))

print(newVariables)


# print(content)
