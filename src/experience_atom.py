# experience_atom.py

# Source:
#   "Expertise Browser: A Quantitative Approach to Identifying Expertise"
#   by Audris Mockus et al.

class Delta:
    """
    Represents elementary change to source file; can have a single delta per
    many entities
    """

    def __init__(self, file_len, delta_len, date, time):
        self.file_name = file_name
        self.delta_len = data_len
        self.date = date
        self.time = time

    def __len__(self):
        return self.delta_len

class ExperienceAtom:
    """
    (EA) Basic component of experience determined and measured by deltas --
    small changes to any arbitrary file by a particular developer, organization,
    etc; Each EA is unique to a certain experience gathering entity and to a
    certain delta
    """

    def __init__(self, entity, delta):
        self.entity = entity
        self.delta = delta
