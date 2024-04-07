#testing import
from models import person

class Meeting:
    def __init__(self, meeting_id, date, start_time, end_time, oraganizer=None, participants=None):
        self.meeting_id = meeting_id
        self.date = date  # Expected format "YYYY-MM-DD"
        self.start_time = start_time  # Expected format "HH:MM"
        self.end_time = end_time  # Expected format "HH:MM"
        self.organizer = oraganizer if oraganizer else None
        self.participants = participants if participants else []

    def add_participant(self, person):
        """Add a participant to the meeting."""
        if person not in self.participants:
            self.participants.append(person)

    def remove_participant(self, person):
        """Remove a participant from the meeting."""
        if person in self.participants:
            self.participants.remove(person)

    def set_organizer(self, organizer):
        self.organizer = organizer

    def get_organizer(self):
        return self.organizer

    def get_tuple_representation_for_meeting(self):
        return (self.meeting_id, self.date, self.start_time, self.end_time)
    
    def get_participants(self):
        return self.participants

    def __str__(self):
        """Return a string representation of the meeting."""
        participants_names = ', '.join([p.full_name() for p in self.participants])
        return (f"Meeting ID: {self.meeting_id}, Date: {self.date}, Start Time: {self.start_time}, "
                f"End Time: {self.end_time}, Participants: {participants_names}")

# Example usage
if __name__ == "__main__":
    # Assuming a Person class exists and has a method full_name()
    john = person.Person("John", "Doe", 1)
    jane = person.Person("Jane", "Doe", 2)
    
    meeting = Meeting(meeting_id=1, date="2024-04-08", start_time="09:00", end_time="10:00")
    meeting.add_participant(john)
    meeting.add_participant(jane)
    
    print(meeting)
