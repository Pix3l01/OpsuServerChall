from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import desc

from bakand.db.dbClasses import db, Score, User
from bakand.utils import getMapsForProfileTable

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/profile')
@login_required
def profilePage():
    maps = getMapsForProfileTable()
    haveScored = False
    count = 0
    for i, sMap in enumerate(maps):
        sc = Score.query.filter_by(user_id=current_user.id, mid=sMap.id).order_by(desc(Score.score)).first()
        if sc is not None:
            maps[i].score = sc.score
            haveScored = True
            if maps[i].score > maps[i].toBeat:
                maps[i].done = True
                count += 1
    if count == 3:
        print(f'{current_user.username} : {current_user.guid} HA FLAGGATO!!!!', flush=True)
    return render_template('profile.html', name=current_user.username, guid=current_user.guid, maps=maps, flag='ptm{I_D!d_Th3_08fUSCati0n_bY_H4nD}', authenticated=current_user.is_authenticated, zip=zip, scored=haveScored)
