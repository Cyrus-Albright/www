class Config:
    DEBUG = False
    FILECACHEDIR = "downloadfile"

    @staticmethod
    def init_app(app):
        app.app_context().push()


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}