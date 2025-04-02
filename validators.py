"""
Este módulo contiene validaciones de campos con valores restringidos (campos tipo ENUM, STATUS, PRIORITY, ROLE, etc.),
así como la validación de campos obligatorios, campos NULL permitidos y ahora también fechas en lenguaje natural.
"""

import dateparser

# Campos con valores limitados por tabla y columna
table_constraints = {
    "TASKS": {
        "STATUS": ["To Do", "in progress", "completed"],
        "PRIORITY": ["alta", "media", "baja"]
    },
    "PROJECTS": {
        "STATUS": ["To Do", "in progress", "completed"]
    },
    "SPRINTS": {
        "STATUS": ["To Do", "in progress", "completed"]
    },
    "USERS": {
        "ROLE": ["admin", "developer", "manager"],
        "WORK_MODALITY": ["remote", "hybrid", "on-site"]
    }
}

# Campos NOT NULL según el esquema de la base de datos
required_fields_by_table = {
    "TASKS": ["TASK_NAME", "DESCRIPTION", "PRIORITY", "STATUS", "USER_ID"],
    "PROJECTS": ["PROJECT_NAME", "DESCRIPTION", "STATUS", "START_DATE"],
    "SPRINTS": ["SPRINT_NAME", "START_DATE", "FINISH_DATE", "STATUS"],
    "USERS": ["NAME", "EMAIL", "ROLE", "WORK_MODALITY", "PASSWORD"],
    "TEAMS": ["TEAM_NAME", "PROJECT_ID"]
}

# Campos que sí pueden ser nulos, aunque existan en el modelo
nullable_fields_by_table = {
    "PROJECTS": ["DELETED_AT", "REAL_FINISH_DATE"],
    "SPRINTS": ["DELETED_AT"],
    "TASKS": ["DELETED_AT", "REAL_FINISH_DATE", "ESTIMATED_HOURS", "REAL_HOURS"],
    "USERS": ["TELEGRAM_ID", "PHONE_NUMBER", "TEAM_ID", "DELETED_AT"]
}

# Campos que son tipo fecha (timestamp)
datetime_fields_by_table = {
    "TASKS": ["ESTIMATED_FINISH_DATE", "REAL_FINISH_DATE", "CREATION_DATE"],
    "PROJECTS": ["START_DATE", "ESTIMATED_FINISH_DATE", "REAL_FINISH_DATE"],
    "SPRINTS": ["START_DATE", "FINISH_DATE"],
    "USERS": ["CREATION_DATE"],
    "TEAMS": ["CREATION_DATE"]
}

def validate_field_value(table: str, field: str, value: str):
    """
    Valida si el valor pertenece al set de valores válidos definidos por la DB.
    Si el campo es tipo fecha, intenta parsearlo automáticamente con dateparser.
    Devuelve el valor normalizado o None si es inválido.
    """
    # 1. Validar tipo fecha
    if is_datetime_field(table, field):
        parsed_date = dateparser.parse(value, languages=['es', 'en'])
        if parsed_date:
            return parsed_date.isoformat()
        print(f"⚠️ No se reconoció '{parsed_date}' como una fecha válida para {table}.{field}.")
        return None


def is_field_required(table: str, field: str) -> bool:
    """Devuelve True si el campo es obligatorio (NOT NULL)."""
    return field.upper() in required_fields_by_table.get(table.upper(), [])

def is_field_nullable(table: str, field: str) -> bool:
    """Devuelve True si el campo acepta valores NULL."""
    return field.upper() in nullable_fields_by_table.get(table.upper(), [])

def is_datetime_field(table: str, field: str) -> bool:
    """Devuelve True si el campo es tipo fecha (TIMESTAMP)."""
    return field.upper() in datetime_fields_by_table.get(table.upper(), [])
