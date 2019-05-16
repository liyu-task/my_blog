import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', '12345678')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_WIDTH = '150em'
    CKEDITOR_HEIGHT = '50em'
    CKEDITOR_LANGUAGE = 'zh-cn'

    POST_PER_PAGE = 5


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data-dev.db'))


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}