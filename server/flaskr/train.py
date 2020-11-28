
from flask import (
    Blueprint, request, session, jsonify, abort
)
from flask_cors import CORS, cross_origin

from flaskr.utils import process_response
from server.management.train_manager import TrainManager

DEFAULT_SCORE_LIMIT = 5


def _convert_partition_name_to_partition_id(partition_name: str) -> int:
    partition_name = partition_name.lower()
    if partition_name == "high":
        return 3
    elif partition_name == "medium":
        return 2
    elif partition_name == "low":
        return 1
    else:
        return 0


def construct_train_blueprint(train_manager: TrainManager):
    bp = Blueprint('train', __name__, url_prefix='/train')


    CORS(bp, resources={r"/train*": {"origins": "http://localhost/*"}},headers=['Content-Type', 'Authorization'],
     expose_headers='Authorization')


    @bp.route('/article', methods=['GET'])
    def get_random_article():
        if 'username' not in session:
            response = process_response(False)
            return response, 403

        random_article = train_manager.get_random_article()
        session['last_article'] = random_article.id
        response = process_response(random_article)
        return response, 200

    @bp.route('/article/last', methods=['GET'])
    def get_article():
        if 'username' not in session:
            response = process_response(False)
            return response, 403
        if 'last_article' in session:
            last_article = train_manager.get_article(session['last_article'])
            response = process_response(last_article)
            return response, 200
        else:
            response = process_response('Not last article available')
            return response, 406

    @bp.route('/article', methods=['POST'])
    @cross_origin(origin='http://localhost/*', headers=['Content- Type', 'Authorization'])
    def add_user_answer():
        if 'username' not in session:
            response = process_response('User not logged in')
            return response, 403

        if 'last_article' not in session:
            response = process_response('An article has not been retrieved before.')
            return response, 400

        json_request = request.get_json(force=True)
        if 'impact' in json_request:
            impact = json_request['impact']
            score = train_manager.answer_from_user(session['username'], session['last_article'], impact)
            del session['last_article']
            response = process_response(score.to_json(), authorization__required=True)
            return response, 200
        else:
            response = process_response('param "quartile" is not in the request', authorization__required=True)
            return response, 400

    @bp.route('/score/<partition>', methods=['GET'])
    @bp.route('/score/<partition>/<int:limit>', methods=['GET'])
    def get_quartile_score(partition, limit=DEFAULT_SCORE_LIMIT):
        if 'username' not in session:
            abort(403)
        partition_id = _convert_partition_name_to_partition_id(partition)

        if partition_id == 0:
            abort(400)

        user_scores = train_manager.get_quartile_score(session['username'], partition_id, limit)
        return user_scores.to_json()

    @bp.route('/score/table', methods=['GET'])
    @bp.route('/score/table/<int:limit>', methods=['GET'])
    def get_table(limit=DEFAULT_SCORE_LIMIT):
        if 'username' not in session:
            abort(403)

        table_scores = train_manager.get_user_score_table(session['username'], limit)
        return table_scores

    return bp


