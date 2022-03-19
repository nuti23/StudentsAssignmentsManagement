from datetime import datetime


class AssignmentException(Exception):
    """
    Here we create Assignment exceptions that may occur.
    """
    def __init__(self, message=''):
        self._message = message

    # def __str__(self):
    #     return self._message


class AssignmentValidator:
    """
    This is StudentValidator class, here we validate a assignment.
    id -> integer, !=''
    description -> string, !=''
    deadline -> date, !='', it has to be greater then the current date
    """
    def validate(self, assignment):
        # id validation
        if assignment.assignment_id == '':
            raise AssignmentException('Invalid assignment_id, empty value provided!')
        if not isinstance(assignment.assignment_id, int):
            raise AssignmentException('Id must be an integer!')

        # description validation
        if assignment.description == '':
            raise AssignmentException('Invalid description, empty value provided!')
        if not isinstance(assignment.description, str):
            raise AssignmentException('Description must be a string!')

        # deadline validation
        if assignment.deadline == '':
            raise AssignmentException('Invalid deadline, empty value provided!')
        if not isinstance(assignment.deadline, datetime):
            raise AssignmentException("Deadline must be a date!")
