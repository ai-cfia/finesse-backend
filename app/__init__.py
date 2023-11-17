from .app_creator import create_app
from .config import Config

config = Config()
app = create_app(config)

if __name__ == "__main__":
    app.run(debug=True)
