from app import db
from app.main import bp
from flask import render_template
from flask_login import login_required, current_user
from app.main.forms import CreateOrder
from app.models import OrderTypes, Tag, Order


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    title = 'Главная'

    # Я поставил
    orders_iam_creator = current_user.get_orders_iam_creator()

    # Мне поставили
    orders_iam_executor = current_user.get_orders_iam_executor()

    create_order_form = CreateOrder()
    for order_type in OrderTypes.query.all():
        create_order_form.type.choices.append((str(order_type.id), order_type.title))
    for tag in Tag.query.all():
        create_order_form.executors.choices.append((str(tag.id), tag.name))


    if create_order_form.validate_on_submit():
        order = Order()
        order.creator = current_user.id
        order.title = create_order_form.title.data
        order.description = create_order_form.description.data
        order.description_sound = create_order_form.file.data
        order.priority = create_order_form.priority.data
        order.type = create_order_form.type.data
        order.interval = create_order_form.interval.data
        order.deadline = create_order_form.deadline.data
        order.status = 1

        tag = Tag.query.filter(Tag.id == create_order_form.executors.data).first()
        for user in tag.users:
            order.executors.append(user)

        db.session.add(order)
        db.session.commit()
    return render_template('main/index.html',
                           title=title,
                           create_order_form=create_order_form,
                           orders_iam_creator=orders_iam_creator,
                           orders_iam_executor=orders_iam_executor)
