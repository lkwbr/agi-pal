# entity.py

from experience import *

class EntityPool:
    """
    Collection of each unique (contributing) entity within organization's
    code base; Entity id's are used to hash each Entity within our pool
    """

    def __init__(self):
        self.pool = {}

    def update(self, entity):
        """ Given an entity, update our pool """

        # Get entity, setting it if non-existent
        self.pool[entity.id] = self.pool.get(entity.id, entity)

    def get(self, name, email):
        """ Get (or, if non-existent, create) an entity with the given email """
        self.pool[email] = self.pool.get(email, Entity(name, email))
        return self.pool[email]

class Entity:
    """ Represents an experience gathering entity """

    def __init__(self, name, email):

        # Identifying information
        self.name = name
        self.email = email
        self.id = email # NOTE: Assuming emails are unique

        # Personal collection of experience atoms
        # NOTE: List is fine, so long as we do not need lookups
        self.ea_list = []

    def add(self, ea):
        """ Update the entity's knowledge with an experience atom """
        if not isinstance(ea, ExperienceAtom): raise ValueError()
        self.ea_list.append(ea)

class Developer(Entity):
    def __init__(self, name, email):
        Entity.__init__(self, name, email)

# TODO: Have Organization be a collection of Developers, obtaining all their EAs
# from them!
class Organization(Entity):
    def __init__(self, name, email):
        Entity.__init__(self, name, email)
