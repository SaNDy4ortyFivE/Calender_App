from database.helpers import commit_transactions, fetch_from_db, insert_bulk_records, insert_new_record
from models import meeting, person
from services import scheduler_service
from services.helpers import utilities, custom_logger


def handle_new_single_meeting(person_id: int, date: str, from_time: str, to_time: str) -> None:
    """Schedule a meeting with single person.
    :param person id: Person Id
    :param date: Date, format(YYYY-MM-dd)
    :param from_time: Start Time, 24 Hr format, "HH:MM"
    :param to_time: End Time, 24 Hr format, "HH:MM"
    :return: None
    """
    try:
        #Fetch Table names
        person_table = utilities.get_value("custom_person_table")
        person_id_column = utilities.get_value("custom_person_table_id_column")

        #Check if person id is present in db
        if not check_if_exists_int(person_id_column, person_id, person_table):
            custom_logger.logger.error(f'No Person with ID: {person_id} found in database')
            return
        
        #Check if theres a conflict for this person
        is_conflict = check_meeting_conflict(date, person_id, from_time, to_time)
        if is_conflict:
            custom_logger.logger.error("Conflict Found, not scheduling meeting")
            return 

        custom_logger.logger.debug("No conflicts found for organizer...")

        #Generate new meeting id
        meeting_id = utilities.get_new_meeting_id()

        if meeting_id == -1:
            custom_logger.logger.Error("Could not schedule meeting, as no meeting id was generated.")
            return

        #Create new instance of single meeting
        meeting_instance = meeting.SinglePersonMeeting(meeting_id, date, from_time, to_time)

        custom_logger.logger.debug(f'Creating new person with id={person_id}')
        person_instance = person.Person(person_id)
        custom_logger.logger.debug(f'New person with id={person_id} created')

        custom_logger.logger.debug("Setting this person as organizer...")
        meeting_instance.set_organizer(person_instance)

        if not insert_meeting(meeting_instance):
            custom_logger.logger.debug("Meeting not scheduled")
            return
        if commit_transactions():
            custom_logger.logger.debug("Meeting scheduled successfully.")
        else:
            custom_logger.logger.error("Meeting not scheduled.")
    except Exception as e:
        custom_logger.logger.error("Error occured when scheduling new single meeting" + repr(e), exc_info=True)
    



def handle_new_multiple_meeting(person_id, date, from_time, to_time, participants, meeting_room):
    """Schedule a meeting with multiple persons with room
    :param person id: Person Id
    :param date: Date, format(YYYY-MM-dd)
    :param from_time: Start Time, 24 Hr format, "HH:MM"
    :param to_time: End Time, 24 Hr format, "HH:MM"
    :param participants: List of person ids
    :meeting_room: Room number for a meeting to schedule
    :return: None
    """
    try:
        #Check for organizer conflict
        is_conflict = check_meeting_conflict(date, person_id, from_time, to_time)

        if is_conflict:
            custom_logger.logger.debug("Conflict Found, not scheduling meeting")
            return 

        custom_logger.logger.debug("No conflicts found for organizer...")

        #Check for participants conflict
        are_conflicts = check_meeting_conflict_multiple(participants, date, from_time, to_time)

        if are_conflicts:
            custom_logger.logger.debug("Conflict Found for Participants, not scheduling meeting")
            return 

        custom_logger.logger.debug("No conflicts found for participants...")

        #Generate new meeting id
        meeting_id = utilities.get_new_meeting_id()

        if meeting_id == -1:
            custom_logger.logger.Error("Could not schedule meeting, as no meeting id was generated.")
            return

        #Create new instance of multi meeting
        meeting_instance = meeting.MultiPersonMeeting(meeting_id, date, from_time, to_time, meeting_room)

        custom_logger.logger.debug(f'Creating new person with id={person_id}')
        person_instance = person.Person(person_id)
        custom_logger.logger.debug(f'New person with id={person_id} created')

        custom_logger.logger.debug("Setting this person as organizer...")
        meeting_instance.set_organizer(person_instance)

        #Add participants for this meeting
        for p in participants:
            meeting_instance.add_participant(person.Person(p))

        if not insert_meeting(meeting_instance):
            custom_logger.logger.error("Meeting not scheduled")
            return

        if not insert_meeting_members(meeting_instance.meeting_id, meeting_instance.get_participants()):
            custom_logger.logger.error("Meeting not scheduled")
            return

        if not insert_room(meeting_instance.meeting_id, meeting_room):
            custom_logger.logger.error("Meeting not scheduled")
            return
    
        if commit_transactions():
            custom_logger.logger.debug("Meeting scheduled successfully.")
        else:
            custom_logger.logger.error("Meeting not scheduled.")
    except Exception as e:
        custom_logger.logger.error("Error occured when scheduling new multi meeting:" + repr(e), exc_info=True)





