from flask import (
    Blueprint, request, session, jsonify
)

from server.management.train_manager import TrainManager


def construct_train_blueprint(train_manager: TrainManager):
    bp = Blueprint('train', __name__, url_prefix='/train')

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

    return bp
