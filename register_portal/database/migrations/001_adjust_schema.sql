-- Cho phép sinh viên mới đăng ký chưa có điểm
ALTER TABLE enrollment
  ALTER COLUMN midTermGrade DROP NOT NULL,
  ALTER COLUMN finalGrade DROP NOT NULL;

-- Sửa lỗi gõ nhầm tên cột
ALTER TABLE wishlistRecord RENAME COLUMN whistListId TO wishlistId;
