def parse(c_command):
    eq_index = c_command.find('=')
    sc_index = c_command.find(';')
    dest = c_command[:eq_index] if eq_index > 0 else ''
    comp = c_command[eq_index + 1:sc_index] if sc_index > 0 else c_command[eq_index + 1:]
    jump = c_command[sc_index + 1:] if sc_index > 0 else ''
    return dest, comp, jump

def strip_whitespace_and_comments(string):
    return string.strip().split('//')[0].replace(' ', '')
