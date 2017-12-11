import operator
import functools

class Person:

    def __init__(self, last_name, first_name, school, date_of_birth, username, affiliation):
        self.last_name = last_name.upper()
        self.first_name = first_name.upper()
        self.school = school
        self.date_of_birth = date_of_birth
        self.username = username.upper()
        self.affiliation = affiliation.upper()
        self.email = '{}@{}.edu'.format(self.username, self.school.name.replace(' ', '')).upper()

    def list_courses(self):
        pass


class Instructor(Person):

    def __init__(self, last_name, first_name, school, date_of_birth, username, affiliation):
        super().__init__(last_name, first_name, school, date_of_birth, username, affiliation)
        self.courseofferings = {}
        school.hire_instructor(self)

    def list_courses(self, year=None, quarter=None):
        ret = list()
        for key in self.courseofferings:
            if year and quarter:
                if str(year) in key and quarter.upper() in key:
                    ret.append(self.courseofferings.get(key))
            elif year:
                if str(year) in key:
                    ret.append(self.courseofferings.get(key))
            elif quarter:
                if quarter in key:
                    ret.append(self.courseofferings.get(key))
            else:
                ret.append(self.courseofferings.get(key))
        return sorted(ret, key=operator.attrgetter('year', 'quarter'), reverse=True)

    def add_course(self, courseoffering):
        self.courseofferings.update({courseoffering.courseofferingidentifier: courseoffering})

    def __str__(self):
        return '{}\t{} {}\t{}\t{}\t{}\t{}'.format(self.username, self.first_name, self.last_name, self.school.name,
                                                  self.date_of_birth, self.affiliation, self.email)


class Student(Person):

    def __init__(self, last_name, first_name, school, date_of_birth, username, affiliation):
        super().__init__(last_name, first_name, school, date_of_birth, username, affiliation)
        self.courseofferings = {}
        school.enroll_student(self)

    def list_courses(self):
        ret = list()
        for key in self.courseofferings:
            ret.append(self.courseofferings.get(key))
        return sorted(ret, key=operator.attrgetter('year', 'quarter'), reverse=True)

    def credits(self):
        earned_credits = [int(x.course.credits) for x in self.list_courses()
                          if x.get_grade(username=self.username) != '-']
        if earned_credits:
            return functools.reduce(lambda x, y: x+y, earned_credits)
        else:
            return 0

    def total_credits(self):
        return functools.reduce(lambda x, y: x+y,
                                [int(x.course.credits) for x in self.list_courses()])

    def gpa(self):
        grades = [self.letter_to_point(x.get_grade(username=self.username)) *
                  int(x.course.credits) for x in self.list_courses() if x.get_grade(username=self.username) != '-']
        if grades:
            return functools.reduce(lambda x, y: x+y, grades) / self.credits()
        else:
            return 0

    @staticmethod
    def letter_to_point(self, letter_grade):
        points_table = {'A+': 4, 'A': 4, 'A-': 3.7,
                        'B+': 3.3, 'B': 3, 'B-': 2.7,
                        'C+': 2.3, 'C': 2, 'C-': 1.7,
                        'D+': 1.3, ' D': 1, 'D-': 0.7,
                        'F': 0}
        return points_table.get(letter_grade.upper())

    def add_course(self, courseofferingidentifier):
        self.courseofferings.update({courseofferingidentifier.upper():
                                    self.school.get_course_offering(courseofferingidentifier.upper())})

    def __str__(self):
        return '{}\t{} {}\t{}\t{}\t{}\t{}'.format(self.username, self.first_name, self.last_name, self.school.name,
                                                  self.date_of_birth, self.affiliation, self.email)