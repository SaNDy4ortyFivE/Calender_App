import os
import click
import configparser

from database import connection

@click.group()
def cli():
    pass

@click.command(name="view-schedule")
@click.option('--person-id', '-p', help='Person ID.')
@click.option('--date', '-d', help='Date (YYYY-MM-DD).', default=None)
@click.option('--config-file', '-c', default='config.properties', help='Path to the configuration file.')
def view_schedule(person_id, date, config_file):

    '''Add helpful comments later'''
    
    #Put config file check in different location later
    if not os.path.exists(config_file):
        click.echo(f"Configuration file '{config_file}' not found.")
        return

    if not person_id:
        click.echo("Person ID is required. Please provide a value for person_id.")
        return

    # Your logic for viewing a person's schedule goes here
    if date:
        click.echo(f"Viewing schedule for Person ID: {person_id} on Date: {date}")
    else:
        click.echo(f"Viewing schedule for Person ID: {person_id}")

@click.command(name="schedule-meeting")
@click.option('--person-id', '-p', help='Person ID.')
@click.option('--date', '-d', help='Date (YYYY-MM-DD).')
@click.option('--from-time', '-f', help='From time (HH:MM).')
@click.option('--to-time', '-t', help='To time (HH:MM).')
@click.option('--config-file', '-c', default='config.properties', help='Path to the configuration file.')
def schedule_meeting(person_id, date, from_time, to_time, config_file):

    '''Add helpful comments later'''

    if not os.path.exists(config_file):
        click.echo(f"Configuration file '{config_file}' not found.")
        return

    
    if not all([person_id, date, from_time, to_time]):
        click.echo("All parameters are required for scheduling a meeting.")
        return
    # Your logic for scheduling a meeting goes here
    # Read database name from config file
    config = configparser.ConfigParser()
    config.read('config.properties')
    DB_FILE = config['database']['db_name']


    db_instance = connection.SQLiteDBConnection(db_file=DB_FILE)
    click.echo(f"Meeting scheduled for Person ID: {person_id}, Date: {date}, From: {from_time}, To: {to_time}")
    
if __name__ == '__main__':
    cli.add_command(schedule_meeting)
    cli.add_command(view_schedule)
    cli()
