# Register Portal

## Chạy lần đầu
1. Tạo database `register_portal` trong pgAdmin.
2. Chạy lần lượt trong Query Tool (database register_portal):
   `database/schema.sql` → `database/seed.sql` → `database/migrations/001_adjust_schema.sql` → `database/migrations/002_sync_enrollment_counts.sql`
   (001 chỉ chạy MỘT lần; 002 chạy lại được.)
3. Tạo `.env` từ `.env.example` (điền mật khẩu PostgreSQL).
4. `pip install -r requirements.txt`
5. `python scripts/set_passwords.py`   (đặt mật khẩu 123456 cho mọi tài khoản trong seed)
6. `python run.py`  →  http://127.0.0.1:5000

Tài khoản thử: S0001 (Student), L0001 (Lecturer), A0001 (Administrator), mật khẩu 123456.
