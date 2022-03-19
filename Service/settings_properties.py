
class SettingsProperties:
    """
    Here is the SettingsProperties class.
    """
    def __init__(self, settings_path="settings.properties.txt"):
        """
        Here is the constructor of SettingsProperties class.
        Here we will extract 'commands' from settings.properties.txt to decide which repository and files to use.
        :param settings_path: it is the name of the file form where we extract the 'commands'
        """
        self._settings_data = {}
        self._load(settings_path)

    @property
    def settings_data(self):
        return self._settings_data

    @property
    def repository_type(self):
        return self._settings_data["repository"]

    @property
    def student_file(self):
        return self._settings_data["student"]

    @property
    def assignment_file(self):
        return self._settings_data["assignment"]

    @property
    def grade_file(self):
        return self._settings_data["grade"]

    def _load(self, file_path):
        """
        Here we read from the give file and we save the information in a dictionary.
        {"repository": inmemory/textfiles/binaryfiles,
        "student": " "/student.txt/student.bin,
        "assignment": " "/assignment.txt/assignment.bin }
        :param file_path: it is the name of the file form where we extract the 'commands'
        """
        file = open(file_path, "rt")
        lines = file.readlines()
        file.close()

        for line in lines:
            [property, value] = line.split("=", 1)
            property = property.strip()
            value = value.strip()
            self._settings_data[property] = value
