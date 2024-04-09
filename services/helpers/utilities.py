import services
from services.helpers import configs, custom_logger


def get_value(key):
    '''Returns a value from config, None if key not found'''
    global configs
    if key in configs.keys():
        return configs.get(key)
    return None



def print_configs():
    global configs
    for k in configs.keys():
        custom_logger.logger.debug(f'Key:{k}->{configs.get(k)}')



def get_new_meeting_id():
    custom_logger.logger.debug("Generating new meeting id...")
    new_meeting_id = -1

    try:
        meeting_ids = services.meeting_service.get_meetings()
        if len(meeting_ids) == 0:
            new_meeting_id = 1
        else:
            new_meeting_id = max(meeting_ids)[0]
            new_meeting_id += 1
        custom_logger.logger.debug("New meeting id generated...")
        custom_logger.logger.debug(f'New meeting id {new_meeting_id}')
    except Exception as e:
        custom_logger.logger.error("Error occurred when generating meeting id:" + repr(e), exc_info=True)
    
    
    return new_meeting_id
