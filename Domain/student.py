
class Student:
    """
    The Student class.
    """

    def __init__(self, _student_id, name, group):
        """
        This function is a constructor which creates a Student.
        :param _student_id: natural number representing the unique code of a Student
        :param name: string representing the name of a Student
        :param group: natural number representing the group of a Student
        """
        self._student_id = _student_id
        self._name = name
        self._group = group

    @property
    def student_id(self):
        return self._student_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    def __str__(self):
        return str(self._student_id) + ' ' + self._name + " " + self._group


def test_Student():
    student = Student(23452, 'Summer Sun', 45)
    assert student.name == 'Summer Sun'
    assert student.student_id == 23452
    assert student.group == 45


test_Student()





