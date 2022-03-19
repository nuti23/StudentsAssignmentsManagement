import datetime


class Assignment:
    """
    The Assignment class.
    """

    def __init__(self, assignment_id, description, deadline):
        """
        This function is a constructor which creates an Assignment.
        :param assignment_id: natural number representing the unique code of an Assignment
        :param description: string representing the task of an Assignment
        :param deadline: date type representing the last date to push an Assignment, (> today's date)
        """
        self._assignment_id = assignment_id
        self._description = description
        self._deadline = deadline

    @property
    def assignment_id(self):
        return self._assignment_id

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        self._deadline = value


def test_assignment():
    date = datetime.datetime(2021, 3, 1)
    assignment = Assignment(111, "Write a song about Python Language.", date)
    assert assignment.assignment_id == 111
    assert assignment.description == "Write a song about Python Language."
    assert assignment.deadline == date


test_assignment()