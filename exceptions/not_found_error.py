class NotFoundError(Exception):
    """Exception raised when an entity is not found."""
    def __init__(self, entity="Contact"):
        self.message = f"{entity} not found"
        super().__init__(self.message)
