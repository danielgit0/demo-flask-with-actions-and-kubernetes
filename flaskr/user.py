from flask import (
    Blueprint, jsonify
)

bp = Blueprint('user', __name__)


@bp.route('/')
def index():
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})
