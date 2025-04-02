from openai import OpenAI
import os
from dotenv import load_dotenv
from db_schema import db_schema, action_schema

# Cargar API key de OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_prompt(user_input):
    # Construir el esquema de acciones de forma detallada y explícita
    action_descriptions = """
Action Schema:
- create_task:
    Required fields: NAME, DESCRIPTION, PRIORITY, ESTIMATED_FINISH_DATE
    Optional fields: ASSIGNED_USER_ID, SPRINT_ID, PROJECT_ID
- update_task_status:
    Required fields: TASK_ID, STATUS
- assign_user_to_task:
    Required fields: TASK_ID, USER_ID
- update_task:
    Required fields: TASK_ID
    Optional fields: NAME, DESCRIPTION, PRIORITY, ESTIMATED_FINISH_DATE, STATUS, SPRINT_ID, USER_ID
- delete_task:
    Required fields: TASK_ID
- create_project:
    Required fields: NAME, DESCRIPTION
- update_project:
    Required fields: PROJECT_ID
    Optional fields: NAME, DESCRIPTION
- delete_project:
    Required fields: PROJECT_ID
- create_sprint:
    Required fields: NAME, DESCRIPTION, START_DATE, END_DATE, PROJECT_ID
- update_sprint:
    Required fields: SPRINT_ID
    Campos opcionales: NAME, DESCRIPTION, START_DATE, END_DATE, STATUS
- delete_sprint:
    Required fields: SPRINT_ID
- create_team:
    Required fields: NAME
- add_user_to_team:
    Required fields: TEAM_ID, USER_ID
- create_user:
    Required fields: USERNAME, EMAIL, PASSWORD
- create_todo:
    Required fields: TASK_ID, TITLE, DESCRIPTION
- update_todo_status:
    Required fields: TODO_ID, STATUS
"""

    # Nuevo prompt sin ejemplo fijo de salida
    return f"""
Your task is to interpret the following user instruction and transfrom it into a list of valid actions that the system can execute, using only the actions defined in the following schema. For each action, include a 'params' object that contains the required fields; if you cannot determine any value, assign null. Do not add any additional text outside of the JSON.
{action_descriptions}

User instruction: "{user_input}"
"""

def get_action_json(user_input):
    """
    Llama al modelo GPT con el prompt generado y devuelve la respuesta cruda.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": generate_prompt(user_input)
        }],
        temperature=0
    )
    return response.choices[0].message.content