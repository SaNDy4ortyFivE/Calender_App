from services.helpers import configs, custom_logger
from services.meeting_service import get_meetings

def get_value(key):
    global configs
    if key in configs.keys():
        return configs.get(key)
    return None

def print_configs():
    global configs
    for k in configs.keys():
        custom_logger.logger.debug(f'Key:{k}->{configs.get(k)}')

def get_new_meeting_id(conn):
    custom_logger.logger.debug("Generating new meeting id...")
    meeting_ids = get_meetings(conn)
    new_meeting_id = -1
    if len(meeting_ids) == 0:
        new_meeting_id = 1
    else:
        new_meeting_id = max(meeting_ids)[0]
        print(new_meeting_id)
        new_meeting_id += 1
    
    custom_logger.logger.debug("New meeting id generated...")
    return new_meeting_id
