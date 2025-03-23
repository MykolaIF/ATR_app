from flask import Blueprint

# Створення Blueprint для admin_dashboard
admin_bp = Blueprint('admin_dashboard', __name__)

# Імпорт маршрутів
from . import routes
