CREATE TABLE administrator (
    adminId CHAR(5) PRIMARY KEY,
    fullName VARCHAR(50) NOT NULL,
    passwordHash CHAR(60) NOT NULL,
    dateOfBirth DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    adminRole VARCHAR(100) NOT NULL
);





CREATE TABLE lecturer (
    lecturerId CHAR(5) PRIMARY KEY,
    fullName VARCHAR(50) NOT NULL,
    passwordHash CHAR(60) NOT NULL,
    dateOfBirth DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL
);

CREATE TABLE student (
    studentId CHAR(5) PRIMARY KEY,
    fullName VARCHAR(50) NOT NULL,
    passwordHash CHAR(60) NOT NULL,
    dateOfBirth DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    enrollmentYear INTEGER NOT NULL,
    major VARCHAR(100) NOT NULL
);

CREATE TABLE course (
    courseId CHAR(5) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL,
    adminId CHAR(5) NOT NULL,
    CONSTRAINT fk_course_admin
        FOREIGN KEY (adminId)
        REFERENCES administrator(adminId)
);

CREATE TABLE registrationTerm (
    termId VARCHAR(10) PRIMARY KEY,
    semesterName CHAR(10) NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    registrationOpen DATE NOT NULL,
    registrationClose DATE NOT NULL,
    status VARCHAR(10) NOT NULL,
    adminId CHAR(5) NOT NULL,
    CONSTRAINT fk_term_admin
        FOREIGN KEY (adminId)
        REFERENCES administrator(adminId)
);

CREATE TABLE classSection (
    classId CHAR(5) PRIMARY KEY,
    currentEnrollment INTEGER NOT NULL,
    scheduleTime TIMESTAMPTZ NOT NULL,
    room CHAR(4) NOT NULL,
    maxCapacity INTEGER NOT NULL,
    termId VARCHAR(10) NOT NULL,
    courseId CHAR(5) NOT NULL,
    lecturerId CHAR(5) NOT NULL,
    CONSTRAINT fk_section_term
        FOREIGN KEY (termId)
        REFERENCES registrationTerm(termId),
    CONSTRAINT fk_section_course
        FOREIGN KEY (courseId)
        REFERENCES course(courseId),
    CONSTRAINT fk_section_lecturer
        FOREIGN KEY (lecturerId)
        REFERENCES lecturer(lecturerId)
);

CREATE TABLE enrollment (
    enrollmentId CHAR(5) PRIMARY KEY,
    enrolledAt DATE NOT NULL,
    status VARCHAR(100) NOT NULL,
    midTermGrade REAL NOT NULL,
    finalGrade REAL NOT NULL,
    classId CHAR(5) NOT NULL,
    studentId CHAR(5) NOT NULL,
    CONSTRAINT fk_enrollment_class
        FOREIGN KEY (classId)
        REFERENCES classSection(classId),
    CONSTRAINT fk_enrollment_student
        FOREIGN KEY (studentId)
        REFERENCES student(studentId),
    CONSTRAINT uq_enrollment_class_student
        UNIQUE (classId, studentId)
);

CREATE TABLE wishlistRecord (
    whistListId INTEGER PRIMARY KEY,
    addedDate DATE NOT NULL,
    approvalStatus VARCHAR(100) NOT NULL,
    studentId CHAR(5) NOT NULL,
    courseId CHAR(5) NOT NULL,
    CONSTRAINT fk_wishlist_student
        FOREIGN KEY (studentId)
        REFERENCES student(studentId),
    CONSTRAINT fk_wishlist_course
        FOREIGN KEY (courseId)
        REFERENCES course(courseId)
);

CREATE TABLE payment (
    transactionId INTEGER PRIMARY KEY,
    amount REAL NOT NULL,
    paymentDate DATE NOT NULL,
    status VARCHAR(100) NOT NULL,
    studentId CHAR(5) NOT NULL,
    CONSTRAINT fk_payment_student
        FOREIGN KEY (studentId)
        REFERENCES student(studentId)
);
