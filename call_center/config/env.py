# config/env.py
"""
Environment configuration and loading utilities
"""

import os
from pathlib import Path
from decouple import config

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

def load_dotenv():
    """
    Load environment variables from .env file
    """
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        from decouple import Config, RepositoryEnv
        env_config = Config(RepositoryEnv(str(env_file)))
        return env_config
    return None

def get_env():
    """Get current environment"""
    return config('DJANGO_ENV', default='development')

def is_development():
    """Check if in development environment"""
    return get_env() == 'development'

def is_production():
    """Check if in production environment"""
    return get_env() == 'production'

def is_testing():
    """Check if in testing environment"""
    return get_env() == 'test'

# Load environment variables
load_dotenv()