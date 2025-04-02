import json
import dateparser
from datetime import datetime

def normalize_actions(actions):
    """
    Recorre la lista de acciones y normaliza campos específicos.
    Por ejemplo, para "create_task", normaliza 'ESTIMATED_FINISH_DATE' a formato ISO.
    """
    for action in actions:
        if action.get("action") == "create_task":
            params = action.get("params", {})
            date_str = params.get("ESTIMATED_FINISH_DATE")
            if date_str:
                # Usar dateparser para convertir a datetime
                parsed_date = dateparser.parse(date_str, languages=["en", "es"])
                if parsed_date:
                    # Convertir a ISO format (sin milisegundos)
                    params["ESTIMATED_FINISH_DATE"] = parsed_date.replace(microsecond=0).isoformat()
                else:
                    # En caso de fallo, puedes optar por dejarlo en null o conservar el original
                    params["ESTIMATED_FINISH_DATE"] = None
            # Si quisieras normalizar PRIORITY (por ejemplo, convertir "urgent" a "alta"), puedes hacerlo aquí:
            priority = params.get("PRIORITY")
            if priority:
                if priority.lower() == "urgent":
                    params["PRIORITY"] = "alta"
    return actions

def parse_response(json_string):
    """
    Intenta convertir la respuesta del modelo en una estructura JSON válida.
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        print("❌ Error al procesar JSON. Asegúrate de que el modelo devuelva un formato correcto o si tu mensaje no contiene acciones validas.")
        return []

def summarize_actions(actions):
    """
    Devuelve un resumen legible de las acciones extraídas.
    """
    summary = []
    for i, action in enumerate(actions, 1):
        text = f"{i}. Action: {action['action']}\n"
        for k, v in action['params'].items():
            estado = v if v else '❓ Faltante'
            text += f"   - {k}: {estado}\n"
        summary.append(text)
    return "\n".join(summary)