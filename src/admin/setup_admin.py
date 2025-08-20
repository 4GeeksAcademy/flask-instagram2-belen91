import os
from admin.secure_model import SecureModelView
from flask_admin import Admin
from models import db, User


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(SecureModelView(User, db.session))
