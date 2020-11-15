from flask import (
    Blueprint, request, session
)

from flask import jsonify
from server.db.database_manager import DatabaseManager
from server.flaskr.db import get_db
from server.management.train_manager import TrainManager
from server.management.user_manager import UserManager

bp = Blueprint('user', __name__, url_prefix='/train')
database_manger = DatabaseManager(get_db('db/peer_review.db'))
user_manager = UserManager(database_manger)


@bp.route('/user', methods=['GET'])
def get_user():
    if request.method == 'GET':
        random_article = user_manager.get_user(id_user)
        session['last_article'] = random_article.id

        return jsonify(random_article)

@bp.route('/user', methods=['POST'])
def add_user_answer():
    if request.method == 'POST':
        quartile = request.args.get('quartile')
        score = train_manager.answer_from_user(session['username'], session['last_article'], quartile)

        return jsonify(score)

