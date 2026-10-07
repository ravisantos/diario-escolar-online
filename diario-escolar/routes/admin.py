from flask import Blueprint, render_template

from routes.decorators import login_obrigatorio

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_obrigatorio('admin')
def dashboard():
    return render_template('admin/dashboard.html')
