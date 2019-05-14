from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Email, Length


# 表单基类
class BaseForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)],
                           render_kw={'class': 'form-control', 'placeholder': "请输入用户名"})
    password = PasswordField('密码', validators=[DataRequired()],
                             render_kw={'class': 'form-control', 'placeholder': "请确认密码"})


# 注册表单类
class RegisterForm(BaseForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()],
                        render_kw={'class': 'form-control', 'placeholder': '请输入邮箱'})
    confirm_pwd = PasswordField('密码', validators=[DataRequired()],
                                render_kw={'class': 'form-control', 'placeholder': "请确认密码"})
    register = SubmitField('注册', render_kw={'class': ['form-control', 'btn'], 'value': '注册'})


# 登陆表单类
class LoginForm(BaseForm):
    login = SubmitField('登陆', render_kw={'class': ['form-control', 'btn'], 'value': '登陆'})


# 文章分类表单类
class CategoryForm(FlaskForm):
    category = StringField('分类', validators=[DataRequired()],
                           render_kw={'class': 'form-control', 'placeholder': '文章分类'})


# 文章表单类
class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()],
                        render_kw={'class': 'form-control', 'placeholder': '请输入文章标题'})
    body = CKEditorField('正文', validators=[DataRequired()],
                         render_kw={'class': 'form-control', 'placeholder': '请输入正文'})
    submit = SubmitField('提交', render_kw={'class': ['form-control', 'btn'], 'value': '提交'})
