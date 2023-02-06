import os
from factory import create_app


if __name__ == "__main__":
    # WORK_ENV = 'prod', 'test' or 'dev' -> See config.py
    app = create_app(os.getenv('WORK_ENV') or 'dev')
    app.run(host='0.0.0.0')