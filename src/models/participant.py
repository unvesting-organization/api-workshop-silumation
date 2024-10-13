# src/models/participant.py

class Participant:
    def __init__(self, user_id):
        self.user_id = user_id
        self.choices = {}  # Choices per time
        self.total = 1000  # Initial investment