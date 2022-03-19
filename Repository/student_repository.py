
class StudentRepositoryException(Exception):
    """
     Here we create StudentRepository exceptions that may occur.
    """

    def __init__(self, message=''):
        self.message = message

    # def __str__(self):
    #     return self.message


class StudentRepository:
    """
    This is StudentRepository class. Here we perform functionalities for student's list.
    """
    def __init__(self, students_list=None):
        """
        This function creates the students list.
        :param students_list: the proper students list
        """
        self._students_list = []
        if students_list is not None:
            self._students_list = students_list

    @property
    def students_list(self):
        return self._students_list

    def add_student(self, new_student):
        """
        This function adds a new student in students_list.
        :param new_student: the student that is going to be added
        """
        for student in self._students_list:
            if student.student_id == new_student.student_id:
                raise StudentRepositoryException("WARNING: duplicate id! can't add that student!")
        self._students_list.append(new_student)

    def remove(self, filter_function):
        """
        This function removes a student with a specific property given.
        :param filter_function: is the specific property given
                for example: remove by id, remove by name, remove by group
        """
        self._students_list = list(filter(filter_function, self._students_list))

    def get_students_list(self):
        """
        Here we return the students_list so that we can use it to display students in UI module.
        :return: students list
        """
        return self._students_list

    def find_by_id(self, student_id):
        """
        Here we are looking for a student with id == student_id
        :param student_id: the id of the student we are looking for
        :return: the student with student_id
        """
        for student in self._students_list:
            if student.student_id == student_id:
                return student
        raise StudentRepositoryException("WARNING: There is no student with the given id!")


    def update(self, student_id, name, group):
        """
        Here we update an existing student by its id
        :param student_id: the id of the student that will pe updated
        :param name: string representing the new name
        :param group: integer representing the new group
        :return: the student
        """
        student = self.find_by_id(student_id)
        old_name = student.name
        old_group = student.group
        student.name = name
        student.group = group
        return student, old_name, old_group


    def un_update(self, student_id, name, group):
        student = self.find_by_id(student_id)
        student.name = name
        student.group = group