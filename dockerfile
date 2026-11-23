FROM python:3.11-slim

# Ngăn Python tạo file .pyc và xuất log trực tiếp ra terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cài đặt thư viện hệ thống cần thiết cho PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt các thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

EXPOSE 5000

# Chạy ứng dụng Flask
CMD ["flask", "--app", "run.py", "run", "--host=0.0.0.0", "--port=5000"]