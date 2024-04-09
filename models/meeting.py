from models.person import Person


class Meeting:

    '''
    Represents a meeting

    Attributes:
        meeting_id(int): unique meeting id
        date(str): scheduled date
        start_time(str): start time for this meeting. Format:- HH:MM, 24 Hr
        end_time(str): end time for this meeting. Format:- HH:MM, 24 Hr
    '''

    def __init__(self, meeting_id: int, date: str, start_time: str, end_time: str):
        self.meeting_id = meeting_id
        self.date = date  # Expected format "YYYY-MM-DD"
        self.start_time = start_time  # Expected format "HH:MM"
        self.end_time = end_time  # Expected format "HH:MM"


    def get_tuple_representation_for_meeting(self):
        '''Returns a tuple containing all attributes. Required for prepared statements'''
        return (self.meeting_id, self.date, self.start_time, self.end_time)
    

    def __str__(self):
        """Return a string representation of the meeting."""
        return (f"Meeting ID: {self.meeting_id}, Date: {self.date}, Start Time: {self.start_time}, "
                f"End Time: {self.end_time}")




class SinglePersonMeeting(Meeting):

    '''
    Represents a meeting with single person

    Attributes:
        meeting_id(int): unique meeting id
        date(str): scheduled date
        start_time(str): start time for this meeting. Format:- HH:MM, 24 Hr
        end_time(str): end time for this meeting. Format:- HH:MM, 24 Hr
        organizer(Person): Organizer for this Meeting
    '''

    def __init__(self, meeting_id: int, date: str, start_time: str, end_time: str, oraganizer:Person):
        super().__init__(meeting_id, date, start_time, end_time)
        self.organizer = oraganizer

    def set_organizer(self, organizer):
        '''Sets the organizer for this meeting'''
        self.organizer = organizer

    def get_organizer(self):
        return self.organizer
    
    def __str__(self):
        '''Return a string representation of the SinglePersonMeeting.'''
        return (super().__str__(),
                f"Organizer: {self.get_organizer()}")





class MultiPersonMeeting(SinglePersonMeeting):

    '''
    Represents a meeting with multiple persons

    Attributes:
        meeting_id(int): unique meeting id
        date(str): scheduled date
        start_time(str): start time for this meeting. Format:- HH:MM, 24 Hr
        end_time(str): end time for this meeting. Format:- HH:MM, 24 Hr
        meeting_room(int): Room number for meeting
        organizer(Person): Organizer for this Meeting
        participants(List of Persons): Participants for this meeting
    '''

    def __init__(self, meeting_id: int, date: str, start_time: str, end_time: str, meeting_room: int, oraganizer:Person, participants: list=None):
        super().__init__(meeting_id, date, start_time, end_time, oraganizer)
        self.participants = participants if participants else []
        self.meeting_room = meeting_room

    def add_participant(self, person):
        """Add a participant to the meeting."""
        if person not in self.participants:
            self.participants.append(person)

    def remove_participant(self, person):
        """Remove a participant from the meeting."""
        if person in self.participants:
            self.participants.remove(person)

    def get_participants(self):
        return self.participants
    
    def __str__(self):
        """Return a string representation of the MultiPersonMeeting."""
        participants_names = ', '.join([p.full_name() for p in self.participants])
        return (super().__str__(),
                f"Participants: {participants_names}", f'Meeting Room:{self.meeting_room}')