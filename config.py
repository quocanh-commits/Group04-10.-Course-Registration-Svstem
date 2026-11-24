import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("Thiếu DATABASE_URL. Hãy chạy bằng: docker compose up --build")

    MAX_CREDITS = 24
    TUITION_PER_CREDIT = 1250000
    DEFAULT_PASSWORD = "123456"      # mật khẩu ban đầu khi admin tạo hoặc đặt lại tài khoản
