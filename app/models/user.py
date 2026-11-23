import secrets

import bcrypt
from flask import session

from app.extensions import db


class User(db.Model):
    """Lớp trừu tượng User. Các phương thức in nghiêng trong UML do lớp con cài đặt."""
    __tablename__ = "users"

    user_id = db.Column(db.String(20), primary_key=True)         
    full_name = db.Column(db.String(100), nullable=False)         
    password_hash = db.Column(db.String(128), nullable=False)    
    date_of_birth = db.Column(db.Date)                           
    email = db.Column(db.String(120), unique=True)               
    role = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {"polymorphic_on": role, "polymorphic_identity": "user"}

    def set_password(self, raw: str) -> None:
        self.password_hash = bcrypt.hashpw(raw.encode(), bcrypt.gensalt()).decode()

    def check_password(self, raw: str) -> bool:
        return bcrypt.checkpw(raw.encode(), self.password_hash.encode())

   
    def login(self, user_id: str, password: str) -> bool:
        return self.user_id == user_id and self.check_password(password)

    
    def logout(self) -> None:
        session.clear()

   
    def reset_password(self, email: str) -> bool:
        if email != self.email:
            return False
        self.set_password(secrets.token_urlsafe(8))   
        return True

   
    def search_course(self, keyword: str = ""):
        raise NotImplementedError

    def classes_info(self, class_id: str):
        raise NotImplementedError
   
    def view_schedule(self):
        raise NotImplementedError

class Student(User):
    major = db.Column(db.String(100))            
    enrollment_year = db.Column(db.Integer)       
    __mapper_args__ = {"polymorphic_identity": "student"}

    def search_course(self, keyword: str = ""):
        from app.services import search_service
        return search_service.search_courses(keyword)

    def classes_info(self, class_id: str):
        from app.services import class_service
        return class_service.get_class(class_id)

    def view_schedule(self):
        from app.services import class_service
        return class_service.get_timetable(self.user_id)[1]

  
    def add_to_wishlist(self, course_id: str) -> bool:
        from app.services import wishlist_service
        return wishlist_service.add_to_wishlist(self.user_id, course_id).ok


    def register_class(self, class_id: str):
        from app.services import registration_service
        return registration_service.register_class(self.user_id, class_id)


    def make_payment(self, amount: int | None = None, payment_id: str | None = None):
        from app.services import payment_service
        return payment_service.make_payment(self.user_id)

class Lecturer(User):
    department = db.Column(db.String(100))
    academic_title = db.Column(db.String(50))
    __mapper_args__ = {"polymorphic_identity": "lecturer"}

    def search_course(self, keyword: str = ""):
        from app.services import search_service
        return search_service.search_courses(keyword)

    def classes_info(self, class_id: str):
        from app.services import class_service
        return class_service.get_class(class_id)

    def view_schedule(self):
        from app.services import class_service
        return class_service.get_timetable(self.user_id)[1]
class Administrator(User):
    admin_level = db.Column(db.String(50))
    __mapper_args__ = {"polymorphic_identity": "admin"}

    def search_course(self, keyword: str = ""):
        from app.services import search_service
        return search_service.search_courses(keyword)

    def classes_info(self, class_id: str):
        from app.services import class_service
        return class_service.get_class(class_id)

    def view_schedule(self):
        from app.services import class_service
        return class_service.get_timetable(self.user_id)[1]
