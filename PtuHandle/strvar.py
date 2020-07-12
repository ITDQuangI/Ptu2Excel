def var_get_info(str_in):
    var_name = str_in.split(',', maxsplit=1)[0].strip()
    repl_str = str_in.replace(var_name, '', 1).replace(',', '', 1).strip()
    repl_str = replace_in_bracket(repl_str, '{', '}', ',')
    var_init = repl_str.split(',', maxsplit=1)[0].strip()
    var_ev = repl_str.replace(var_init, '', 1).replace(',', '', 1).strip()
    if '=' in var_init:
        var_init = var_init.split('=', maxsplit=1)[1].strip()
    if '=' in var_ev:
        var_ev = var_ev.split('=', maxsplit=1)[1].strip()
    if 'INIT' in var_ev.upper():
        var_ev = check_keyword(var_ev, 'INIT').replace('$INIT$', var_init)
    var_init = check_keyword(var_init, 'IN')
    var_init = check_keyword(var_init, 'WITH')
    var_ev = check_keyword(var_ev, 'IN')
    return var_name, \
           replace_in_bracket(var_init, '{', '}', ',', False), \
           replace_in_bracket(var_ev, '{', '}', ',', False)

def replace_in_bracket(str_in, left, right, replace, forward=True):
    count, new_str = 0, ''
    for index in range(len(str_in)):
        if str_in[index] == left:
            count += 1
        elif str_in[index] == right:
            count -= 1
        if forward is True:
            new_str += '$' if str_in[index] == replace and count != 0   \
            else str_in[index]
        else:
            new_str += replace if str_in[index] == '$' and count != 0   \
            else str_in[index]
    return new_str

def check_keyword(string, keyword):
    upper_str = string.upper()
    like_keyword_pos, keyword_pos, str_out = list(), list(), list(string)
    index, increas = upper_str.find(keyword), 0
    while(index != -1):
        like_keyword_pos.append(index)
        index = upper_str.find(keyword, index + 1)
    for i in like_keyword_pos:
        is_keyword = True
        for diff in (-1, len(keyword)):
            if (i + diff) < 0 or (i + diff) == len(string):
                continue
            if (string[i + diff] <= 'Z' and string[i + diff] >= 'A') \
            or (string[i + diff] <= 'z' and string[i + diff] >= 'a') \
            or (string[i + diff] <= '9' and string[i + diff] >= '0') \
            or string[i + diff] == '_':
                is_keyword = False;
        if is_keyword is True:
            keyword_pos.append(i)
        else:
            continue
    for i in keyword_pos:
        start, end = i + increas, i + len(keyword) + increas + 2
        str_out.insert(start, '$')
        str_out.insert(end - 1, '$')
        str_out[start:end] = list(map(str.upper, str_out[start:end]))
        increas += 2
    return ''.join(str_out)

def multi_var(str_in):
    if '{' not in str_in:
        val = list(str_in)
    else:
        val = str_in.split('{')[1][:-1].strip()
        val = [i.strip() for i in val.split(',')]
    val_len = len(val)
    return val, val_len
