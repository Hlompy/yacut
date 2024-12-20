from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import REG


class CutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL(message='Введите ссылку целиком')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=16,
                           message='Длина ссылки должна быть до 16 символов'),
                    Regexp(REG,
                           message='Только латинские буквы и цифры'),
                    Optional()]
    )
    submit = SubmitField('Создать')
