from .app_creator import create_app
from .config import Config

configuration = Config()
app = create_app(configuration)

if __name__ == "__main__":
    app.run(debug=True)
