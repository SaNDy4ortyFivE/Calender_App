#testing import
from person import Person

class Meeting:
    def __init__(self, meeting_id, date, start_time, end_time, participants=None):
        self.meeting_id = meeting_id
        self.date = date  # Expected format "YYYY-MM-DD"
        self.start_time = start_time  # Expected format "HH:MM"
        self.end_time = end_time  # Expected format "HH:MM"
        self.participants = participants if participants else []

    def add_participant(self, person):
        """Add a participant to the meeting."""
        if person not in self.participants:
            self.participants.append(person)

    def remove_participant(self, person):
        """Remove a participant from the meeting."""
        if person in self.participants:
            self.participants.remove(person)

    def __str__(self):
        """Return a string representation of the meeting."""
        participants_names = ', '.join([p.full_name() for p in self.participants])
        return (f"Meeting ID: {self.meeting_id}, Date: {self.date}, Start Time: {self.start_time}, "
                f"End Time: {self.end_time}, Participants: {participants_names}")

# Example usage
if __name__ == "__main__":
    # Assuming a Person class exists and has a method full_name()
    john = Person("John", "Doe", 1)
    jane = Person("Jane", "Doe", 2)
    
    meeting = Meeting(meeting_id=1, date="2024-04-08", start_time="09:00", end_time="10:00")
    meeting.add_participant(john)
    meeting.add_participant(jane)
    
    print(meeting)
