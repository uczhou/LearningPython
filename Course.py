

class Course:

    def __init__(self, department, number, name, c_credits):
        self.department = department.upper()
        self.number = str(number)
        self.name = name
        self.credits = str(c_credits)
        self.courseidentifier = '{}{}'.format(self.department, self.number)

    def __str__(self):
        return 'Department: {}\tCourse number: {}\t' \
               'Course name: {}\tCredits: {}'.format(self.department, self.number, self.name, self.credits)