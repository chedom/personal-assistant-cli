class AlreadyExistError(Exception):
    def __init__(self, entity="Contact"):
        self.message = f"{entity} already exists"
        super().__init__(self.message)
