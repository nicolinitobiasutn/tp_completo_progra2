import inputs
import prints
import funciones

def login_orquestador(usuarios):
    while True:
        usuario, contrasenia = inputs.pedir_credenciales()
        if len(usuario) >= 3 and len(contrasenia) >= 6:
            user_dict = funciones.buscar_usuario(usuarios, usuario)
            if user_dict and user_dict["contrasenia"] == contrasenia:
                print(f"\nAcceso concedido.")
                return user_dict
            prints.mostrar_error_credenciales()
        else:
            prints.mostrar_error_longitud()

# --- MENÚ JUGADOR ---
def menu_jugador(usuario_actual, usuarios, juegos, compras, rutas):
    while True:
        print(f"\n[Menú] Sesión: {usuario_actual['usuario']} ({usuario_actual['rol']})")
        print("1. Consultar mi Perfil Gamer")
        print("2. Explorar catálogo y comprar")
        print("3. Ver mi biblioteca")
        print("4. Cerrar Sesión")

        opcion = inputs.pedir_opcion_menu()
        if opcion == "1":
            biblioteca = funciones.obtener_biblioteca_jugador(compras, usuario_actual['usuario'])
            prints.mostrar_perfil_jugador(usuario_actual, biblioteca)
        elif opcion == "2":
            explorar_catalogo_jugador(usuario_actual, usuarios, juegos, compras, rutas)
        elif opcion == "3":
            biblioteca = funciones.obtener_biblioteca_jugador(compras, usuario_actual['usuario'])
            prints.mostrar_biblioteca_jugador(biblioteca)
        elif opcion == "4":
            break

def explorar_catalogo_jugador(usuario_actual, usuarios, juegos, compras, rutas):
    nombre_dev = inputs.pedir_nombre_desarrolladora()
    desarrolladora = funciones.buscar_usuario(usuarios, nombre_dev)

    if desarrolladora is None or not funciones.cadenas_iguales(desarrolladora["rol"], "Desarrolladora"):
        print("Error: la desarrolladora indicada no existe.")
        return

    juegos_dev = funciones.filtrar_por_desarrolladora(juegos, desarrolladora["usuario"])
    if not juegos_dev:
        print("Esta desarrolladora no tiene juegos publicados.")
        return

    prints.mostrar_catalogo(juegos_dev, desarrolladora["usuario"])
    opcion = inputs.pedir_opcion_juego(len(juegos_dev))
    if opcion == 0:
        print("Operación cancelada.")
        return
    juego_elegido = juegos_dev[opcion - 1]

    biblioteca = funciones.obtener_biblioteca_jugador(compras, usuario_actual["usuario"])
    ya_lo_tiene = False
    for compra in biblioteca:
        if funciones.cadenas_iguales(compra["juego"], juego_elegido["nombre"]):
            ya_lo_tiene = True

    if ya_lo_tiene:
        print("Error: ya tenés este juego en tu biblioteca.")
        return

    metodo_pago = inputs.pedir_metodo_pago()
    if metodo_pago is None:
        print("Operación cancelada.")
        return

    prints.mostrar_resumen_compra(juego_elegido, desarrolladora, metodo_pago)

    if not inputs.pedir_confirmacion("¿Confirma la compra?"):
        print("Error: compra rechazada.")
        return

    nueva_compra = {
        "jugador": usuario_actual["usuario"],
        "juego": juego_elegido["nombre"],
        "desarrolladora": desarrolladora["usuario"],
        "precio": juego_elegido["precio"],
        "metodo_pago": metodo_pago,
        "fecha": "2025-06-01"
    }
    compras.append(nueva_compra)
    juego_elegido["copias_vendidas"] = juego_elegido["copias_vendidas"] + 1

    funciones.guardar_json(rutas["juegos"], juegos)
    funciones.guardar_json(rutas["compras"], compras)
    print("¡Compra confirmada con éxito!")

# --- MENÚ DESARROLLADORA ---
def menu_desarrolladora(usuario_actual, juegos, rutas):
    while True:
        print(f"\n[Menu] Empresa: {usuario_actual['usuario']} ({usuario_actual['rol']})")
        print("1. Ver mis datos")
        print("2. Publicar juego")
        print("3. Ver ventas")
        print("4. Cerrar sesion")

        opcion = inputs.pedir_opcion_menu()
        if opcion == "1":
            prints.mostrar_perfil_desarrolladora(usuario_actual)
        elif opcion == "2":
            publicar_juego_desarrolladora(usuario_actual, juegos, rutas["juegos"])
        elif opcion == "3":
            matriz = funciones.obtener_ventas_a_matriz(juegos, usuario_actual['usuario'])
            prints.mostrar_matriz_ventas(matriz, usuario_actual['usuario'])
        elif opcion == "4":
            break
        else:
            print("Opcion invalida.")

