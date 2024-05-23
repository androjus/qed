import os
from pathlib import Path
from typing import Type


class BaseConfig:
    """
    Base Template.
    """

    BASE_PATH = Path(__file__).parent

    # celery config
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://redis:6379/0"
    )
    CELERY_IGNORE_RESULT = False
    CELERY_TASK_TRACK_STARTED = True

    MODEL_PATH = BASE_PATH / "models/repres.pickle"


class ProdConfig(BaseConfig):
    pass


class DevConfig(BaseConfig):
    pass


app_settings: str = os.environ.get("APP_SETTINGS", "DevConfig").lstrip()

Config: Type[BaseConfig]
if app_settings == "ProdConfig":
    Config = ProdConfig
elif app_settings == "DevConfig":
    Config = DevConfig
else:
    raise Exception("[ERROR] invalid_config")
