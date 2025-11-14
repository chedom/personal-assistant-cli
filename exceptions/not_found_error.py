class NotFoundError(Exception):
    def __init__(self, entity="Contact"):
        self.message = f"{entity} not found"
        super().__init__(self.message)
