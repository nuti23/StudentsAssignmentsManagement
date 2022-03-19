from Domain.student import Student


class StudentException(Exception):
    """
    Here we create Student exceptions that may occur.
    """
    def __init__(self, message=''):
        self._message = message

    # def __str__(self):
    #     return self._message


class StudentValidator:
    """
    This is StudentValidator class, where we validate a student.
    id -> integer, !=''
    name -> string, !=''
    group -> integer, !=''
    """
    def validate(self, student):
         # id validation
         if student.student_id == '':
             raise StudentException("Invalid student_id, empty value provided!")
         if not isinstance(student.student_id, int):
             raise StudentException('Id must be an integer!')

         # name validation
         if student.name == '':
            raise StudentException("Invalid name, empty value provided!")
         if not isinstance(student.name, str):
             raise StudentException('Name must be a string!')

         # group validation
         if student.group == '':
            raise StudentException("Invalid group, empty value provided!")
         if not isinstance(student.group, int):
             raise StudentException('Group must be an integer!')