def publicar_juego_desarrolladora(usuario_actual, juegos, ruta_juegos):
    print("\n--- PUBLICAR NUEVO JUEGO ---")
    nombre = inputs.pedir_nombre_juego()
    if funciones.buscar_juego(juegos, nombre) is not None:
        print("Error: Ya existe un juego con ese nombre.")
        return

    precio = inputs.pedir_precio_juego()
    funciones.publicar_juego(usuario_actual, juegos, nombre, precio)
    funciones.guardar_json(ruta_juegos, juegos)
    print("Juego publicado correctamente.")

# --- MENÚ ADMINISTRADOR ---
def menu_administrador(usuario_actual, usuarios, eliminados, juegos, rutas):
    while True:
        print(f"\n[Menú] Administrador: {usuario_actual['usuario']}")
        print("1. Dar de alta nuevo usuario")
        print("2. Dar de baja un usuario (Persistencia de históricos)")
        print("3. Desplegar Ranking Top 5 Ventas")
        print("4. Auditoría del sistema (Roles)")
        print("5. Cerrar Sesión")
        
        opcion = inputs.pedir_opcion_menu()
        if opcion == "1":
            alta_usuario_admin(usuarios, rutas["usuarios"])
        elif opcion == "2":
            baja_usuario_admin(usuarios, eliminados, rutas["usuarios"], rutas["eliminados"])
        elif opcion == "3":
            top_5 = funciones.ordenar_juegos_por_ventas(juegos)
            prints.mostrar_top_juegos(top_5)
        elif opcion == "4":
            prints.mostrar_info_sistema_completa(usuarios, funciones.filtrar_por_rol)
        elif opcion == "5":
            break

# --- Operaciones Críticas del Administrador ---
def alta_usuario_admin(lista_usuarios, ruta_usuarios):
    print("\n--- PROCESO DE ALTA DE USUARIO ---")
    rol = inputs.pedir_rol_admin()
    username = inputs.pedir_nuevo_username(lista_usuarios, funciones.buscar_usuario)
    contrasenia = inputs.pedir_nueva_contrasenia()
    
    nuevo_usuario = {"usuario": username, "contrasenia": contrasenia, "rol": rol}
    if rol == "Jugador":
        nombre, pais, juego_fav = inputs.pedir_datos_perfil_jugador()
        nuevo_usuario.update({"nombre": nombre, "pais": pais, "juego_favorito": juego_fav, "horas_jugadas": 0})
        
    if inputs.pedir_confirmacion("¿Desea impactar las modificaciones en el JSON?"):
        lista_usuarios.append(nuevo_usuario)
        funciones.guardar_json(ruta_usuarios, lista_usuarios)
        print("Éxito: Datos volcados al archivo de usuarios.")

def baja_usuario_admin(lista_usuarios, lista_eliminados, ruta_usuarios, ruta_eliminados):
    print("\n--- PROCESO DE REMOCIÓN DE USUARIO ---")
    prints.mostrar_lista_usuarios_simple(lista_usuarios)
    target = inputs.pedir_usuario_baja()
    
    indice = funciones.buscar_indice_usuario(lista_usuarios, target)
    if indice == -1:
        print("Error: El usuario ingresado no existe en los registros activos.")
        return
        
    if lista_usuarios[indice]["rol"] == "Administrador":
        print("Error: No está permitido dar de baja cuentas de jerarquía Administrador.")
        return
        
    if inputs.pedir_confirmacion(f"¿Confirma la baja definitiva de '{lista_usuarios[indice]['usuario']}'?"):
        # Extracción física de la memoria dinámica usando pop
        usuario_removido = lista_usuarios.pop(indice)
        lista_eliminados.append(usuario_removido)
        
        # Sincronización inmediata en los archivos correspondientes
        funciones.guardar_json(ruta_usuarios, lista_usuarios)
        funciones.guardar_json(ruta_eliminados, lista_eliminados)
        print("Éxito: Registros actualizados en base de activos e históricos.")
