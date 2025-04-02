"""
Este archivo contiene la lista de acciones válidas que el bot puede ejecutar,
así como funciones para manejar interacciones como el llenado de campos faltantes.
"""

from validators import validate_field_value, is_field_required, is_field_nullable

# Lista de acciones soportadas por el bot con los campos requeridos, actualizada para producción
action_list = [
    {
        "name": "create_task",
        "required_fields": ["NAME", "DESCRIPTION", "PRIORITY", "ESTIMATED_FINISH_DATE"],
        "optional_fields": ["ASSIGNED_USER_ID", "SPRINT_ID", "PROJECT_ID"]
    },
    {
        "name": "update_task_status",
        "required_fields": ["TASK_ID", "STATUS"]  # Cambiado de "NAME" a "TASK_ID"
    },
    {
        "name": "add_comment",
        "required_fields": ["TASK_ID", "COMMENT", "MENTIONS"]  # Se usa TASK_ID en lugar de NAME para identificar la tarea
    },
    {
        "name": "request_help",
        "required_fields": ["NAME"]
    },
    # Acciones adicionales según el esquema
    {
        "name": "assign_user_to_task",
        "required_fields": ["TASK_ID", "USER_ID"]
    },
    {
        "name": "update_task",
        "required_fields": ["TASK_ID"],
        "optional_fields": ["NAME", "DESCRIPTION", "PRIORITY", "ESTIMATED_FINISH_DATE", "STATUS", "SPRINT_ID", "USER_ID"]
    },
    {
        "name": "delete_task",
        "required_fields": ["TASK_ID"]
    },
    {
        "name": "create_project",
        "required_fields": ["NAME", "DESCRIPTION"]
    },
    {
        "name": "update_project",
        "required_fields": ["PROJECT_ID"],
        "optional_fields": ["NAME", "DESCRIPTION"]
    },
    {
        "name": "delete_project",
        "required_fields": ["PROJECT_ID"]
    },
    {
        "name": "create_sprint",
        "required_fields": ["NAME", "DESCRIPTION", "START_DATE", "END_DATE", "PROJECT_ID"]
    },
    {
        "name": "update_sprint",
        "required_fields": ["SPRINT_ID"],
        "optional_fields": ["NAME", "DESCRIPTION", "START_DATE", "END_DATE", "STATUS"]
    },
    {
        "name": "delete_sprint",
        "required_fields": ["SPRINT_ID"]
    },
    {
        "name": "create_team",
        "required_fields": ["NAME"]
    },
    {
        "name": "add_user_to_team",
        "required_fields": ["TEAM_ID", "USER_ID"]
    },
    {
        "name": "create_user",
        "required_fields": ["USERNAME", "EMAIL", "PASSWORD"]
    },
    {
        "name": "create_todo",
        "required_fields": ["TASK_ID", "TITLE", "DESCRIPTION"]
    },
    {
        "name": "update_todo_status",
        "required_fields": ["TODO_ID", "STATUS"]
    }
]

def prompt_for_missing_info(actions):
    """
    Solicita al usuario los campos faltantes marcados como None.
    Valida si el valor ingresado es aceptado por la base de datos.
    """
    for action in actions:
        table = infer_table_from_action(action['action'])
        for param in action['params']:
            while True:
                current_value = action['params'][param]

                # Si ya hay valor, intentamos validarlo directamente
                if current_value is not None:
                    validated = validate_field_value(table, param, current_value)
                    if validated is not None:
                        action['params'][param] = validated
                        break
                    else:
                        print(f"⚠️ El valor actual de '{param}' es inválido.")

    return actions

def infer_table_from_action(action_name):
    """
    Dada una acción como 'create_task', deduce a qué tabla se refiere.
    Esto permite aplicar validaciones específicas por tabla.
    """
    if "task" in action_name:
        return "TASKS"
    elif "project" in action_name:
        return "PROJECTS"
    elif "sprint" in action_name:
        return "SPRINTS"
    elif "user" in action_name:
        return "USERS"
    elif "team" in action_name:
        return "TEAMS"
    return ""  # Por defecto vacío
