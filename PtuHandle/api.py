from PtuHandle import ptu
from openpyxl import Workbook

def clone_variant(lst):
    with open('clone.ptu', 'w') as f:
        f.write('\n'.join(lst))

def check_variant(lst, c_switchs):
    result, order = list(), [False]
    for line in lst:
        temp = line.split()
        if temp[0].upper() == 'IF':
            if order[-1] == False:
                if temp[-1].split('!')[-1] not in c_switchs:
                    order.append(True)
                else:
                    order.append(False)
                if temp[-1].startswith('!'):
                    order[-1] = not(order[-1])
            else:
                order.append(True)
            continue
        elif temp[0].upper() == 'ELSE':
            if order[-2] == False:
                order[-1] = not(order[-1])
            continue
        elif ''.join(temp).upper().startswith('ENDIF'):
            order.pop()
            continue
        if order[-1] == False:
            result.append(line)
    return result

def remove_comments(string):
    for key in ptu.comments:
        if string.upper().startswith(key):
            return string
    return string.split('--', maxsplit=1)[0]

def read_raw_file(file_name):
    with open(file_name, 'r') as f:
        raw_content = [remove_comments(line.strip()) for line in f.readlines()]
        return [line.strip() for line in raw_content if line != '']

def read_ptu(file_name, check_var, variant_list=[]):
    raw_cnt = read_raw_file(file_name)
    if check_var is True:
        content = check_variant(raw_cnt, variant_list)
        clone_variant(content)
    else:
        content = raw_cnt
    parser = ptu.Parse(content)
    script = ptu.Script(file_name, parser.get_services())
    return script

def get_content(script, key_list):
    return script.get_content(key_list)

def self_check_script(script):
    script.self_check()

def write_to_excel(file_name, content):
    file_spec = file_name + '.xlsx'
    wb = Workbook()
    ws = wb.active
    ws.title = 'TestSpecification'
    if content != []:
        field_len, row = len(content[0]), 1
        for x in range(len(content)):
            for y in range(field_len):
                cell = ws.cell(column=(1+y), row=(row+x))
                cell.value = content[x][y]
    wb.save(file_spec)


def check_folder_structure(directory):
    pass
