-- Trong seed.sql cột currentEnrollment đều là 0 dù đã có lượt đăng ký.
-- Đồng bộ lại theo số lượt đăng ký thực tế.
UPDATE classSection AS cs
SET currentEnrollment = (
    SELECT COUNT(*) FROM enrollment e
    WHERE e.classId = cs.classId AND e.status = 'ENROLLED'
);
