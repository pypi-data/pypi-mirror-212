import os

class FileMaster:
    def __init__(self):
        self.filename = None
        self.file = None

    def search(self, filename):
        self.filename = filename
        try:
            self.file = open(self.filename, "r")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error 01: No file found named '{self.filename}'") from e
        return self

    def add(self, text):
        if self.file:
            with open(self.filename, "a") as file:
                file.write(text)
        else:
            raise Exception("Error 02: File not opened")

    def write(self, text):
        if self.file:
            with open(self.filename, "w") as file:
                file.write(text)
        else:
            raise Exception("Error 02: File not opened")

    def see(self):
        if self.file:
            with open(self.filename, "r") as file:
                contents = file.read()
                return contents
        else:
            raise Exception("Error 02: File not opened")

    @staticmethod
    def create(filename, extension):
        filename = f"{filename}.{extension}"
        try:
            open(filename, "w").close()  # Create an empty file
        except Exception as e:
            raise Exception(f"Error 03: Error creating file: '{filename}'") from e
        return FileMaster().search(filename)
