# End-to-End Testing Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Django 5.1](https://img.shields.io/badge/django-5.1-green)](https://www.djangoproject.com/)
[![DRF 3.15](https://img.shields.io/badge/drf-3.15-red)](https://www.django-rest-framework.org/)

A comprehensive Django-based framework for automated end-to-end API testing across multiple environments.

## 🚀 Features

- **Environment-Aware Testing** - Auto-detects dev/staging/local configurations
- **Secure Credential Management** - `.env`-based authentication with role support
- **Declarative Endpoint Definition** - Clean endpoint configuration with path parameters
- **Atomic Test Scenarios** - Isolated, self-cleaning test cases
- **Detailed Execution Logging** - Step-by-step tracking with timestamps

## 📦 Requirements

```text
Django==5.1
requests==2.32.3
djangorestframework==3.15.2
drf-yasg==1.21.8
python-dotenv==1.0.1
```


# 🏗️ Project Architecture
```text
vion-test-senario/
├── any_new_test_module/    # Test module template
│   ├── scenarios.py       # Test cases
│   ├── endpoints.py       # API routes
├── scenario_tester/       # Core framework
│   ├── assertions.py      # Validation tools
│   ├── credentials.py     # Auth handling
│   ├── endpoints.py       # Base endpoint class
│   ├── scenarios.py       # Base scenario logic
│   ├── services.py        # Shared utilities
│   └── utils.py           # Helper functions
├── test_api_vion/         # API test config
│   ├── settings.py        # Framework settings  
│   └── swagger.py         # API documentation
.env                       # Environment variables
manage.py                  # Django CLI
```

## 🔒 Authentication & Environment Setup

### 1. Environment Configuration (`.env`)
```ini
# Development Environment
DEV_USERNAME_BACKOFFICE="admin@dev.com"
DEV_PASSWORD_BACKOFFICE="devpass123"
DEV_USERNAME_PARTNER1="partner1@dev.com"
DEV_PASSWORD_PARTNER1="partner123"

# Staging Environment
STAGING_USERNAME_BACKOFFICE="admin@stage.com"
STAGING_PASSWORD_BACKOFFICE="stagepass456"
STAGING_USERNAME_PARTNER1="partner2@stage.com"
STAGING_PASSWORD_PARTNER1="stagepass789"

# Local Testing
LOCAL_USERNAME_BACKOFFICE="tester@local"
LOCAL_PASSWORD_BACKOFFICE="testpass000"
LOCAL_USERNAME_PARTNER1="partner2@stage.com"
LOCAL_PASSWORD_PARTNER1="stagepass789"
```
### 2. Credential Mapping (`credentials.py`)
```ini
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

CREDENTIALS = {
    "development": {
        "backoffice": {
            "username": os.getenv("DEV_USERNAME_BACKOFFICE"),
            "password": os.getenv("DEV_PASSWORD_BACKOFFICE"),
        },
        "partner1": {
            "username": os.getenv("DEV_USERNAME_PARTNER1"),
            "password": os.getenv("DEV_PASSWORD_PARTNER1"),
        }
    },
    "staging": {
        "backoffice": {
            "username": os.getenv("STAGING_USERNAME_BACKOFFICE"),
            "password": os.getenv("STAGING_PASSWORD_BACKOFFICE"),
        },
        "partner1": {
            "username": os.getenv("STAGING_USERNAME_PARTNER1"),
            "password": os.getenv("STAGING_PASSWORD_PARTNER1"),
        }
    },
    "local": {
        "backoffice": {
            "username": os.getenv("LOCAL_USERNAME_BACKOFFICE"),
            "password": os.getenv("LOCAL_PASSWORD_BACKOFFICE"),
        },
        "partner1": {
            "username": os.getenv("LOCAL_USERNAME_PARTNER1"),
            "password": os.getenv("LOCAL_PASSWORD_PARTNER1"),
        }
    }
}
```
