# entity.py

from experience import *

class Pool:
    __name__ = "Pool"
    def __init__(self): self.pool = {}
    def get(self, oid): return self.pool.get(oid, None)
    def add(self, obj): self.pool[obj.id] = obj

class FilePool(Pool):
    """ Map each file to a set of contributors """
    __name__ = "FilePool"
    def __init__(self):
        Pool.__init__(self)

class EntityPool(Pool):
    """
    Collection of each unique (contributing) entity within organization's
    code base; Entity id's are used to hash each Entity within our pool
    """
    __name__ = "EntityPool"
    def __init__(self):
        Pool.__init__(self)

class Node:
    """ """

    def __init__(self):
        # Personal collection of experience atoms
        # (List is fine, so long as we do not need lookups)
        self.eas = []
        self.id = None

    def link(self, ea):
        """ Update the entity's knowledge with an experience atom """
        if not isinstance(ea, ExperienceAtom): raise ValueError()
        self.eas.append(ea)

class File(Node):
    """
    Simple file class, attributing to each file a set of distinct developers
    """

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.id = path

class Entity(Node):
    """ Represents an experience gathering entity """

    def __init__(self, name, email):

        super().__init__()

        # Identifying information
        self.name = name
        self.email = email
        self.id = email # NOTE: Assuming emails are unique

class Developer(Entity):
    def __init__(self, name, email):
        super().__init__(name, email)

# TODO: Have Organization be a collection of Developers, obtaining all their EAs
# from them!
class Organization(Entity):
    def __init__(self, name, email):
        super().__init__(name, email)
