import re
from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id

REG = '^[A-Za-z0-9]*$'


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    original = data.get('url')
    if not original:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_short = data.get('custom_id')
    if custom_short:
        if len(custom_short) > 16 or not re.match(REG,
                                                  custom_short):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_short).first():
            raise InvalidAPIUsage(f'Имя "{custom_short}" уже занято.')

    else:
        custom_short = get_unique_short_id()
    links = URLMap(
        original=original,
        short=custom_short
    )
    db.session.add(links)
    db.session.commit()
    return jsonify(links.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_short_link(short):
    original_link = URLMap.query.filter_by(short=short).first()
    if original_link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': original_link.original}), 200
