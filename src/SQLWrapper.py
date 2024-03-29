###
# Programmers: David Landsman, Aaron Nahum
# File name: SQLWrapper.py
# Description: Contains methods for easily working with the database.
###

import sqlite3
import Course
import Student

class SQLWrapper:
    def __init__(self):
        '''Initialize SQLWrapper.'''
        # Create a database file
        self.con = sqlite3.connect('timetable.db')
        # Connect to the database (locally)
        self.cursor = self.con.cursor()

    def createStudentsTable(self):
        """
        Creates a table to store student data
        """
        statement = "CREATE TABLE IF NOT EXISTS Students (studentId INTEGER, grade INTEGER, selectedCourses TEXT, password TEXT, finalCourses TEXT)"
        self.cursor.execute(statement)
        self.con.commit()
        
    def createCoursesTable(self):
        """
        Creates a courses table
        """
        statement = "CREATE TABLE IF NOT EXISTS Courses (courseId INTEGER, name TEXT, priority INTEGER)"
        self.cursor.execute(statement)
        self.con.commit()

    def generateCourses(self):
        """
        Generates courses for the courses table
        """
        # Check if courses aren't already generated
        if len(self.getAllCourses()) > 0:
            return
        
        Courses = ["English", "Math", "Comp Sci", "Entrepreneurship",
               "Accounting", "History", "Geography", "Music",
               "Religion"] #List of Courses

        #Adds courses with different priorities
        i = 0
        for i in range (0,2):
            self.addCourse(i + 1, Courses[i], 3)
        for i in range (0,5):
            self.addCourse(i + 3, Courses[i+2], 2)
        for i in range (0,2):
            self.addCourse(i+8, Courses[i+7],1)

    def addStudent(self, studentId, grade, password):
        """ (int, int, str) -> (none)

        Adds a student into the database
        """
        statement = "INSERT INTO Students VALUES (%s, %s, '%s', '%s', '%s')" % (studentId, grade, None, password, None)
        self.cursor.execute(statement)
        self.con.commit()
        

    def addStudentCourses (self, studentId, selectedCourses):
        """ (int, list) -> (none)

        Adds all courses that the Student chose
        """
        # Use a string representation of the selectedCourses list to store it in the database
        statement = 'UPDATE Students SET selectedCourses = "%s" WHERE studentId = %s' % (repr(selectedCourses), studentId)
        self.cursor.execute(statement)
        self.con.commit()

    def addFinalCourses(self, studentId, finalCourses):
        """ (int, list) -> (none)

        Adds final timetable to Student.
        """
        statement = 'UPDATE Students SET finalCourses = "%s" WHERE studentId = %s' % (repr(finalCourses), studentId)
        self.cursor.execute(statement)
        self.con.commit()
        
    def addCourse(self, courseId, name, priority):
        """ (int, str, int) -> (none)

        Adds a course to the Students selected courses
        """
        statement = "INSERT INTO Courses VALUES (%s, '%s', %s)" % (courseId, name, priority)
        self.cursor.execute(statement)
        self.con.commit()

    def deleteStudent(self, studentId):
        """ (str) -> (none)

        Deletes a student from a selected course
        """
        statement = "DELETE FROM Students WHERE studentId = %s" % (studentId)
        self.cursor.execute(statement)
        self.con.commit()

    def getCourse(self, courseId):
        """ (int) -> (Course)

        Gets a course with the given id
        """
        statement = "SELECT * FROM Courses WHERE courseId = %s" % (courseId)
        self.cursor.execute(statement)
        # Retrieve a single course and return it
        row = self.cursor.fetchone()
        if row != None:
            return self.parseCourse(row)
        else:
            return None

    def getAllCourses(self):
        """
        Gets all courses
        """
        statement = "SELECT * FROM Courses"
        self.cursor.execute(statement)
        courses = []
        # Retrieve all courses and create a list of Course (model) objects and return it
        rows = self.cursor.fetchall()
        if rows == None:
            return None
        for row in rows:
            courses.append(self.parseCourse(row))
        return courses

    def getStudent(self, studentId):
        """ (int) -> (Student)

        Gets a student with the given id
        """
        statement = "SELECT * FROM Students WHERE studentId = %s" % (studentId)
        self.cursor.execute(statement)
        # Retrieve a single student and return it
        row = self.cursor.fetchone()
        if row != None:
            return self.parseStudent(row)
        else:
            return None

    def getAllStudents(self):
        """
        Gets all students
        """
        statement = "SELECT * FROM Students"
        self.cursor.execute(statement)
        students = []
        # Retrieve all students and create a list of Student (model) objects and return it
        rows = self.cursor.fetchall()
        if rows == None:
            return None
        for row in rows:
            students.append(self.parseStudent(row))
        return students

    def parseStudent(self, row):
        return Student.Student(row[0], row[1], row[2], row[3], row[4])

    def parseCourse(self, row):
        return Course.Course(row[0], row[1], row[2])




