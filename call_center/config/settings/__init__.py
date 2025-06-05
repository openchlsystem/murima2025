from ..env import get_env

env = get_env()

if env == 'production':
    from .production import *
elif env == 'test':
    from .test import *
else:
    from .development import *