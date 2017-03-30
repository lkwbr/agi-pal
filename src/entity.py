# entity.py

class Entity:
    def __init__(self):
        self.id = ""

class Developer(Entity):
    def __init__(self):
        Entity.__init__(self)

class Organization(Entity):
    def __init__(self):
        Entity.__init__(self)
