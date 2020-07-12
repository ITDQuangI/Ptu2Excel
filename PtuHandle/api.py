from PtuHandle import ptu
from openpyxl import Workbook

def remove_comments(string):
    for key in ptu.comments:
        if string.upper().startswith(key):
            return string
    return string.split('--', maxsplit=1)[0]


def read_raw_file(file_name):
    with open(file_name, 'r') as f:
        raw_content = [remove_comments(line.strip()) for line in f.readlines()]
        return [line.strip() for line in raw_content if line != '']


def read_ptu(file_name):
    parser = ptu.Parse(read_raw_file(file_name))
    script = ptu.Script(file_name, parser.get_services())
    return script


def get_content(script, key_list):
    return script.get_content(key_list)


def write_to_excel(file_name, content):
    file_spec = file_name + '.xlsx'
    wb = Workbook()
    ws = wb.active
    ws.title = 'TestSpecification'
    field_len, row = len(content[0]), 1
    for x in range(len(content)):
        for y in range(field_len):
            cell = ws.cell(column=(1+y), row=(row+x))
            cell.value = content[x][y]
    wb.save(file_spec)


def check_folder_structure(directory):
    pass
