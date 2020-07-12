from PtuHandle import ptu


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
    parser.initialize()
    return ptu.Script(file_name, parser.get_services())


def check_folder_structure(directory):
    pass
