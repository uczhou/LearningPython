#! /usr/bin/env python3
import Course
import CourseOffering
import Institution
import Person
import sys
import os
import pandas as pd


# Function Tools
def get_course(school):
    department = input('Please enter department: ').strip()
    number = input('Please enter course number: ').strip()
    courseidentifier = department + number
    return school.get_course(courseidentifier)


def get_instructor(school):
    return school.get_instructor(input('Please enter the instructor username: ').strip())


def get_student(school):
    return school.get_student(input('Please enter the student username: ').strip())


def get_courseoffering(school):
    department = input('Please enter department: ').strip()
    number = input('Please enter course number: ').strip()
    section_number = input('Please enter section number: ').strip()
    year = input('Please enter the year: ').strip()
    quarter = input('Please enter the quarter: ').strip()
    if year.isalnum():
        courseofferingidentifier = year + quarter + department + number + section_number
        return school.get_course_offering(courseofferingidentifier)
    else:
        print('Sorry, input information is incorrect')


class Data:

    def __init__(self):
        self.schools_df = pd.DataFrame({'name': [], 'instructors': [], 'students': [],
                                        'course_catalog': [], 'course_schedule': []})
        self.courses_df = pd.DataFrame({'department': [], 'number': [], 'name': [], 'credits': [],
                                        'courseidentifier': []})
        self.courseofferings_df = pd.DataFrame({'course': [], 'section_number': [], 'instructor': [], 'year': [],
                                                'quarter': [], 'courseofferingidentifier': []})
        self.students_df = pd.DataFrame({'last_name': [], 'first_name': [], 'school': [],
                                         'date_of_birth': [], 'username': [], 'affiliation': [], 'email': []})
        self.instructors_df = pd.DataFrame({'last_name': [], 'first_name': [], 'school': [],
                                            'date_of_birth': [], 'username': [], 'affiliation': [], 'email': []})
        self.register_students_df = pd.DataFrame({'courseofferingidentifier': [], 'username': [], 'grade': []})

    def initialize_system(self, school_name):
        # To be implemented
        # Check if file exists
        # cwd = os.getcwd()
        if os.path.exists('schools.csv'):
            self.schools_df = pd.read_csv('schools.csv')
        if not self.schools_df.empty and not self.schools_df.loc[self.schools_df['name'] == school_name].empty:
            print('Welcome back')
            school = Institution.Institution(school_name)

            # Initialize courses
            self.courses_df = pd.read_csv('{}_courses.csv'.format(school_name.upper()))
            for i in range(self.courses_df.shape[0]):
                department = self.courses_df.iloc[i]['department']
                number = self.courses_df.iloc[i]['number']
                name = self.courses_df.iloc[i]['name']
                c_credits = self.courses_df.iloc[i]['credits']
                school.add_course(Course.Course(department, number, name, c_credits))

            # Initialize students
            self.students_df = pd.read_csv('{}_students.csv'.format(school_name.upper()))
            for i in range(self.students_df.shape[0]):
                last_name = str(self.students_df.iloc[i]['last_name'])
                first_name = str(self.students_df.iloc[i]['first_name'])
                # school_name = self.students_df.iloc[i]['school']
                date_of_birth = self.students_df.iloc[i]['date_of_birth']
                username = str(self.students_df.iloc[i]['username'])
                affiliation = str(self.students_df.iloc[i]['affiliation'])
                # email = self.students_df.iloc[i]['email']
                registrar.Student(last_name, first_name, school, date_of_birth, username, affiliation)
                # school.enroll_student(registrar.Student(last_name, first_name, school,
                #                                         date_of_birth, username, affiliation))

            # Initialize instructors
            self.instructors_df = pd.read_csv('{}_instructors.csv'.format(school_name.upper()))
            for i in range(self.instructors_df.shape[0]):
                last_name = str(self.instructors_df.iloc[i]['last_name'])
                first_name = str(self.instructors_df.iloc[i]['first_name'])
                # school_name = self.instructors_df.iloc[i]['school']
                date_of_birth = self.instructors_df.iloc[i]['date_of_birth']
                username = str(self.instructors_df.iloc[i]['username'])
                affiliation = str(self.instructors_df.iloc[i]['affiliation'])
                Person.Instructor(last_name, first_name, school, date_of_birth, username, affiliation)
                # email = self.instructors_df.iloc[i]['email']
                # school.hire_instructor(registrar.Instructor(last_name, first_name, school,
                #                                             date_of_birth, username, affiliation))

            # Initialize courseofferings
            self.courseofferings_df = pd.read_csv('{}_courseofferings.csv'.format(school_name.upper()))
            for i in range(self.courseofferings_df.shape[0]):
                course = self.courseofferings_df.iloc[i]['course']
                section_number = self.courseofferings_df.iloc[i]['section_number']
                instructor = self.courseofferings_df.iloc[i]['instructor']
                year = self.courseofferings_df.iloc[i]['year']
                quarter = self.courseofferings_df.iloc[i]['quarter']
                courseoffering = CourseOffering.CourseOffering(school.get_course(course), section_number, year, quarter)
                school.add_course_offering(courseoffering)
                if instructor != 'Not Assigned':
                    school.assign_instructor(courseoffering, school.get_instructor(instructor))

            # Update relational information
            self.register_students_df = pd.read_csv('{}_register_students.csv'.format(school_name.upper()))

            for i in range(self.register_students_df.shape[0]):
                courseofferingidentifier = self.register_students_df.iloc[i]['courseofferingidentifier']
                username = self.register_students_df.iloc[i]['username']
                grade = self.register_students_df.iloc[i]['grade']
                school.get_course_offering(courseofferingidentifier).\
                    register_student(school.get_student(username))
                if grade and grade != '-':
                    school.get_course_offering(courseofferingidentifier).submit_grade(grade, username=username)
                school.get_student(username).add_course(courseofferingidentifier)
        else:
            school = Institution.Institution(school_name)
            self.schools_df = \
                self.schools_df.append({'name': school_name,
                                        'instructors': '{}_instructors.csv'.format(school.name),
                                        'students': '{}_students.csv'.format(school.name),
                                        'course_catalog': '{}_courses.csv'.format(school.name),
                                        'course_schedule': '{}_courseofferings.csv'.format(school.name)},
                                       ignore_index=True)
        return school


