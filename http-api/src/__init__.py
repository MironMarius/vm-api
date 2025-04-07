from flask import Flask
from src.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DatabaseSessionHolder:
    session = None

db = DatabaseSessionHolder()

def __create_db_session(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    return scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.session = __create_db_session(app)

    # shutdown session gracefully
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if db.session:
            db.session.remove()

    with app.app_context():
        from src.routes import register_routes
        register_routes(app)

    return app

app = create_app(Config)




