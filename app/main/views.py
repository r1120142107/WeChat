# -*- coding: utf-8 -*-

from flask import render_template, request, flash, redirect, url_for,current_app,abort, jsonify
from . import main
from .forms import PostForm,CommentForm,CardForm
from ..models import Post,Comment,Card
from .. import db
from flask.ext.login import login_required, current_user
from flask_babel import gettext as _


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.route('/')
@login_required
def index():
    #posts = Post.query.all()

    page_index = request.args.get('page', 1, type=int)

    query = Card.query.order_by(Card.id.desc())

    pagination = query.paginate(page_index, per_page=20, error_out=False)

    posts = pagination.items

    return render_template('index.html',
                           title=_(u'WeChat'),
                           posts=posts,
                           pagination=pagination)


@main.route('/services')
def services():
    return 'services'

@main.route('/about')
def about():
    return 'about'

@main.route('/user/<regex("[a-z]{3}"):user_id>')  #转换器 int fload path
def user(user_id):
    return 'User %s' % user_id

@main.route('/projects/')
@main.route('/our-works/')
def projects():
    return 'The project page'

# @main.route('/login',methods=['GET','POST'])
# def login():
#     from .forms import LoginForm
#     form = LoginForm()
#     # if request.method == 'POST':
#     #     username = request.form['username']
#     #     password = request.form['password']
#     # else:
#     #     username = "" #request.args['username']
#     flash(u'登录成功')
#     return render_template('login.html', title="登录", form=form)

# @main.route('/upload',methods=['GET','POST'])
# def upload():
#     if request.method=='POST':
#         f = request.files['file']
#         basepath = path.abspath(path.dirname(__file__))
#         upload_path = path.join(basepath,'static/uploads')
#         f.save(upload_path,secure_filename(f.filename))
#         return redirect(url_for('upload'))
#     return render_template('upload.html')


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def post(id):
    # Detail 详情页
    post = Post.query.get_or_404(id)

    # 评论窗体
    form = CommentForm()

    # 保存评论
    if form.validate_on_submit():
        comment = Comment(author=current_user,
                          body=form.body.data,
                          post=post)
        db.session.add(comment)
        db.session.commit()

    return render_template('posts/detail.html',
                           title=post.title,
                           form=form,
                           post=post)

@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()

    if id == 0:
        post = Post(author=current_user)
    else:
        post = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post', id=post.id))

    form.title.data = post.title
    form.body.data = post.body

    title = _(u'添加新文章')
    if id > 0:
        title =_(u'编辑 - %(title)',title = post.title)

    return render_template('posts/edit.html',
                           title=title,
                           form=form,
                           post=post)

@main.route('/shoutdown')
def shutdown():
    if not current_app.testing:
        abort(404)

    shoutdown = request.environ.get('werkzeug.server.shutdown')
    if not shoutdown:
        abort(500)

    shoutdown()
    return u'正在关闭服务端进程...'

@main.route('/cardedit', methods=['GET', 'POST'])
@main.route('/cardedit/<int:id>', methods=['GET', 'POST'])
@login_required
def cardedit(id=0):
    form = CardForm()

    if id == 0:
        card = Card(author=current_user)
    else:
        card = Card.query.get_or_404(id)

    if form.validate_on_submit():
        card.count = form.count.data
        card.code = form.code.data
        card.openid='test'
        card.timestamp='test'
        card.signature='test'
        card.balance=0.00

        db.session.add(card)
        db.session.commit()

        return redirect(url_for('.cardpost', id=card.id))

    form.code.data = card.code
    form.count.data = card.count

    title = _(u'code码')
    if id > 0:
        title =_(u'编辑 - %(title)',title = card.code)

    return render_template('card/edit.html',
                           title=title,
                           form=form,
                           card=card)
@main.route('/cardposts/<int:id>', methods=['GET', 'POST'])
def cardpost(id):
    # Detail 详情页
    card = Card.query.get_or_404(id)
    return render_template('card/detail.html',
                           title=card.code,
                           card=card)


@main.route('/api/cardposts/<int:id>', methods=['GET', 'POST'])
def sign(id):
    # Detail 详情页
    from ..util.wechat_sign import Sign
    appId = 'wx7b7e7bf5132ffccc'
    appSecret = 'b99531fcaac1a77a882d7bfa323740bb'
    url = 'http://renxinlei.space:8808/cardposts/<int:id>'
    sign = Sign(appId, appSecret, url)
    card = Card.query.get_or_404(id)
    return render_template('card/detail.html',
                           title=card.code,
                           card=card)




@main.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():

    return jsonify({'tasks': tasks})