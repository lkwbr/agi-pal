# entity.py

class Entity:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.id = email # NOTE: Assuming emails are unique

class Developer(Entity):
    def __init__(self):
        Entity.__init__(self)

class Organization(Entity):
    def __init__(self):
        Entity.__init__(self)
