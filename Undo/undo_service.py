class UndoRedoException(Exception):
    """
    Here we create UndoRedoService exceptions that may occur.
    """

    def __init__(self, message=''):
        self.message = message

    # def __str__(self):
    #     return self.message


class UndoRedoService:
    """
    This is undo & redo class.
    """
    def __init__(self):
        """
        This is the creator of UndoRedoService.
        * history is a list, containing the function for undoing the last function called and the function for redoing,
        which is in fact, the initial function
        so, (undo_function, redo_function) is an element of history list
        """
        self.history = []
        self.index = -1

    def record(self, operation):
        """
        Here we record a certain operation, meaning that we add to history the undo-redo pair of functions
        :param operation: the undo-redo pair of functions -> (undo_function, redo_function)
        """
        self.history.append(operation)
        self.index += 1

    def undo(self):
        """
        Here we use history to undo an operation.
        :return: true if all is good
        """
        if self.index == -1:
            raise UndoRedoException("no more undos")

        self.history[self.index].undo()
        self.index -= 1
        return True

    def redo(self):
        """
        Here we use history to redo an operation.
        :return: true if all is good
        """
        if self.index == len(self.history) - 1:
            raise UndoRedoException("no more redos")

        self.index += 1
        self.history[self.index].redo()
        return True


class CascadedOperation:
    """
    This is CascadedOperation class.
    """
    def __init__(self, *operations):
        """
        Here is the constructor of CascadedOperation class.
        If for example we want to delete a student, we also have to delete its grades.
        same thing for assignments.
        :param operations: the given operation
        """
        self.operations = operations

    def undo(self):
        for operation in self.operations:
            operation.undo()

    def redo(self):
        for operation in self.operations:
            operation.redo()


class Operation:
    """
    Here we create an operation wich contains an undo and a redo function call.
    """
    def __init__(self, function_call_undo, function_call_redo):
        self.function_call_undo = function_call_undo
        self.function_call_redo = function_call_redo

    def undo(self):
        self.function_call_undo()

    def redo(self):
        self.function_call_redo()


class FunctionCall:
    """
    Here we create a FunctionCall.
    """
    def __init__(self, function_name, *function_parameters):
        self.function_name = function_name
        self.function_parameters = function_parameters

    def call(self):
        return self.function_name(*self.function_parameters)

    def __call__(self):
        return self.call()