from flask import (
    Blueprint, request, session
)

from flask import jsonify
from server.db.database_manager import DatabaseManager
from server.flaskr.db import get_db
from server.management.train_manager import TrainManager

bp = Blueprint('train', __name__, url_prefix='/train')
database_manger = DatabaseManager(get_db('db/peer_review.db'))
train_manager = TrainManager(database_manger)


@bp.route('/article', methods=['GET'])
def get_article():
    if request.method == 'GET':
        random_article = train_manager.get_random_article()
        session['last_article'] = random_article.id

        return jsonify(random_article)

@bp.route('/article', methods=['PUT'])
def add_user_answer():
    if request.method == 'PUT':
        quartile = request.args.get('quartile')
        score = train_manager.answer_from_user(session['username'], session['last_article'], quartile)

        return jsonify(score)

