# main.py
import os
from app import create_app

config_class = os.getenv('FLASK_CONFIG', 'app.config.base.BaseConfig')
app = create_app(config_class)

if __name__ == '__main__':
    app.run()