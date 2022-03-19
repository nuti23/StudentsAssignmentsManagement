from Domain.grade import Grade


class GradeException(Exception):
    """
    Here we create Grade exceptions that may occur.
    """
    def __init__(self, message=''):
        self._message = message

    # def __str__(self):
    #     return self._message


class GradeValidator:
    """
    This is GradeValidator class, where we validate a grade.
    student_id -> integer, !=''
    assignment_id -> integer, !=''
    grade_value -> integer in [0,10], !=''
    """

    def validate(self, grade):
        # student_id validation
        if grade.student_id == '':
            raise GradeException("Invalid student_id, empty value provided!")
        if not isinstance(grade.student_id, int):
            raise GradeException('student_id must be an integer!')

        # assignment_id validation
        if grade.assignment_id == '':
            raise GradeException("Invalid assignment_id, empty value provided!")
        if not isinstance(grade.assignment_id, int):
            raise GradeException('assignment_id must be an integer!')

        # grade_value validation
        if grade.grade_value == '':
            raise GradeException("Invalid grade_value, empty value provided!")
        if not isinstance(grade.grade_value, int):
            raise GradeException('grade_value must be an integer!')
        if grade.grade_value > 10 or grade.grade_value < 0:
            raise GradeException('grade_value must be in [0,10]')
