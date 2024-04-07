import click

from database import db_instance
from models import meeting, person
from services import meeting_service
from services.helpers import custom_logger
from services.helpers.utilities import get_new_meeting_id

@click.group()
def cli():
    pass

@click.command(name="view-schedule")
@click.option('--person-id', '-p', help='Person ID.', type=int)
@click.option('--date', '-d', help='Date (YYYY-MM-DD).', default=None)
def view_schedule(person_id, date):

    '''View Meetings for a Particular Person at a given Date'''
 
    if not person_id:
        custom_logger.logger.debug('Person ID is required. Please provide a value for person_id.')
        return
    person_instance = person.Person(person_id)
    # logic for viewing a person's schedule
    if date:
        custom_logger.logger.debug(f"Viewing schedule for Person ID: {person_id} on Date: {date}")
        #complete this later
    else:
        custom_logger.logger.debug(f"Viewing schedule for Person ID: {person_id}")
        meeting_service.view_meetings(db_instance.conn, person_instance)




@click.command(name="schedule-meeting")
@click.option('--person-id', '-p', help='Person ID.')
@click.option('--date', '-d', help='Date (YYYY-MM-DD).')
@click.option('--from-time', '-f', help='From time (HH:MM).')
@click.option('--to-time', '-t', help='To time (HH:MM).')
def schedule_meeting(person_id, date, from_time, to_time):

    '''Schedule a new Meeting(Single Person)'''

    if not all([person_id, date, from_time, to_time]):
        custom_logger.logger.Error("All parameters are required for scheduling a meeting.")
        return
    
    meeting_instance = meeting.Meeting(get_new_meeting_id(db_instance.conn), date, from_time, to_time)
    custom_logger.logger.debug("Creating new person...")
    person_instance = person.Person(person_id)
    custom_logger.logger.debug("Setting this person as organizer...")
    meeting_instance.set_organizer(person_instance)
    meeting_service.insert_meeting(db_instance.conn, meeting_instance)




@click.command(name="schedule-meeting-multiple")
@click.option('--person-id', '-p', help='Person ID.')
@click.option('--date', '-d', help='Date (YYYY-MM-DD).', default=None)
@click.option('--from-time', '-f', help='From time (HH:MM).')
@click.option('--to-time', '-t', help='To time (HH:MM).')
@click.option('--meeting-room', '-m', help='Meeting Room.')
@click.option('--participants', '-pt', help='Participants.Person1, Person2, Person3,...')
def schedule_meeting_multiple(person_id, date, from_time, to_time, meeting_room, participants):

    '''Schedule a Meeting(Multiple Persons with Room)'''

    if not all([person_id, date, from_time, to_time, meeting_room, participants]):
        click.echo("All parameters are required for scheduling a meeting.")
        return

    meeting_instance = meeting.Meeting(get_new_meeting_id(), date, from_time, to_time)
    person_instance = person.Person(person_id)
    meeting_instance.set_organizer(person_instance)

    pts = [pt.strip() for pt in participants.split(',')]

    for pt in pts:
        pt_instance = person.Person(pt)
        meeting_instance.add_participant(pt_instance)

    meeting_service.insert_meeting(db_instance.conn, meeting_instance)
    click.echo(f"Meeting scheduled for Person ID: {person_id}, Date: {date}, From: {from_time}, To: {to_time}")



if __name__ == '__main__':
    cli.add_command(schedule_meeting)
    cli.add_command(view_schedule)
    cli.add_command(schedule_meeting_multiple)
    cli()