def insert_meeting(meeting_instance, is_multiple=False):
    """Insert a new meeting record into the meetings table.
    :param conn: Connection object
    :param meeting_data: Tuple containing meeting data (meeting_id, date, start_time, end_time, ...)
    :return: None
    """
    is_meeting_inserted = False
    try:
        custom_logger.logger.debug("Trying to insert new meeting...")

        #add support for meeting room later
        meeting_table = utilities.get_value("custom_meeting_table")
        meeting_sql = " INSERT INTO " + meeting_table + " (id, date, from_time, to_time) " \
                  " VALUES(?,?,?,?) "

        
        if insert_new_record(meeting_sql, meeting_instance.get_tuple_representation_for_meeting()):
            custom_logger.logger.debug("Meeting inserted into Databse")
            custom_logger.logger.debug("Trying to insert Members")
            if insert_meeting_member(meeting_instance.meeting_id, meeting_instance.get_organizer().person_id):
                custom_logger.logger.debug("Members added for Meeting into Database")
                #Set to true
                is_meeting_inserted = True
            else:
                custom_logger.logger.error("Members not inserted")
        else:
            custom_logger.logger.error("Meeting not inserted")
    except Exception as e:
        custom_logger.logger.error("Error occured when inserting new single meeting into Database:" + repr(e), exc_info=True)
    
    return is_meeting_inserted




def insert_meeting_member(meeting_id, person_id):
    '''Inserts a meeting member into database'''
    is_member_inserted = False
    try:
        meeting_member_table = utilities.get_value("custom_meeting_member_table")
        meeting_member_sql = "INSERT INTO " + meeting_member_table + "(meeting_id, person_id)" \
                  "VALUES(?,?) "
        if insert_new_record(meeting_member_sql, (meeting_id, person_id)):
            custom_logger.logger.debug("Meeting Member added")
            is_member_inserted = True
        else:
            custom_logger.logger.error("Meeting Member not added")
    except Exception as e:
        custom_logger.logger.error("Error occured when inserting meeting member into Database:" + repr(e), exc_info=True)
    return is_member_inserted



def insert_meeting_members(meeting_id, participants):
    '''Inserts participants into database for a meeting'''
    #Fetch Table names
    members_inserted = False
    try:
        meeting_member_table = utilities.get_value("custom_meeting_member_table")
        meeting_member_sql = "INSERT INTO " + meeting_member_table + "(meeting_id, person_id)" \
                  "VALUES(?,?) "
        values = []

        for p in participants:
            values.append((meeting_id, p.person_id))
        if insert_bulk_records(meeting_member_sql, values):
            custom_logger.logger.debug("Meeting Members added")
            members_inserted = True
        else:
            custom_logger.logger.error("Meeting Members not added")
    except Exception as e:
        custom_logger.logger.error("Error occured when inserting meeting members into Database:" + repr(e), exc_info=True)
    return members_inserted 




def insert_room(meeting_id, room_number):
    '''Inserted meeting room along with meeting id'''
    meeting_room_inserted = False
    try:
        meeting_room_table = utilities.get_value("custom_meeting_room")
        meeting_room_sql = "SELECT id FROM " + meeting_room_table + " where room_number=?";
        result = fetch_from_db(meeting_room_sql, (room_number,))

        if len(result) == 1:
            meeting_det_table = utilities.get_value("custom_meeting_details")
            meeting_det_sql = "INSERT INTO " + meeting_det_table + "(id, room_id)" \
                            "VALUES(?,?)"
            if insert_new_record(meeting_det_sql, (meeting_id, result[0][0])):
                custom_logger.logger.debug("Meeting Room Booked")
                meeting_room_inserted = True
            else:
                custom_logger.logger.error("Meeting Room not Booked")
    except Exception as e:
        custom_logger.logger.error("Error occured when booking meeting room into Database:" + repr(e), exc_info=True)
    return meeting_room_inserted



