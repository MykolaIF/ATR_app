from flask import Blueprint

# Створення Blueprint для user_dashboard
user_bp = Blueprint('user_dashboard', __name__)

from . import routes
