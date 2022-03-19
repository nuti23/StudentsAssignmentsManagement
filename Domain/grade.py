from Domain.assignment import Assignment
from Domain.student import Student
import datetime


class Grade:
    """
    The Grade class.
    """

    def __init__(self, student_id, assignment_id, grade_value):
        """
        This function is a constructor which creates a connection between an Assignment and a Student.
        :param assignment_id: natural number representing the unique code of an Assignment
        :param student_id: natural number representing the unique code of a Student
        :param grade_value: positive integer representing the Grade of a Student at a specific Assignment
        """
        self._assignment_id = assignment_id
        self._student_id = student_id
        self._grade_value = grade_value

    @property
    def assignment_id(self):
        return self._assignment_id

    @property
    def student_id(self):
        return self._student_id

    @property
    def grade_value(self):
        return self._grade_value

    @grade_value.setter
    def grade_value(self, value):
        self._grade_value = value


def test_grade():
    date = datetime.datetime(2021, 3, 4)
    assignment = Assignment(123, "Write a song about Python Language.", date)
    student = Student(453, "Summer Sun", 91)
    grade_value = 5
    grade = Grade(student.student_id, assignment.assignment_id, grade_value)

    assert grade.assignment_id == 123
    assert grade.student_id == 453
    assert grade.grade_value == 5


test_grade()
