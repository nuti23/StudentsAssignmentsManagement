import datetime

from Domain.assignment import Assignment
from Repository.assignment_repository import AssignmentRepository


class AssignmentRepositoryTextFile(AssignmentRepository):
    """
    Here is the AssignmentRepositoryTextFile class.
    """
    def __init__(self, file_name="assignment.txt"):
        """
        This is the constructor of AssignmentRepositoryTextFile class.
        :param file_name: the name of the file we're working with
        """
        super().__init__()
        self._file_name = file_name
        self._load()

    def add_assignment(self, assignment):
        """
        Here we use the functionalities from AssignmentRepository class to add a an assignment in the file and also
        in memory.
        We also save the change.
        :param assignment: the assignment that will be added, Assignment() type
        """
        super().add_assignment(assignment)
        self._save()

    def remove(self, filter_function):
        """
        Here we use the functionalities from AssignmentRepository class to remove an assignment by its id from the file
        and also from memory.
        We also save the change.
        :param filter_function: a general remove function, we use remove by id
        """
        super().remove(filter_function)
        self._save()

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
        self._save()

    def _load(self):
        """
        Here we read the txt file and we add the assignment.
        """
        file = open(self._file_name, 'rt')
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.split(";")
            year, month, day = line[2].split("-")
            super().add_assignment(Assignment(int(line[0]), line[1], datetime.datetime(int(year), int(month), int(day))))

    def _save(self):
        """
        Here we write the assignments from our assignments_list.
        """
        file = open(self._file_name, 'wt')
        for assignment in self.get_assignment_list():
            line = str(assignment._assignment_id) + ";" + assignment.description + ";" + str(assignment.deadline)
            file.write(line)
            file.write("\n")
        file.close()