def options():
    lines = list()
    lines.append('Please select an option from the following:')
    lines.append('{:2}\t{}'.format(1, 'Create a course'))
    lines.append('{:2}\t{}'.format(2, 'Schedule a course offering'))
    lines.append('{:2}\t{}'.format(3, 'List course catalog'))
    lines.append('{:2}\t{}'.format(4, 'List course schedule'))
    lines.append('{:2}\t{}'.format(5, 'Hire an instructor'))
    lines.append('{:2}\t{}'.format(6, 'Assign an instructor to a course'))
    lines.append('{:2}\t{}'.format(7, 'Enroll a student'))
    lines.append('{:2}\t{}'.format(8, 'Register a student for a course'))
    lines.append('{:2}\t{}'.format(9, 'List enroled students'))
    lines.append('{:2}\t{}'.format(10, 'List students registered for a course'))
    lines.append('{:2}\t{}'.format(11, 'Submit student grade'))
    lines.append('{:2}\t{}'.format(12, 'Get student records'))
    lines.append('{:2}\t{}'.format(13, 'Exit'))
    print('\n'.join(lines))


def save_to_disk(school, data):
    # Save school meta data
    data.schools_df.to_csv('schools.csv', index=False)
    # Save course data
    data.courses_df.to_csv('{}_courses.csv'.format(school.name.upper()), index=False)
    # Save course offering data
    data.courseofferings_df.to_csv('{}_courseofferings.csv'.format(school.name.upper()), index=False)
    # Save instructors data
    data.instructors_df.to_csv('{}_instructors.csv'.format(school.name.upper()), index=False)
    # Save students data
    data.students_df.to_csv('{}_students.csv'.format(school.name.upper()), index=False)
    # Save register data
    data.register_students_df.to_csv('{}_register_students.csv'.format(school.name.upper()), index=False)