def check_meeting_conflict(date, person_id, start_time, end_time):
    '''Check if there are any conflicts if this meeting is scheduled'''
    is_conflict = False
    try:
        #get all meeting for this person
        custom_logger.logger.debug("Checking for conflicts")
        meeting_table = utilities.get_value("custom_meeting_table")
        meeting_member_table = utilities.get_value("custom_meeting_member_table")
        meetings_sql = "SELECT id, date, from_time, to_time FROM " + meeting_table + " " \
                        " WHERE date=? AND id in " \
                        "( SELECT meeting_id FROM " + meeting_member_table + " where person_id=?)"
        #Fetch all meetings on this date for this person
        meeting_records = fetch_from_db(meetings_sql, (date, person_id))

        #Add all meeting timings to list
        time_windows = [(from_time, to_time) for id, date, from_time, to_time in meeting_records]
        #Append current meeting time
        time_windows.append((start_time, end_time))

        conflicts = scheduler_service.has_conflict(time_windows)

        if not conflicts is None:
            custom_logger.logger.debug(f"Conflict Found for Person:{person_id}")
            custom_logger.logger.debug(f'Meeting 1:{conflicts[0][0]}-{conflicts[0][1]}')
            custom_logger.logger.debug(f'Meeting 2:{conflicts[1][0]}-{conflicts[1][1]}')
            is_conflict=True
    except Exception as e:
        custom_logger.logger.error("Error when checking for conflicts:" + repr(e), exc_info=True)   
    return is_conflict






def check_meeting_conflict_multiple(participants, date, start_time, end_time):
    '''Checks conflicts for all participants'''

    is_conflict = False
    try:
        custom_logger.logger.debug("Checking for participant conflicts")
        for p in participants:
            if check_meeting_conflict(date, p, start_time, end_time):
                is_conflict = True
    except Exception as e:
        custom_logger.logger.error("Error when checking for participants conflicts:" + repr(e), exc_info=True)
       
    return is_conflict





def view_meetings(person_id):
    """View Meeting for a particular person.
    :param person id: Person Id
    :return: None
    """

    #Fetch Table names
    meeting_table = utilities.get_value("custom_meeting_table")
    meeting_member_table = utilities.get_value("custom_meeting_member_table")
    person_table = utilities.get_value("custom_person_table")
    person_id_column = utilities.get_value("custom_person_table_id_column")

    #Check if person id is present in db
    if not check_if_exists_int(person_id_column, person_id, person_table):
        custom_logger.logger.error(f'No Person with ID: {person_id} found in database')
        return

    view_meeting_sql = " SELECT MM.person_id, M.date, M.from_time, m.to_time FROM " + meeting_table + " M " \
                        " inner join " +   meeting_member_table + " MM " \
                        " on M.id=MM.meeting_id " \
                        " and MM.person_id=?" \
                        " order by M.date, M.from_time"
    
    results = fetch_from_db(view_meeting_sql, (person_id,))
    
    custom_logger.logger.debug("---------")
    for m in results:
        custom_logger.logger.debug(f'Date:{m[1]}, from {m[2]} to {m[3]}')
        custom_logger.logger.debug("---------")




def get_meetings():
    """Get all scheduled meetings for everyone.
    :return: List of meeting Ids
    """
    results = []
    try:
        custom_logger.logger.debug("Getting all meetings...")
        meeting_table = utilities.get_value("custom_meeting_table")
        get_meetings_sql = " SELECT id FROM " + meeting_table

        results = fetch_from_db(get_meetings_sql, ())
        custom_logger.logger.debug(f'Total Meetings Fetched:{len(results)}')
    except Exception as e:
        custom_logger.logger.error("Error getting meetings" + e)
    return results

def check_if_exists_int(column_name, value, table):
    does_exist = False
    try:
        sql_str = "SELECT * FROM " + table + " WHERE " + column_name + "=?"
        results = fetch_from_db(sql_str, (value,))
        if len(results) > 0:
            does_exist = True
    except Exception as e:
        custom_logger.logger.error("Error checking value in Database:" + repr(e), exc_info=True)
    return does_exist
    