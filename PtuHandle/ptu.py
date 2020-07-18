from collections import defaultdict
from PtuHandle.minorcheck import check_name, check_setup, check_prefix
from PtuHandle.strstub import stub_get_info, stub_get_calltime
from PtuHandle.strvar import var_get_info, multi_var
from PtuHandle.tostring import               \
                    (                        \
                    stub_in, stub_out,       \
                    array_in, array_out,     \
                    struct_in, struct_out,   \
                    var_in, var_out,         \
                    setup_call               \
                    )

keywords = [
    'VAR',
    'STR',
    'STUB',
    'ARRAY',
    'STRUCT'
]

comments = {
    '----TC_TYPE:': 'TYPE',
    '----TC_VARIANT:': 'VARI',
    '----TC_FUNCTIONALITY:': 'FUNC',
    '----TC_REQUIREMENT_ID:': 'REQI'
}

class TestCase:
    'Test case class'
    def __init__(self, name):
        self.name = name
        self.summary = {'TYPE': 'NA', 'FUNC': 'NA', 'VARI': 'NA', 'REQI': 'NA'}
        self.comments = list()
        self.elements = list()
        self.input, self.output, self.setup = '', '', ''

    def add_info(self, key, content):
        self.summary[key] = content

    def add_comments(self, content):
        self.comments.append(content)

    def add_elements(self, cache):
        self.elements.append(cache)

    def copy_tc(self, tc):
        tc.summary = self.summary
        tc.comments = self.comments
        tc.input = self.input
        tc.output = self.output
        tc.setup = self.setup

    def mapping(self):
        self.table = {
            'Name': self.name,                      \
            'Type': self.summary['TYPE'],           \
            'Variant': self.summary['VARI'],        \
            'Function': self.summary['FUNC'],       \
            'Requirement': self.summary['REQI'],    \
            'Init': self.input,                     \
            'Setup': self.setup,                    \
            'Expected': self.output,                \
            'Comment': '\n'.join(self.comments)     \
        }

    def process(self):
        cond = self.elements[0].multi
        flag = True if cond != [] else False
        if flag is True:
            num_tc = len(cond[0][1])
            tc_list = list()
            self.input = self.elements[0].init
            self.output = self.elements[0].ev
            self.setup = self.elements[0].setup
            for x in range(num_tc):
                tc = TestCase(self.name + '_' + str(x + 1))
                self.copy_tc(tc)
                for y in cond:
                    tc.input += var_in(y[0], y[1][x]) + '\n'
                    tc.output += var_out(y[0], y[2][x]) + '\n'
                tc.mapping()
                tc_list.append(tc)
            del self.elements
            return tc_list
        else:
            num_ele = len(self.elements)
            for i in range(num_ele):
                step = 'Step ' + str(i + 1) + ':\n'
                self.setup += step if num_ele > 1 else ''
                self.input += step if num_ele > 1 else ''
                self.output += step if num_ele > 1 else ''
                self.setup += self.elements[i].setup + '\n' \
                    if self.elements[i].setup != '' else 'No setup'
                self.input += self.elements[i].init + '\n' \
                    if self.elements[i].init != '' else 'No input'
                self.output += self.elements[i].ev + '\n'  \
                    if self.elements[i].ev != '' else 'No output'
            self.mapping()
            del self.elements
            return [self]


class Script:
    'General class'
    def __init__(self, name, services):
        self.name = name.split('.')[0]
        self.services = services

    def self_check(self):
        with open('TestCaseLog.txt', 'w') as f:
            for ser in self.services:
                for tc in self.services[ser]:
                    e1 = check_name(ser, tc.name)
                    e2 = check_setup(ser, tc.setup)
                    e3 = check_prefix(ser, tc.name, 'UT_')
                    if any([e1, e2, e3]):
                        f.write('\n' + tc.name + ':\n')
                        f.write(e1)
                        f.write(e2)
                        f.write(e3)


    def get_content(self, key_list):
        result = list()
        for ser in self.services:
            for tc in self.services[ser]:
                temp = list()
                for key in key_list:
                    multi = [ikey.strip() for ikey in key.split('+')]
                    multi_cont = [tc.table.get(ikey, ikey) for ikey in multi]
                    temp.append('\n'.join(multi_cont))
                result.append(temp)
        return result

class Parse:
    'Parsing PTU syntax'
    def __init__(self, content):
        self.content = content
        self.services = dict()
        self.initialize()

    def initialize(self):
        in_element = False
        for line in self.content:
            statement = line.split(maxsplit=1)
            cmd, param = statement[0].upper(), statement[-1]
            if cmd == 'SERVICE':
                current_service = param
                tcs_list = list()
            elif cmd == 'TEST':
                test_case = TestCase(param)
            elif cmd == 'COMMENT':
                test_case.add_comments(line[7:].strip())
            elif cmd in comments:
                key = comments[cmd]
                test_case.add_info(key, line.split(':', maxsplit=1)[1].strip())
            elif cmd == 'ELEMENT':
                in_element = True
                cache = Cache()
            elif cmd in keywords and in_element:
                cache.input_to_cache(cmd, param)
            elif line.startswith('#') and in_element:
                cache.input_to_cache('SETUP', line[1:])
            elif cmd == 'END':
                end_state = ''.join([cmd, param.upper()])
                if end_state == 'ENDELEMENT':
                    in_element = False
                    cache.process()
                    test_case.add_elements(cache)
                    del cache
                elif end_state == 'ENDTEST':
                    tcs_list += test_case.process()
                    del test_case
                elif end_state == 'ENDSERVICE':
                    self.services[current_service] = tcs_list
                else:
                    continue
            else:
                continue

    def get_services(self):
            return self.services


class Cache:
    def __init__(self):
        self.input = defaultdict(list)
        self.init, self.ev, self.setup = '', '', ''
        self.multi = list()

    def process(self):
        self.__var_handle()
        self.__stub_handle()
        self.__array_handle()
        self.__struct_handle()
        self.__setup_handle()
        del self.input

    def input_to_cache(self, key, content):
        if key == 'STRUCT':
            key = 'STR'
        self.input[key].append(content)

    def __stub_handle(self):
        for stub in self.input['STUB']:
            name, para, ret, time = stub_get_info(stub)
            self.init += stub_in(name, para, ret, time) + '\n'
            self.ev += stub_out(name, para, ret, time) + '\n'

    def __array_handle(self):
        for array in self.input['ARRAY']:
            name, init, ev = var_get_info(array)
            self.init += array_in(name, init) + '\n'
            self.ev += array_out(name, ev) + '\n'

    def __struct_handle(self):
        for struct in self.input['STR']:
            name, init, ev = var_get_info(struct)
            self.init += struct_in(name, init) + '\n'
            self.ev += struct_out(name, ev) + '\n'

    def __var_handle(self):
        for var in self.input['VAR']:
            name, init, ev = var_get_info(var)
            if ('$IN$' in init) or ('$WITH$' in init) or ('$IN$' in ev):
                init, init_len = multi_var(init)
                ev, ev_len = multi_var(ev)
                if init_len < ev_len:
                    init = init * ev_len
                elif init_len > ev_len:
                    ev = ev * init_len
                self.multi.append([name, init, ev])
            else:
                self.init += var_in(name, init) + '\n'
                self.ev += var_out(name, ev) + '\n'

    def __setup_handle(self):
        for setup in self.input['SETUP']:
            func = setup.strip(';').split('=')[-1].strip()
            self.setup += setup_call(func)
