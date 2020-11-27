from app.main import bp
from flask import render_template, request
from flask_login import login_required
from config import Config



@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    bot_name = Config.BOT_NAME
    stream_link = Config.STREAM_LINK
    vidget_prefix = Config.VIDGET_PREFIX
    title = 'Главная'
    if request.args:
        if 'u' in request.args:
            print(request.args['u'])
    return render_template('main/index.html',
                           bot_name=bot_name,
                           stream_link=stream_link,
                           vidget_prefix=vidget_prefix,
                           title=title,
                           yandex_verification_content=Config.YANDEX_VERIFICATION_CONTENT)