# 1
def create_course(school, data):
    department = input('Please enter the department offering the new course: ').strip()
    number = input('Please enter the new course number: ').strip()
    name = input('Please enter the new course name: ').strip()
    c_credits = input('Please enter the new course credits: ').strip().replace(' ', '')
    course = Course.Course(department, number, name, c_credits)
    school.add_course(course)
    data.courses_df = \
        data.courses_df.append({'department': department, 'number': number, 'name': name, 'credits': c_credits,
                                'courseidentifier': course.courseidentifier}, ignore_index=True)
    print('Successfully create a course.')
    save_to_disk(school, data)


# 2
def schedule_courseoffering(school, data):
    # Check if course exists
    course = get_course(school)
    section_number = input('Please enter the section number: ').strip()
    year = input('Please enter the year offering the course: ').strip()
    quarter = input('Please enter the quarter offering the course: ').strip()
    if course:
        courseoffering = CourseOffering.CourseOffering(course, section_number, year, quarter)
        instructor = courseoffering.get_instructor()
        school.add_course_offering(courseoffering)
        data.courseofferings_df = \
            data.courseofferings_df.append({'course': course.courseidentifier, 'section_number': section_number,
                                            'instructor': instructor, 'year': year, 'quarter': quarter,
                                            'courseofferingidentifier': courseoffering.courseofferingidentifier},
                                           ignore_index=True)
        print('Successfully scheduled a course offering.')
        save_to_disk(school, data)
    else:
        print('Sorry, input information is incorrect')


# 3
def show_courses(school, data):
    for course in school.list_course_catalog():
        print(course)


# 4
def show_course_schedules(school, data):
    year = input('Please enter the year: ').strip()
    quarter = input('Please enter the quarter: ').strip()
    if year.isnumeric() and school.list_course_schedule(int(year), quarter):
        for courseoffering in school.list_course_schedule(year, quarter):
            instructor = courseoffering.get_instructor()
            if instructor != 'Not Assigned':
                instructor_name = '{} {}'.format(school.get_instructor(instructor).first_name,
                                                 school.get_instructor(instructor).last_name)
            else:
                instructor_name = instructor
            print(courseoffering.course)
            print('Section: {}\t Instructor: {}\tYear: {}\t'
                  'Quarter: {}'.format(courseoffering.section_number, instructor_name,
                                       courseoffering.year, courseoffering.quarter))
    else:
        print('Sorry, no class scheduled for the searched criteria')


# 5
def hire_instructor(school, data):
    # Get instructor information
    last_name = input('Please enter the instructor\'s last_name: ').strip()
    first_name = input('Please enter the instructor\'s first_name: ').strip()
    date_of_birth = input('Please enter the instructor\'s data birth in format MM/DD/YYYY: ').strip()
    username = input('Please enter the instructor\'s username: ').strip()
    while school.get_student(username) or school.get_instructor(username):
        print('Username has been registered, please choose another username.')
        username = input('Please enter the instructor\'s username: ').strip()
    affiliation = input('Please enter the instructor\'s affiliation (e.g., student, faculty, staff, etc): ').strip()
    # email = input('Please enter the instructor\'s email: ').strip()
    instructor = Person.Instructor(last_name, first_name, school, date_of_birth, username, affiliation)
    school.hire_instructor(instructor)
    data.instructors_df = \
        data.instructors_df.append({'last_name': last_name, 'first_name': first_name, 'school': school.name,
                                    'date_of_birth': date_of_birth, 'username': username,
                                    'affiliation': affiliation, 'email': instructor.email}, ignore_index=True)
    print('Successfully hired an instructor.')
    save_to_disk(school, data)


# 6
def assign_course(school, data):
    instructor = get_instructor(school)
    courseoffering = get_courseoffering(school)
    if instructor and courseoffering:
        school.assign_instructor(courseoffering, instructor)
        # instructor.add_course(courseoffering)
        print('Successfully assign the instructor to the course.')
        save_to_disk(school, data)
    else:
        print('Sorry, input information is incorrect')


