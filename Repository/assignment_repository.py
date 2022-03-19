
class AssignmentRepositoryException(Exception):
    """
    Here we create AssignmentRepository exceptions that may occur.
    """

    def __init__(self, message=''):
        self.message = message

    # def __str__(self):
    #     return self.message


class AssignmentRepository:
    """
    This is AssignmentRepository class. Here we perform functionalities for assignment list.
    """
    def __init__(self, assignment_list=None):
        """
        This function creates the assignment list.
        :param assignment_list: the proper assignment list
        """

        self._assignment_list = []
        if assignment_list is not None:
            self._assignment_list = assignment_list

    @property
    def assignment_list(self):
        return self._assignment_list

    def add_assignment(self, new_assignment):
        """
        This function adds a new assignment in assignment_list.
        :param new_assignment: the assignment that is going to be added
        """
        for assignment in self._assignment_list:
            if assignment.assignment_id == new_assignment.assignment_id:
                raise AssignmentRepositoryException("WARNING: duplicate id! can't add that assignment!")
        self._assignment_list.append(new_assignment)

    def remove(self, filter_function):
        """
        This function removes an assignment with a specific property given.
        :param filter_function: is the specific property given
                for example: remove by id, remove by name, remove by group
        """
        self._assignment_list = list(filter(filter_function, self._assignment_list))

    def get_assignment_list(self):
        """
        Here we return the assignment_list so that we can use it to display assignments in UI module.
        :return: assignment list
        """
        return self._assignment_list

    def find_by_id(self, assignment_id):
        """
        Here we are looking for a assignment with id == assignment_id given
        :param assignment_id: the id of the student we are looking for
        :return: the assignment with assignment_id
        """
        for assignment in self._assignment_list:
            if assignment.assignment_id == assignment_id:
                return assignment
        raise AssignmentRepositoryException("WARNING: There is no assignment with the given id!")

    def update(self, assignment_id, description, deadline):
        assignment = self.find_by_id(assignment_id)
        old_assignment = assignment
        assignment.description = description
        assignment.deadline = deadline
        return assignment, old_assignment

    def un_update(self, assignment_id, description, deadline):
        assignment = self.find_by_id(assignment_id)
        assignment.description = description
        assignment.deadline = deadline
