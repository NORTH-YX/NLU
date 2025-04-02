from parser import summarize_actions

def simulate_edit_mode(actions):
    """
    Permite al usuario editar manualmente campos de cada acción.
    """
    print("🛠 Modo edición activado. Puedes escribir comandos como:")
    print("  editar <número>.<campo>: <nuevo_valor>")
    print("  mostrar → ver acciones actuales")
    print("  listo → salir del modo edición\n")

    while True:
        command = input("Usuario: ").strip()
        if command.lower() == "listo":
            print("✅ Saliendo del modo edición...")
            break
        elif command.lower() == "mostrar":
            print("\n📋 Acciones actuales:\n")
            print(summarize_actions(actions))
        elif command.startswith("editar"):
            try:
                _, body = command.split("editar", 1)
                field_path, new_value = body.strip().split(":", 1)
                index_str, field = field_path.strip().split(".")
                index = int(index_str) - 1
                actions[index]['params'][field.strip()] = new_value.strip()
                print(summarize_actions(actions))
                print("✏️ Parámetro actualizado exitosamente.")
            except Exception as e:
                print(f"❌ Error al interpretar el comando de edición: {e}")
        else:
            print("❗ Comando no reconocido. Usa 'editar', 'mostrar' o 'listo'.")
    return actions