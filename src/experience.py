# experience.py

# Source:
#   "Expertise Browser: A Quantitative Approach to Identifying Expertise"
#   by Audris Mockus et al.

class Tech:
    pass

class Module:
    pass

class Delta:
    """
    Represents elementary change to source file; can have a single delta per
    many entities
    """

    def __init__(self, file_name, num_insert, num_delete, date_time):
        """ """

        self.file_name = file_name
        self.num_insert = num_insert
        self.num_delete = num_delete
        self.delta_len = num_insert + num_delete
        self.date_time = date_time

    def __len__(self):
        return self.delta_len

class ExperienceAtom:
    """
    (EA) Basic component of experience determined and measured by deltas --
    small changes to any arbitrary file by a particular developer, organization,
    etc; each EA is unique to a certain experience gathering entity and to a
    certain delta, therefore, each EA is owned by a single entity
    """

    def __init__(self, entity, ffile, delta):

        # Two links EA is tieing together
        self.entity = entity
        self.ffile = ffile

        # File delta from which this EA was conceived
        self.delta = delta
