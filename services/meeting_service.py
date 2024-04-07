from services import scheduler_service
from services.helpers import utilities, custom_logger

def insert_meeting(conn, meeting_instance):
    """Insert a new meeting record into the meetings table.
    :param conn: Connection object
    :param meeting_data: Tuple containing meeting data (meeting_id, date, start_time, end_time, ...)
    :return: None
    """
    custom_logger.logger.debug("Trying to insert new meeting...")
    #single person
    conflicts = check_meeting_conflict(conn, meeting_instance)
    if not conflicts is None:
        custom_logger.logger.debug("Conflict Found, not scheduling meeting")
        custom_logger.logger.debug(f'Meeting 1:{conflicts[0][0]}-{conflicts[0][1]}')
        custom_logger.logger.debug(f'Meeting 2:{conflicts[1][0]}-{conflicts[1][1]}')
        return 

    custom_logger.logger.debug("No conflicts found...")
    '''if check_meeting_conflict_multiple(conn, meeting_instance):
        print("Conflict Found in participants, not scheduling meeting")
        return'''
    
    #add support for meeting room later
    meeting_table = utilities.get_value("custom_meeting_table")
    meeting_member_table = utilities.get_value("custom_meeting_member_table")
    meeting_sql = " INSERT INTO " + meeting_table + " (id, date, from_time, to_time) " \
              " VALUES(?,?,?,?) "
    #custom_logger.logger.debug(f'Insert Query:{meeting_sql}')
    cur = conn.cursor()
    cur.execute(meeting_sql, meeting_instance.get_tuple_representation_for_meeting())

    meeting_member_sql = "INSERT INTO " + meeting_member_table + "(meeting_id, person_id)" \
              "VALUES(?,?) "
    #custom_logger.logger.debug(f'Insert Query:{meeting_member_sql}')
    cur.execute(meeting_member_sql, (meeting_instance.meeting_id, meeting_instance.get_organizer().person_id))

    '''for p in meeting_instance.get_participants():
        cur.execute(meeting_member_sql, (meeting_instance.meeting_id, p.person_id))'''

    conn.commit()
    print("Meeting scheduled successfully.")

def check_meeting_conflict(conn, meeting_instance):
    #get all meeting for this person
    custom_logger.logger.debug("Checking for conflicts")
    meeting_table = utilities.get_value("custom_meeting_table")
    meeting_member_table = utilities.get_value("custom_meeting_member_table")
    meetings_sql = "SELECT id, date, from_time, to_time FROM " + meeting_table + " " \
                    " WHERE date=? AND id in " \
                    "( SELECT meeting_id FROM " + meeting_member_table + " where person_id=?)"
    cur = conn.cursor()
    cur.execute(meetings_sql, (meeting_instance.date, meeting_instance.get_organizer().person_id))

    meeting_records = cur.fetchall()

    time_windows = [(from_time, to_time) for id, date, from_time, to_time in meeting_records]
    time_windows.append((meeting_instance.start_time, meeting_instance.end_time))

    return scheduler_service.has_conflict(time_windows)

def check_meeting_conflict_multiple(conn, meeting_instance):
    #get all meeting for this person

    is_conflict = False
    for p in meeting_instance.get_participants():
        meetings_sql = '''SELECT id, date, from_time, to_time FROM Meeting WHERE date=? AND id in ( SELECT meeting_id FROM MeetingMember where person_id=?)'''
        cur = conn.cursor()
        cur.execute(meetings_sql, (meeting_instance.date, p.person_id))

        meeting_records = cur.fetchall()

        for r in meeting_records:
            print(r[0])
            print(r[1])
            print(r[2])
            print(r[3])

        time_windows = [(from_time, to_time) for id, date, from_time, to_time in meeting_records]
        time_windows.append((meeting_instance.start_time, meeting_instance.end_time))

        if scheduler_service.has_conflict(time_windows):
            is_conflict = True
            break
    return is_conflict

def view_meetings(conn, person, date=None):
    """View Meeting for a particular person.
    :param conn: Connection object
    :param person: Person Object
    :return: None
    """
    meeting_table = utilities.get_value("custom_meeting_table")
    meeting_member_table = utilities.get_value("custom_meeting_member_table")

    view_meeting_sql = " SELECT MM.person_id, M.date, M.from_time, m.to_time FROM " + meeting_table + " M " \
                        " inner join " +   meeting_member_table + " MM " \
                        " on M.id=MM.meeting_id " \
                        " and MM.person_id=?" \
                        " order by M.date, M.from_time"
    
    cur = conn.cursor()
    cur.execute(view_meeting_sql, [(person.person_id)])
    
    custom_logger.logger.debug("---------")
    for m in cur.fetchall():
        custom_logger.logger.debug(f'Date:{m[1]}, from {m[2]} to {m[3]}')
        custom_logger.logger.debug("---------")
        
def get_meetings(conn):
    """Get all scheduled meetings for everyone.
    :return: List of meeting Ids
    """
    custom_logger.logger.debug("Getting all meetings...")
    meeting_table = utilities.get_value("custom_meeting_table")
    get_meetings_sql = " SELECT id FROM " + meeting_table;
    cur = conn.cursor()
    cur.execute(get_meetings_sql)
    results = cur.fetchall()
    custom_logger.logger.debug(f'Total Meetings Fetched:{len(results)}')
    return results