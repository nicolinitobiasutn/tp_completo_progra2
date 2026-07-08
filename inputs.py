import json

def cargar_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_json(nombre_archivo, datos):
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def a_mayuscula(cadena):
    resultado = ""
    indice = 0
    while indice < len(cadena):
        codigo = ord(cadena[indice])
        if codigo >= 97 and codigo <= 122:  # 'a' a 'z'
            codigo = codigo - 32
        resultado = resultado + chr(codigo)
        indice = indice + 1
    return resultado

def cadenas_iguales(cadena1, cadena2):
    c1 = a_mayuscula(cadena1)
    c2 = a_mayuscula(cadena2)
    if len(c1) != len(c2):
        return False
    indice = 0
    while indice < len(c1):
        if c1[indice] != c2[indice]:
            return False
        indice = indice + 1
    return True

def es_numero(cadena):
    if len(cadena) == 0:
        return False
    indice = 0
    while indice < len(cadena):
        codigo = ord(cadena[indice])
        if codigo < 48 or codigo > 57:
            return False
        indice = indice + 1
    return True

def quitar_espacios(cadena):
    inicio = 0
    fin = len(cadena) - 1
    while inicio <= fin and ord(cadena[inicio]) == 32:
        inicio = inicio + 1
    while fin >= inicio and ord(cadena[fin]) == 32:
        fin = fin - 1
    resultado = ""
    indice = inicio
    while indice <= fin:
        resultado = resultado + cadena[indice]
        indice = indice + 1
    return resultado

def primera_mayuscula(cadena):
    if len(cadena) == 0:
        return cadena
    primera = a_mayuscula(cadena[0])
    resto = ""
    indice = 1
    while indice < len(cadena):
        codigo = ord(cadena[indice])
        if codigo >= 65 and codigo <= 90:  # 'A' a 'Z'
            codigo = codigo + 32
        resto = resto + chr(codigo)
        indice = indice + 1
    return primera + resto

def unir_nombres_juegos(biblioteca):
    texto = ""
    primero = True
    for compra in biblioteca:
        if primero:
            texto = compra["juego"]
            primero = False
        else:
            texto = texto + ", " + compra["juego"]
    return texto


def buscar_usuario(usuarios: list, nombre: str):
    for u in usuarios:
        if cadenas_iguales(u["usuario"], nombre):
            return u
    return None

def buscar_juego(juegos: list, nombre: str):
    for j in juegos:
        if cadenas_iguales(j["nombre"], nombre):
            return j
    return None

def filtrar_por_rol(usuarios: list, rol: str):
    resultado = []
    for u in usuarios:
        if cadenas_iguales(u["rol"], rol):
            resultado.append(u)
    return resultado

def filtrar_por_desarrolladora(juegos: list, nombre: str):
    resultado = []
    for j in juegos:
        if cadenas_iguales(j["desarrolladora"], nombre):
            resultado.append(j)
    return resultado

def obtener_biblioteca_jugador(compras: list, jugador: str):
    biblioteca = []
    for c in compras:
        if cadenas_iguales(c["jugador"], jugador):
            biblioteca.append(c)
    return biblioteca

def obtener_ventas_a_matriz(juegos: list, desarrolladora: str):
    matriz = []
    for j in juegos:
        if cadenas_iguales(j["desarrolladora"], desarrolladora):
            precio = float(j["precio"])
            copias = int(j["copias_vendidas"])
            ingreso_total = precio * copias
            matriz.append([precio, copias, ingreso_total])
    return matriz

def publicar_juego(usuario: dict, juegos: list, nombre: str, precio: float):
    nuevo_juego = {
        "nombre": nombre,
        "desarrolladora": usuario["usuario"],
        "precio": precio,
        "copias_vendidas": 0
    }
    juegos.append(nuevo_juego)
    return juegos

def ordenar_juegos_por_ventas(lista_juegos: list):
    copia_tabla = lista_juegos.copy()
    copia_tabla.sort(key=lambda x: x["copias_vendidas"], reverse=True)
    return copia_tabla[:5]

def buscar_indice_usuario(lista_usuarios: list, nombre_usuario: str):
    for idx, u in enumerate(lista_usuarios):
        if cadenas_iguales(u["usuario"], nombre_usuario):
            return idx
    return -1
