class AlreadyExistError(Exception):
    """Exception raised when trying to create an entity that already exists."""
    def __init__(self, entity="Contact"):
        self.message = f"{entity} already exists"
        super().__init__(self.message)
