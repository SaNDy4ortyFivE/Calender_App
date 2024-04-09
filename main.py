import click

from services import meeting_service
from services.helpers import custom_logger

@click.group()
def cli():
    pass

@click.command(name="view-schedule")
@click.option('--person-id', '-p', help='Person ID.', type=int)
def view_schedule(person_id):

    '''View Meetings for a Particular Person
    '''
 
    if not person_id:
        custom_logger.logger.error('Person ID is required. Please provide a value for person id.')
        return
    custom_logger.logger.debug(f"Viewing schedule for Person ID: {person_id}")
    meeting_service.view_meetings(person_id)




@click.command(name="schedule-meeting")
@click.option('--person-id', '-p', help='Person ID.', type=int)
@click.option('--date', '-d', help='Date (YYYY-MM-DD).')
@click.option('--from-time', '-f', help='From time (HH:MM).')
@click.option('--to-time', '-t', help='To time (HH:MM).')
def schedule_meeting(person_id, date, from_time, to_time):

    '''Schedule a new Meeting(Single Person)'''

    if not all([person_id, date, from_time, to_time]):
        custom_logger.logger.Error("All parameters are required for scheduling a meeting.")
        return
    
    meeting_service.handle_new_single_meeting(person_id, date, from_time, to_time)




@click.command(name="schedule-meeting-multiple")
@click.option('--person-id', '-p', help='Person ID.', type=int)
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

    #Split person_id string, into list
    pts = [pt.strip() for pt in participants.split(',')]
    custom_logger.logger.debug(f'Received {len(pts)} participants...')
    
    meeting_service.handle_new_multiple_meeting(person_id, date, from_time, to_time, pts, meeting_room)



if __name__ == '__main__':
    custom_logger.logger.debug("-"*50)
    cli.add_command(schedule_meeting)
    cli.add_command(view_schedule)
    cli.add_command(schedule_meeting_multiple)
    cli()
