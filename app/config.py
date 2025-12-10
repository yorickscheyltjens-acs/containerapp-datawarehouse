import os

from abc import ABC

class Config(ABC):
    all_keys: list[str] = [
        'SYNC'
    ]

    all_env_vars: dict[str, str | None] = os.environ

    SYNC = all_env_vars.get('SYNC')


    @classmethod
    def check_environment_variables(cls) -> None:
        missing_vars = [key for key in cls.all_keys if not cls.all_env_vars.get(key)]
        if missing_vars:
            raise Exception(f'Missing environment variables: {", ".join(missing_vars)}')
