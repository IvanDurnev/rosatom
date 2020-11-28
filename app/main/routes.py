from app.main import bp
from flask import render_template
from flask_login import login_required
from app.main.forms import CreateOrder
from app.models import OrderTypes, Tag


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    title = 'Главная'
    create_order_form = CreateOrder()
    for order_type in OrderTypes.query.all():
        create_order_form.type.choices.append((str(order_type.id), order_type.title))
    for tag in Tag.query.all():
        create_order_form.executors.choices.append((str(tag.id), tag.name))
    if create_order_form.validate_on_submit():
        print('окей')
    return render_template('main/index.html',
                           title=title,
                           create_order_form=create_order_form)
