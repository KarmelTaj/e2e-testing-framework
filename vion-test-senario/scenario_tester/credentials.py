import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS = {
    "development": {
        "backoffice": {
            "username": os.getenv("VION_DEV_USERNAME_BACKOFFICE"),
            "password": os.getenv("VION_DEV_PASSWORD_BACKOFFICE"),
        },
        "partner1": {
            "username": os.getenv("VION_DEV_USERNAME_PARTNER1"),
            "password": os.getenv("VION_DEV_PASSWORD_PARTNER1"),
        },
        "partner2": {
            "username": os.getenv("VION_DEV_USERNAME_PARTNER2"),
            "password": os.getenv("VION_DEV_PASSWORD_PARTNER2"),
        },
    },
    "staging": {
        "backoffice": {
            "username": os.getenv("VION_STAGING_USERNAME_BACKOFFICE"),
            "password": os.getenv("VION_STAGING_PASSWORD_BACKOFFICE"),
        },
        "partner1": {
            "username": os.getenv("VION_STAGING_USERNAME_PARTNER1"),
            "password": os.getenv("VION_STAGING_PASSWORD_PARTNER1"),
        },
        "partner2": {
            "username": os.getenv("VION_STAGING_USERNAME_PARTNER2"),
            "password": os.getenv("VION_STAGING_PASSWORD_PARTNER2"),
        },
    },
    "local": {
        "backoffice": {
            "username": os.getenv("VION_LOCAL_USERNAME_BACKOFFICE"),
            "password": os.getenv("VION_LOCAL_PASSWORD_BACKOFFICE"),
        },
        "partner1": {
            "username": os.getenv("VION_LOCAL_USERNAME_PARTNER1"),
            "password": os.getenv("VION_LOCAL_PASSWORD_PARTNER1"),
        },
        "partner2": {
            "username": os.getenv("VION_LOCAL_USERNAME_PARTNER2"),
            "password": os.getenv("VION_LOCAL_PASSWORD_PARTNER2"),
        },
    },
}
