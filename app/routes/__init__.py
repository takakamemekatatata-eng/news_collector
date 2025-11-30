# app/routes/__init__.py

from .articles import bp as articles_bp
from .feeds import bp as feeds_bp

def register_routes(app):
    app.register_blueprint(articles_bp)
    app.register_blueprint(feeds_bp)
