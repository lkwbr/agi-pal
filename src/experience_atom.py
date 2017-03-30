# experience_atom.py

# Source:
#   "Expertise Browser: A Quantitative Approach to Identifying Expertise"
#   by Audris Mockus et al.

class Delta:
    """ Represents basic change to source file """

    def __init__(self, delta_len, file_name, date, time):
        self.delta_len = data_len
        self.file_name = file_name
        self.date = date
        self.time = time

    def __len__(self):
        return self.delta_len

class ExperienceAtom:
    """
    (EA) Basic component of experience determined and measured by deltas --
    small changes to any arbitrary file by a particular developer, organization,
    etc.
    """

    def __init__(self, entity, delta):
        self.entity = entity
        self.delta = delta
