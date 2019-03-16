# coding=utf-8

from flask.ext.wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import DataRequired
from flask.ext.pagedown.fields import PageDownField
from flask_babel import gettext as _


class PostForm(FlaskForm):
    title = StringField(label=_(u"标题"), validators=[DataRequired()])
    body = PageDownField(label=_(u"正文"), validators=[DataRequired()])
    submit = SubmitField(_(u"发表"))


class CommentForm(FlaskForm):
    body = PageDownField(label=_(u'评论'), validators=[DataRequired()])
    submit = SubmitField(_(u'发表'))


class CardForm(FlaskForm):
    code = StringField(label=_(u'CODE码'), validators=[DataRequired()])
    count = IntegerField(label=_(u'数量'), validators=[DataRequired()])
    submit = SubmitField(_(u'生成'))