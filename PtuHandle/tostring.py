def stub_out(name, para, ret, time):
    temp = 'Call function ' + name + para
    if time != '':
        if len(time) == 1:
            temp += (' at ' + time[0])
        else:
            temp += (' from ' + time[0] + ' to ' + time[1])
    return temp

def stub_in(name, para, ret, time):
    temp = 'Return value '
    if time != '':
        if len(time) == 1:
            temp += ('at ' + time[0])
        else:
            temp += ('from ' + time[0] + ' to ' + time[1])
    else:
        temp += 'of'
    temp += ' calling function ' + name + para + ' is ' + ret
    return temp

def array_in(name, init):
    return 'Array: ' + name + ' = ' + init

def array_out(name, ev):
    return 'Array: ' + name + ' = ' + ev

def struct_in(name, init):
    return 'Struct: ' + name + ' = ' + init

def struct_out(name, ev):
    return 'Struct: ' + name + ' = ' + ev

def var_in(name, init):
    return 'Variable: ' + name + ' = ' + init

def var_out(name, ev):
    return 'Variable: ' + name + ' = ' + ev
