class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = unicode(id)
        self.username = username
        self.password = password
        self.authenticated = False

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.id
