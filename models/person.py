class Person:
    '''Represents a Person'''
    def __init__(self, person_id, first_name=None, last_name=None):
        self.first_name = first_name
        self.last_name = last_name
        self.person_id = person_id

    def full_name(self):
        """Return the full name of the person."""
        return f"{self.first_name} {self.last_name}"

    '''Required when checking if person is present in a list or not'''
    def __eq__(self, other_person):
        if isinstance(other_person, Person):
            if other_person.person_id == self.person_id:
                return True
        return False
    
    def __str__(self):
        """Return a string representation of the person."""
        return f"Person ID: {self.person_id}, Name: {self.full_name()}"
