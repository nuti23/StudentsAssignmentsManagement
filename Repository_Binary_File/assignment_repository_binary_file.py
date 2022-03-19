import pickle

from Repository.assignment_repository import AssignmentRepository


class AssignmentRepositoryBinaryFile(AssignmentRepository):
    """
    Here is the AssignmentRepositoryBinaryFile class.
    """
    def __init__(self, file_name):
        """
        This is the constructor of AssignmentRepositoryBinaryFile class.
        :param file_name: the name of the file we're working with
        """
        super().__init__()
        self._file_name = file_name
        self._assignment_list = self._load()

    def add_assignment(self, assignment):
        """
        Here we use the functionalities from AssignmentRepository class to add a an assignment in the file and also
        in memory.
        We also save the change.
        :param assignment: the assignment that will be added, Assignment() type
        """
        super().add_assignment(assignment)
        self._save(self.assignment_list)

    def remove(self, filter_function):
        """
        Here we use the functionalities from AssignmentRepository class to remove an assignment by its id from the file
        and also from memory.
        We also save the change.
        :param filter_function: a general remove function, we use remove by id
        """
        super().remove(filter_function)
        self._save(self.assignment_list)

    def update(self, assignment_id, description, deadline):
        """
        Here we use the functionalities from AssignmentRepository class to update an existent assignment in the file and
        also in memory.
        We also save the change.
        :param assignment_id: an integer representing the id of an existent assignment which we'll be updated
        :param description: a string representing the new description
        :param deadline: a datetime type representing the new deadline
        """
        super().update(assignment_id, description, deadline)
        self._save(self.assignment_list)

    def _load(self):
        """
        Here we read the txt file and we add the assignment.
        We raise EOError or IOError if it is the case.
        """
        try:
            file = open(self._file_name, 'rb')
            lines = pickle.load(file)
            file.close()
            return lines
        except EOFError:
            return []
        except IOError as error:
            raise error

    def _save(self, assignments):
        """
        Here we write the assignments from our assignments_list.
        """
        file = open(self._file_name, "wb")
        pickle.dump(assignments, file)
        file.close()

