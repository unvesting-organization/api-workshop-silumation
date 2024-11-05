class MongoDBException(Exception):
    def __init__(self, message="Error connect to MongoDb"):
        super().__init__(message)