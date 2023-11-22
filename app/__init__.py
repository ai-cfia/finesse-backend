from .app_creator import create_app
from .config import Config

configuration = Config()
app = create_app(configuration)
