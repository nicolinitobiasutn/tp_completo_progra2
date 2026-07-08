import funciones
import prints
import menu

def main():
    # Definición de rutas físicas de archivos
    rutas_archivos = {
        "usuarios": "usuarios.json",
        "juegos": "juegos.json",
        "compras": "compras.json",
        "eliminados": "eliminados.json"
    }
    
    # Carga de datos estricta desde JSON local
    usuarios = funciones.cargar_json(rutas_archivos["usuarios"])
    juegos = funciones.cargar_json(rutas_archivos["juegos"])
    compras = funciones.cargar_json(rutas_archivos["compras"])
    eliminados = funciones.cargar_json(rutas_archivos["eliminados"])
    
    # Inyección de contingencia únicamente si el entorno carece por completo de usuarios
    if not usuarios:
        usuarios = [
            {"usuario": "adminsteam", "contrasenia": "admin999", "rol": "Administrador"},
            {"usuario": "indiedev", "contrasenia": "clave123", "rol": "Desarrolladora"}
        ]
        funciones.guardar_json(rutas_archivos["usuarios"], usuarios)

    prints.mostrar_bienvenida()
    usuario_sesion = menu.login_orquestador(usuarios)
    
    if usuario_sesion:
        rol = usuario_sesion["rol"]
        if rol == "Jugador":
            menu.menu_jugador(usuario_sesion, usuarios, juegos, compras, rutas_archivos)
        elif rol == "Desarrolladora":
            menu.menu_desarrolladora(usuario_sesion, juegos, rutas_archivos)
        elif rol == "Administrador":
            menu.menu_administrador(usuario_sesion, usuarios, eliminados, juegos, rutas_archivos)

if __name__ == "__main__":
    main()
