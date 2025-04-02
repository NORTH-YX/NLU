db_schema = {
    "TEAMS": {
        "columns": {
            "TEAM_ID": "NUMBER",
            "TEAM_NAME": "VARCHAR2(255)",
            "MANAGER_ID": "NUMBER",
            "PROJECT_ID": "NUMBER",
            "CREATION_DATE": "TIMESTAMP WITH TIME ZONE",
            "DELETED_AT": "TIMESTAMP WITH TIME ZONE"
        },
        "foreign_keys": {
            "MANAGER_ID": "USERS.USER_ID",
            "PROJECT_ID": "PROJECTS.PROJECT_ID"
        }
    },
    "PROJECTS": {
        "columns": {
            "PROJECT_ID": "NUMBER",
            "PROJECT_NAME": "VARCHAR2(255)",
            "DESCRIPTION": "VARCHAR2(255)",
            "STATUS": "VARCHAR2(60)",
            "START_DATE": "TIMESTAMP WITH TIME ZONE",
            "ESTIMATED_FINISH_DATE": "TIMESTAMP WITH TIME ZONE",
            "REAL_FINISH_DATE": "TIMESTAMP WITH TIME ZONE",
            "DELETED_AT": "TIMESTAMP WITH TIME ZONE"
        }
    },
    "USERS": {
        "columns": {
            "USER_ID": "NUMBER",
            "NAME": "VARCHAR2(255)",
            "EMAIL": "VARCHAR2(255)",
            "ROLE": "VARCHAR2(100)",
            "WORK_MODALITY": "VARCHAR2(100)",
            "TELEGRAM_ID": "VARCHAR2(100)",
            "PHONE_NUMBER": "VARCHAR2(100)",
            "PASSWORD": "VARCHAR2(255)",
            "CREATION_DATE": "TIMESTAMP WITH TIME ZONE",
            "DELETED_AT": "TIMESTAMP WITH TIME ZONE",
            "TEAM_ID": "NUMBER"
        },
        "foreign_keys": {
            "TEAM_ID": "TEAMS.TEAM_ID"
        }
    },
    "TASKS": {
        "columns": {
            "TASK_ID": "NUMBER",
            "NAME": "VARCHAR2(255)",
            "DESCRIPTION": "VARCHAR2(255)",
            "PRIORITY": "NUMBER",
            "STATUS": "VARCHAR2(50)",
            "ESTIMATED_FINISH_DATE": "TIMESTAMP WITH TIME ZONE",
            "REAL_FINISH_DATE": "TIMESTAMP WITH TIME ZONE",
            "DELETED_AT": "TIMESTAMP WITH TIME ZONE",
            "SPRINT_ID": "NUMBER",
            "USER_ID": "NUMBER"
        },
        "foreign_keys": {
            "SPRINT_ID": "SPRINTS.SPRINT_ID",
            "USER_ID": "USERS.USER_ID"
        }
    },
    "SPRINTS": {
        "columns": {
            "SPRINT_ID": "NUMBER",
            "PROJECT_ID": "NUMBER",
            "SPRINT_NAME": "VARCHAR2(255)",
            "START_DATE": "TIMESTAMP WITH TIME ZONE",
            "FINISH_DATE": "TIMESTAMP WITH TIME ZONE",
            "STATUS": "VARCHAR2(60)",
            "DELETED_AT": "TIMESTAMP WITH TIME ZONE"
        },
        "foreign_keys": {
            "PROJECT_ID": "PROJECTS.PROJECT_ID"
        }
    }
}

action_schema = [
    {
        "name": "create_task",
        "required_fields": ["NAME", "DESCRIPTION", "PRIORITY", "ESTIMATED_FINISH_DATE"],
        "optional_fields": ["ASSIGNED_USER_ID", "SPRINT_ID", "PROJECT_ID"]
    },
    {
        "name": "update_task_status",
        "required_fields": ["TASK_ID", "STATUS"]
    },
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