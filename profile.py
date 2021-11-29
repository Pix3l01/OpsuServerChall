from flask import Blueprint, render_template
from flask_login import login_required, current_user

profile = Blueprint('profile', __name__, template_folder='templates')

@profile.route('/profile')
@login_required
def profilePage():
    return render_template('profile.html', name=current_user.username)