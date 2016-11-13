class Config:
    SECRET_KEY = 'greatunihack'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{}/{}".format(
        'localhost',
        'harras_block'
    )


class ProdConfig(Config):
    pass
    # if 'RDS_USERNAME' in os.environ:
    #     SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    #         os.environ['RDS_USERNAME'],
    #         os.environ['RDS_PASSWORD'],
    #         os.environ['RDS_HOSTNAME'],
    #         os.environ['RDS_PORT'],
    #         os.environ['RDS_DBNAME']
    #     )
    # else:
    #     raise KeyError('No environment variables for database connectivity')

config = {
    'dev': DevConfig,
    'pro': ProdConfig,
    'default': DevConfig

}