# 7
def enroll_student(school, data):
    # Get student information
    last_name = input('Please enter the student\'s last_name: ').strip()
    first_name = input('Please enter the student\'s first_name: ').strip()
    date_of_birth = input('Please enter the student\'s data birth in format MM/DD/YYYY: ').strip()
    username = input('Please enter the student\'s username: ').strip()
    while school.get_student(username) or school.get_instructor(username):
        print('Username has been registered, please choose another username.')
        username = input('Please enter the student\'s username: ').strip()
    affiliation = input('Please enter the student\'s affiliation (e.g., student, faculty, staff, etc): ').strip()
    # email = input('Please enter the student\'s email: ').strip()
    student = Person.Student(last_name, first_name, school, date_of_birth, username, affiliation)
    # school.enroll_student(student)
    data.students_df = \
        data.students_df.append({'last_name': last_name, 'first_name': first_name, 'school':
                                school.name, 'date_of_birth': date_of_birth, 'username': username,
                                 'affiliation': affiliation, 'email': student.email}, ignore_index=True)
    print('Successfully enrolled the student.')
    save_to_disk(school, data)


# 8
def register_student(school, data):
    student = get_student(school)
    courseoffering = get_courseoffering(school)
    if student and courseoffering:
        courseoffering.register_student(student)
    # student.add_course(courseoffering)
        data.register_students_df = \
            data.register_students_df.append({'courseofferingidentifier': courseoffering.courseofferingidentifier,
                                              'username': student.username, 'grade': '-'}, ignore_index=True)
        print('Successfully registered the student.')
        save_to_disk(school, data)
    elif student:
        print('Sorry, course is not found')
    else:
        print('Sorry, student is not found')


# 9
def list_enrolled_students(school, data):
    for student in school.list_students():
        print(student)


# 10
def list_registered_students(school, data):
    courseoffering = get_courseoffering(school)
    if courseoffering:
        for student in courseoffering.get_students():
            print('{} {}'.format(student.first_name, student.last_name))


# 11
def submit_student_grade(school, data):
    username = input('Please enter the student username: ').strip().upper()
    courseoffering = get_courseoffering(school)
    grade = input('Please enter the student grade: ').strip().replace(' ', '')
    if school.get_student(username) and courseoffering and username in courseoffering.get_student_usernames():
        courseoffering.submit_grade(grade, username=username)
        data.register_students_df.loc[(data.register_students_df[
                                      'courseofferingidentifier'] == courseoffering.courseofferingidentifier)
                                      & (data.register_students_df['username'] == username), 'grade'] = grade
        print('Successfully submit student grade.')
        save_to_disk(school, data)
    else:
        print('Sorry, the information is incorrect')


# 12
def get_student_records(school, data):
    username = input('Please enter the student username: ').strip()
    student = school.get_student(username)
    if student:
        coursesofferings = student.list_courses()
        for courseoffering in coursesofferings:
            print('{}\t{}\t{}'.format(courseoffering.course.name,
                                      courseoffering.course.credits, courseoffering.get_grade(username=username)))
        print('Total credits registered: {}\tTotal credits earned: {}\t GPA: {}'
              .format(student.total_credits(), student.credits(), student.gpa()))
    else:
        print('Sorry, input information is incorrect')


# 13
def user_exit(school, data):
    # Save user information
    save_to_disk(school, data)
    sys.exit(0)


optools = {1: create_course, 2: schedule_courseoffering, 3: show_courses, 4: show_course_schedules,
           5: hire_instructor, 6: assign_course, 7: enroll_student, 8: register_student,
           9: list_enrolled_students, 10: list_registered_students, 11: submit_student_grade,
           12: get_student_records, 13: user_exit}


def main():
    print('Welcome to the Registration System')
    data = Data()
    school_name = input('Please enter the name of your institution: ')
    school = data.initialize_system(school_name.upper())
    try:
        while True:
            options()
            arg = input('Please enter your choice: ')
            # Check if arg is number
            if arg.isalnum():
                val = int(arg)
                if val in range(14):
                    optools.get(val)(school, data)
                else:
                    print("Please enter a valid number, or enter 'help' for instructions")
            elif arg.isalpha():
                print('help menu')
            else:
                print("Please enter a valid number, or enter 'help' for instructions")
    except KeyboardInterrupt:
        print('Operation interrupted, saving files ...')
        user_exit(school, data)
        print('Files have been saved.')
        sys.exit(0)


if __name__ == '__main__':
    main()
