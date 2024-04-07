from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('config.env')
load_dotenv(dotenv_path=dotenv_path)
configs = dict()

for d in os.environ.keys():
    if d.lower().startswith('custom'):
        configs[d.lower()]=os.getenv(d)
