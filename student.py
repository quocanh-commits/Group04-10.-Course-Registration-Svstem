
class Student:
    def __init__(self, major, enrollmentYear):
        self.major = major
        self.enrollmentYear = enrollmentYear
    # Add course to wishlist
    def addToWishlist(self, courseId):
        if courseId != "":
            print("Course added to wishlist:", courseId)
            return True
        else:
            return False
    # Register class
    def registerClass(self, classId):
        if classId != "":
            print("Class registration successful:", classId)
            return {
                "status": "Successful",
                "classId": classId
            }
        else:
            return {
                "status": "Failed",
                "message": "Invalid class ID"
            }
    # Make payment
    def makePayment(self, amount, paymentId):
        if amount > 0 and paymentId != "":
            print("Payment successful")
            return {
                "status": "Paid",
                "amount": amount,
                "paymentId": paymentId
            }
        else:
            return {
                "status": "Failed",
                "message": "Invalid payment information"
            }
