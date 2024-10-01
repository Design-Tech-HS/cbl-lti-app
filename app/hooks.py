"""Global hooks"""
from flask import g, render_template
from app.models import SystemSettings
from app.extensions import db

def check_data_update_mode():
    """Function to check data update mode before each request."""
    data_update_mode = db.session.query(SystemSettings).filter_by(key='data_update_mode').first()
    if data_update_mode and data_update_mode.value == 'true':
        g.data_update_mode = True
        return render_template('data_update.html')
    g.data_update_mode = False
