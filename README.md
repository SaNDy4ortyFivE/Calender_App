# Calender_App
 Calender Application (Kpoint Assignment)

#### Contracts/Assumptions
- All Person ID's, Room Numbers, Room ID's are present in Database. Any different value which is not present, will lead to an inconsistent state.
- Conflict checking considers only meetings on a particular day. i.e Conflict between meeting on Day 1 and another meeting which starts on Day 1 and ends on Day 2 will not be considered.
- Meeting cannot start on a particular day and end on next day. It mush finish on that day itself.
- Date Format: YYYY-MM-DD String.  
Example: "2024-09-05", "2024-12-05"
- Time Format: 24 Hour HH:MM String.  
Example: "11:00", "12:00". "13:00", "23:00"
- Meeting Start Time is always less than Meeting End Time.
- If any conflicts are found in meeting timings, meeting is not scheduled
- In case of no conflicts, room availability is not checked. i.e There may be a case when two different meetings with different participants can book a same room.
- All Id's are integers
- All dates and timings provided are valid and in correct format
- Test cases have been written as much as possible in given time frame, but following files are out of scope for Testing:  
    1. database/initialize_db.py

#### Given more time, I would have expanded the functionality to include additional features:
- Robust Logging mechanism
- More extensive Test Cases
- Adding support for inserting new Persons and Rooms from program itself

### Development Environment
- Python: 3.8.6rc1
- SQLite version: 2.6.0

### Usage Instructions

> Please make sure config.env in present in projects root folder

> Run pip install -r requirements.txt

> Log files are generated inside logs folder. Sinlge Log file

1. **Initializing Database**  
> Sample Database db file provided. Only proceed when new DB is required.
Execute __./database/initialize_db.py__ from root project directory
```
(Windows)
python .\database\initialize_db.py
```
This script creates the SQLite Database if not present and inserts records according to statements in file __sample_rows_insert.sql__

2. **Scheduling a Single Person Meeting**  
```
python .\main.py schedule-meeting -p 1 -d "2024-04-09" -f "11:20" -t "13:30"
```

3. **Scheduling a Multi Person Meeting with Room**
```
 python .\main.py schedule-meeting-multiple -p 2 -d "2024-04-09" -f "16:30" -t "17:00" -m 102 -pt "1,3"
```

4. **Getting help for a particular command**
```
python .\main.py --help
```
```
python .\main.py schedule-meeting --help
```
```
python .\main.py schedule-meeting-multiple --help
```

5. **View Schedule for a Person**
```
python .\main.py view-schedule -p 1
```

6. **Running Test Cases**
```
pytest .\tests\
```

### Sample Run After Database Initialization
```
python .\main.py schedule-meeting -p 1 -d "2024-04-09" -f "11:00" -t "12:00"
python .\main.py schedule-meeting -p 2 -d "2024-04-09" -f "11:00" -t "13:00"
python .\main.py schedule-meeting -p 3 -d "2024-04-09" -f "15:00" -t "17:00"
python .\main.py schedule-meeting-multiple -p 1 -d "2024-04-09" -f "13:00" -t "14:00" -m 101 -pt "2,3"
python .\main.py schedule-meeting -p 1 -d "2024-04-09" -f "11:20" -t "13:30"
python .\main.py schedule-meeting-multiple -p 2 -d "2024-04-09" -f "13:30" -t "14:30" -m 102 -pt "1,3"
python .\main.py view-schedule -p 1
```

### Database Schemas

> Sample Database db file provided. If new file is to be created please delete the original one and execute Step 1 from Instructions

1. Person: Stores Person Info
```
id INTEGER PRIMARY KEY,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL
```

2. Meeting: Stores Meeting Info
```
id INTEGER PRIMARY KEY,
date DATE NOT NULL,
from_time TEXT NOT NULL,
to_time TEXT NOT NULL
```

3. Meeting Room: Stores Meeting Room Info
```
id INTEGER PRIMARY KEY,
room_name TEXT NOT NULL,
room_number INTEGER NOT NULL
```

4. Meeting Member: Stores Meeting Participants
```
meeting_id INTEGER,
person_id INTEGER,
FOREIGN KEY(meeting_id) REFERENCES Meeting(id),
FOREIGN KEY(person_id) REFERENCES Person(id)
```

5. Meeting Detail: Stores Meeting Id with Meeting Room
```
id INTEGER PRIMARY KEY,
room_id INTEGER,
FOREIGN KEY(room_id) REFERENCES MeetingRoom(id)
```
<hr>
> Please feel free to reach out in case of any problems/issues. Thank you