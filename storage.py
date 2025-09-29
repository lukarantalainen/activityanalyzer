import tools
from config import TIME_DATA, MOUSE_DATA, KB_DATA, PROGRAM_NAMES

tools.create_files()
time_data = tools.load_json(TIME_DATA)
mouse_data = tools.load_json(MOUSE_DATA)
kb_data = tools.load_json(KB_DATA)
program_names = tools.load_json(PROGRAM_NAMES)
