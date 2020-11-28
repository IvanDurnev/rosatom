from app import db
from app.main import bp
from flask import render_template, request, redirect, jsonify
from flask_login import login_required, current_user
from app.main.forms import CreateOrder
from app.models import OrderTypes, Tag, Order
from werkzeug.utils import secure_filename
from config import Config
import os
import subprocess
import random
import speech_recognition as sr
import json


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
        print(request.form)
        all_fields = request.form
        custom_fields = {}
        for field in all_fields:
            if 'field' in field.split('-'):
                custom_fields[field.split('-')[0]] = all_fields[field]

        order = Order()
        order.creator = current_user.id
        order.title = create_order_form.title.data
        order.description = create_order_form.description.data
        order.description_sound = create_order_form.file.data
        order.priority = create_order_form.priority.data
        order.type = create_order_form.type.data
        order.interval = create_order_form.interval.data
        order.deadline = create_order_form.deadline.data

        for field in all_fields:
            if 'file_id' in field:
                order.description_sound = os.path.join(Config.UPLOAD_FOLDER, f'{all_fields["file_id"]}sound.wav')
                # print(os.path.join(Config.UPLOAD_FOLDER, f'{all_fields["file_id"]}sound.wav'))

        order.status = 1

        tag = Tag.query.filter(Tag.id == create_order_form.executors.data).first()
        for user in tag.users:
            order.executors.append(user)

        order.reactions = json.dumps(custom_fields)

        db.session.add(order)
        db.session.commit()
        return redirect(request.referrer)
    return render_template('main/index.html',
                           title=title,
                           create_order_form=create_order_form,
                           orders_iam_creator=orders_iam_creator,
                           orders_iam_executor=orders_iam_executor)


@bp.route('/recognize_file', methods=['GET', 'POST'])
def recognize_file():
    if request.method == 'POST':
        # print(request.files)
        voice_rec = request.files['audio'] # надо взять аудиофайл из POST запроса
        rand = str(random.randint(100000,1000000))
        filename =  rand + secure_filename(voice_rec.filename)
        voice_rec.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        subprocess.run(['ffmpeg', '-i', os.path.join(Config.UPLOAD_FOLDER, filename), os.path.join(Config.UPLOAD_FOLDER, filename.replace('ogg', 'wav'))])
        with sr.AudioFile(os.path.join(Config.UPLOAD_FOLDER, filename.replace('ogg', 'wav'))) as s:
            r = sr.Recognizer()
            txt = r.listen(s)
            text = r.recognize_google(txt, language = 'ru-RU')
            return jsonify({'stt': text, 'file_id': int(rand)})
