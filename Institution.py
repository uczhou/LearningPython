

class Institution:

    def __init__(self, name):
        self.name = name.upper()
        self.students = {}
        self.instructors = {}
        self.course_catalog = {}
        self.course_schedule = {}

    def list_students(self):
        ret = []
        for key in self.students:
            ret.append(self.students.get(key))
        return ret

    def enroll_student(self, student):
        self.students.update({student.username.upper(): student})

    def get_student(self, username):
        return self.students.get(username.upper())

    def list_instructors(self):
        ret = []
        for key in self.instructors:
            ret.append(self.instructors.get(key))
        return ret

    def hire_instructor(self, instructor):
        self.instructors.update({instructor.username: instructor})
        instructor.school = self

    def get_instructor(self, username):
        return self.instructors.get(username.upper())

    def list_course_catalog(self):
        ret = []
        for key in self.course_catalog:
            ret.append(self.course_catalog.get(key))
        return ret

    def get_course(self, courseidentifier):
        return self.course_catalog.get(courseidentifier.upper())

    def list_course_schedule(self, year, quarter, department=None):
        ret = list()
        for key in self.course_schedule:
            if department:
                if department.upper() in key:
                    if str(year) in key and quarter.upper() in key:
                        ret.append(self.course_schedule.get(key))
            else:
                if str(year) in key and quarter.upper() in key:
                    ret.append(self.course_schedule.get(key))
        return ret

    def get_all_course_schedule(self):
        ret = list()
        for key in self.course_schedule:
            ret.append(self.course_schedule.get(key))
        return ret

    def add_course(self, course):
        self.course_catalog.update({course.courseidentifier: course})

    def add_course_offering(self, course_offering):
        self.course_schedule.update({course_offering.courseofferingidentifier: course_offering})

    def get_course_offering(self, courseofferingidentifier):
        return self.course_schedule.get(courseofferingidentifier.upper())

    @staticmethod
    def assign_instructor(self, course_offering, instructor):
        course_offering.instructor = instructor.username
        instructor.add_course(course_offering)