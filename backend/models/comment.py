class Comment:
    def __init__(self, username, description):
        self.username = username
        self.description = description

    def to_dict(self):
        return {
            'username': self.username,
            'description': self.description
        }
