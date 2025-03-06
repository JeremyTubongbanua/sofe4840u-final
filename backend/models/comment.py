class Comment:
    def __init__(self, username, description, profile_picture_url=None):
        self.username = username
        self.profile_picture_url = profile_picture_url
        self.description = description

    def to_dict(self):
        return {
            'username': self.username,
            'description': self.description
        }
