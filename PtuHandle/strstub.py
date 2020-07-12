ttable = {
    '0': '0th',
    '1': '1st',
    '2': '2nd',
    '3': '3rd',
    '4': '4th',
    '5': '5th',
    '6': '6th',
    '7': '7th',
    '8': '8th',
    '9': '9th'
}

def stub_get_info(string):
    temp = string.split('(', maxsplit=1)
    stub_name = temp[0].strip()
    stub_para = '(' + temp[1]
    count = 0
    for i in range(len(stub_para)):
        if stub_para[i] == '(':
            count += 1
        elif stub_para[i] == ')':
            count -= 1
        if count == 0:
            break
    stub_name = stub_name.replace('=>', '').strip()
    stub_name, stub_time = stub_get_calltime(stub_name)
    return [stub_name, stub_para[:i + 1], stub_para[i + 1:].strip(), stub_time]

def stub_get_calltime(string):
    times = string.split(maxsplit=1)
    if times[0] == string:
        return [string, '']
    else:
        return [
        times[0],
        [t.strip()[:-1] + ttable[t.strip()[-1]] for t in times[1].split('..')]
        ]
