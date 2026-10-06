from flask import Flask, redirect, url_for

from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.professor import professor_bp
    from routes.aluno import aluno_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(professor_bp, url_prefix='/professor')
    app.register_blueprint(aluno_bp, url_prefix='/aluno')

    @app.route('/')
    def inicio():
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    create_app().run(debug=True)