class InvalidCategoryInputError(Exception):
    def __init__(self, name: str):
        self.name = name


class InvalidUrlInputError(Exception):
    def __init__(self, name: str):
        self.name = name
