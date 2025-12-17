import os

from abc import ABC

class Config(ABC):
    required_general_env_vars: list[str] = [
        'SYNC',
        'MI_CLIENT_ID'
    ]

    all_env_vars: dict[str, str | None] = os.environ


    # General
    SYNC = all_env_vars.get('SYNC')
    MI_CLIENT_ID = all_env_vars.get('MI_CLIENT_ID')


    # Adminpulse Document Sync
    ADMINPULSE_API_KEY = all_env_vars.get('ADMINPULSE_API_KEY')
    DAYS_IN_PAST = all_env_vars.get('DAYS_IN_PAST')
    MICROSOFT_TENANT_ID = all_env_vars.get('MICROSOFT_TENANT_ID')
    MICROSOFT_CLIENT_ID = all_env_vars.get('MICROSOFT_CLIENT_ID')
    MICROSOFT_CLIENT_SECRET = all_env_vars.get('MICROSOFT_CLIENT_SECRET')



    @classmethod
    def check_general_environment_variables(cls) -> None:
        missing_vars = [key for key in cls.required_general_env_vars if not cls.all_env_vars.get(key)]
        if missing_vars:
            raise Exception(f'Missing environment variables: {", ".join(missing_vars)}')
        
    
    @classmethod
    def check_detail_environment_variables(cls, required_detail_env_vars: list[str]) -> None:
        missing_vars = [key for key in required_detail_env_vars if not cls.all_env_vars.get(key)]
        if missing_vars:
            raise Exception(f'Missing environment variables: {", ".join(missing_vars)}')
        
    

