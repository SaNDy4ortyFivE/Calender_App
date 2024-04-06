class Person:
    def __init__(self, first_name, last_name, person_id):
        self.first_name = first_name
        self.last_name = last_name
        self.person_id = person_id

    def full_name(self):
        """Return the full name of the person."""
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """Return a string representation of the person."""
        return f"Person ID: {self.person_id}, Name: {self.full_name()}"

# Example of creating and using a Person object
if __name__ == "__main__":
    person = Person("John", "Doe", 1)
    print(person)
    print(f"Full Name: {person.full_name()}")
