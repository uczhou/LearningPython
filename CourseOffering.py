

class CourseOffering:

    def __init__(self, course, section_number, year, quarter):
        self.course = course
        self.section_number = str(section_number)
        self.instructor = 'Not Assigned'
        self.year = str(year)
        self.quarter = quarter.upper()
        self.registered_students = {}
        self.grades = {}
        self.courseofferingidentifier = '{}{}{}{}'.format(self.year, self.quarter,
                                                          self.course.courseidentifier, self.section_number)

    def register_student(self, *args):
        for student in args:
            self.registered_students.update({student.username.upper(): student})
            self.grades.update({student.username.upper(): '-'})
            student.add_course(self.courseofferingidentifier)

    def get_students(self):
        ret = []
        for key in self.registered_students:
            ret.append(self.registered_students.get(key))
        return ret

    def get_student_usernames(self):
        return self.registered_students.keys()

    def get_instructor(self):
        return self.instructor

    def submit_grade(self, grade, student=None, username=None):
        if student is None and username is None:
            print("Please enter student ")
            return
        elif student is None:
            self.grades.update({username.upper(): grade.upper()})
        else:
            self.grades.update({student.username.upper(): grade.upper()})

    def get_grade(self, student=None, username=None):
        if student is None and username is None:
            print("Please enter student ")
            return None
        elif student is None:
            return self.grades.get(username.upper())
        else:
            return self.grades.get(student.username.upper())