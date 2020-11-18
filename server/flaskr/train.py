
from flask import (
    Blueprint, request, session, jsonify, abort
)

from server.management.train_manager import TrainManager


def construct_train_blueprint(train_manager: TrainManager):
    bp = Blueprint('train', __name__, url_prefix='/train')


    @bp.route('/article', methods=['GET'])
    def get_random_article():
        if 'username' not in session:
            abort(403)

        random_article = train_manager.get_random_article()
        session['last_article'] = random_article.id
        return jsonify(random_article)

    @bp.route('/article/last', methods=['GET'])
    def get_article():
        if 'username' not in session:
            abort(403)
        if 'last_article' in session:
            last_article = train_manager.get_article(session['last_article'])
            return jsonify(last_article)
        else:
            abort(406)

    @bp.route('/article', methods=['PUT'])
    def add_user_answer():
        if 'username' not in session:
            abort(403)

        if 'last_article' not in session:
            abort(400,'An article has not been retrieved before.')

        json_request = request.get_json()
        if 'quartile' in json_request:
            quartile = json_request['quartile']
            score = train_manager.answer_from_user(session['username'], session['last_article'], quartile)
            del session['last_article']
            return score.to_json()
        else:
            abort(400)

    return bp
