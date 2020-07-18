def check_setup(ser, setup):
    if ser not in setup:
        return ('\tMismatch between test case set up and service\n')
    return ''

def check_name(ser, name):
    if ser not in name:
        return ('\tMismatch between test case name and service\n')
    return ''

def check_prefix(ser, name, pre):
    if not name.startswith(pre):
        return ('\tTest case not starts with ' + pre + '\n')
    return ''
