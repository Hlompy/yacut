import string
import random

from http import HTTPStatus

from flask import flash, redirect, render_template

from . import app, db
from .forms import CutForm
from .models import URLMap


def get_unique_short_id():
    source_symbols = string.ascii_letters + string.digits
    short_link = ''.join(random.choice(source_symbols)
                         for __ in range(6))
    if URLMap.query.filter_by(short=short_link).first():
        return get_unique_short_id()
    return short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('index.html', form=form)
        if not custom_id:
            custom_id = get_unique_short_id()
        links = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(links)
        db.session.commit()
        return (render_template('index.html', form=form, short=custom_id),
                HTTPStatus.OK)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    original_url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(original_url.original)
