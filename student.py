class Student:
    def __init__(self, major, enrollmentYear):
        self.major = major
        self.enrollmentYear = enrollmentYear
    def addToWishlist(self, courseId):
        print("Added course:", courseId)
        return True
    def registerClass(self, classId):
        print("Registered class:", classId)
        return True
    def makePayment(self, amount, paymentId):
        if amount > 0:
            print("Payment successful")
            return True
        else:
            print("Payment failed")
            return False
