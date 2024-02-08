from .app_creator import create_app
from .config import create_config

app = create_app(create_config())
