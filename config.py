import os


class Config:
    DEBUG = False
    SECRET_KEY = "F0RM$YoWnAP@P=run1N[pyTH0n^N1whERE]*just4FUN"
    FILECACHEDIR = os.getenv("FILECACHEDIR") or "filecachedir"
    UPLOAD_FOLDER = FILECACHEDIR
    # 设置最大允许上传文件大小100MB，可在应用初始化时动态调整
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024

    @staticmethod
    def init_app(app):
        if not os.path.exists(Config.FILECACHEDIR):
            os.mkdir(Config.FILECACHEDIR)
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
