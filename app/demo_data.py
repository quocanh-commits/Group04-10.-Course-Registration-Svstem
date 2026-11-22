"""Dữ liệu giả của bản demo. TẠM THỜI: sẽ xóa khi chuyển sang dữ liệu thật từ PostgreSQL."""

COURSES = [
    {"code": "CS205.01", "name": "Object-oriented programming", "lecturer": "Vũ Quang Huy", "credits": 3,
     "schedule": "Wednesday · 13:00–15:30", "room": "Room B401", "enrolled": 36, "capacity": 45,
     "prereq": "CS101 · Passed", "prereq_ok": True, "status": "Available"},
    {"code": "CS201.02", "name": "Data structures and algorithms", "lecturer": "Trần Hoàng Nam", "credits": 3,
     "schedule": "Wednesday · 07:00–09:30", "room": "Room B201", "enrolled": 45, "capacity": 45,
     "prereq": "CS101 · Passed", "prereq_ok": True, "status": "Full"},
    {"code": "CS207.01", "name": "Computer networks", "lecturer": "Đỗ Minh Quân", "credits": 3,
     "schedule": "Monday · 07:00–09:30", "room": "Room B402", "enrolled": 32, "capacity": 45,
     "prereq": "CS101 · Passed", "prereq_ok": True, "status": "Selected"},
    {"code": "CS301.01", "name": "Artificial intelligence", "lecturer": "Nguyễn Thùy Dung", "credits": 3,
     "schedule": "Friday · 07:00–09:30", "room": "Room B501", "enrolled": 28, "capacity": 40,
     "prereq": "CS201 · Not passed", "prereq_ok": False, "status": "Selected"},
]

GRADES = [
    {"code": "CS101", "name": "Introduction to Programming", "credits": 3, "midterm": 8.5, "final": 9.0, "letter": "A", "gpa": "4.0"},
    {"code": "MA102", "name": "Discrete Mathematics", "credits": 3, "midterm": 8.0, "final": 8.2, "letter": "B+", "gpa": "3.5"},
    {"code": "CS202", "name": "Database Systems", "credits": 3, "midterm": 7.5, "final": 8.0, "letter": "B", "gpa": "3.0"},
]

ROSTER = [
    {"sid": "23010015", "name": "Nguyễn Minh Anh", "sessions": 10, "status": "Present", "midterm": 8.5, "final": 8.8},
    {"sid": "23010018", "name": "Trần Gia Bảo", "sessions": 9, "status": "Present", "midterm": 7.8, "final": 8.0},
    {"sid": "23010024", "name": "Lê Thu Hà", "sessions": 8, "status": "Excused", "midterm": 9.0, "final": 9.2},
]

ANNOUNCEMENTS = [
    {"class_code": "CS205.01", "title": "Lab room change for Week 4", "date": "14/09/2026",
     "body": "Please move to Lab A204 for the OOP practice session."},
    {"class_code": "CS207.01", "title": "Packet Tracer assignment due Friday", "date": "12/09/2026",
     "body": "Submit your VLAN topology file before 23:59."},
]

PERIODS = [
    {"name": "Phase 1 · Planned registration", "window": "24/08–04/09/2026", "max_credits": 24, "status": "Closed"},
    {"name": "Phase 2 · Add/drop period", "window": "07/09–18/09/2026", "max_credits": 24, "status": "Open"},
]

ACCOUNTS = [
    {"username": "23010015", "name": "Nguyễn Minh Anh", "role": "Student", "status": "Active"},
    {"username": "GV014", "name": "Vũ Quang Huy", "role": "Lecturer", "status": "Active"},
    {"username": "ADMIN01", "name": "Phạm Quốc Khánh", "role": "Administrator", "status": "Active"},
]

# Trạng thái thay đổi được (trước đây là biến global trong app.py)
STATE = {
    "tuition_paid": 7500000,
    "confirmed_msg": "",
}
