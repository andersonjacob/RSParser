import re

class person(object):
    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.address_1 = ''
        self.address_2 = ''
        self.city = ''
        self.state = ''
        self.zip = ''
        self.phone = ''
        self.email = ''
        self.birthday = None
        
    def __str__(self):
        ret = 'name: {}, {}'.format(self.last_name, self.first_name)
        ret += '\naddress: {}'.format(self.address_1)
        if len(self.address_2) > 0:
            ret += '\n         {}'.format(self.address_2)
        ret += '\n         {}, {} {}'.format(self.city, self.state, self.zip)
        if len(self.phone) > 0:
            ret += '\nphone: {}'.format(self.phone)
        if len(self.email) > 0:
            ret += '\nemail: {}'.format(self.email)
        if self.birthday:
            ret += '\birthday: {}'.format(self.birthday)
        return ret
            
    def to_dict(self):
        comb_address = self.address_1
        if len(self.address_2) > 0:
            comb_address += ' ' + self.address_2
        return {'first': self.first_name, 'last': self.last_name,
                'address': comb_address, 'phone': self.phone,
                'city': self.city, 'state': self.state, 'zip_code': self.zip,
                'email': self.email, 'birthday': self.birthday}

            
def parse_name_line(l):
    match = re.search(r'([\w\' ]+), ([\w\' ]+)', l)
    if match:
        return match.group(2,1)
    return None, None

def parse_city_state_zip(l, testStates = ['colorado']):
    split_line = l.split(',', maxsplit=1)
    if len(split_line) < 2:
        return None, None, None
    city = split_line[0].rstrip().lstrip()
    split_line = split_line[1].split()
    maybeZip = split_line[-1]
    zip_code = re.match(r'([0-9]{5})((-[0-9]{4})|())', maybeZip)
    if zip_code:
        zip_code = zip_code.group(0)
        state = ' '.join(split_line[:-1])
        return city, state, zip_code
    elif ' '.join(split_line).lower() in testStates:
        return city, ' '.join(split_line), None
    return None, None, None
    
def parse_phone_number(l):
    m = re.search(r'([(]*)([0-9]{3})([)-\. ]*)([0-9]{3})([-\. ]*)([0-9]{4})',
                  l)
    if m:
        return '-'.join(m.group(2,4,6))
    m = re.fullmatch(r'([0-9]{3})([-\. ]*)([0-9]{4})', l)
    if m:
        return '-'.join(m.group(1,3))
    return None
    
def parse_email(l):
    at_loc = l.find('@')
    if at_loc > 0:
        if l.find('.', at_loc) > 0:
            return l
    return None

def parse_text_file(fname):
    peopleList = []
    with open(fname) as f:
        has_name = False
        has_address = False
        has_city_state_zip = False
        has_phone = False
        has_email = False
        p = None
        for l in f:
            l = l.rstrip()
            blankLine = (len(l) < 1)
            if blankLine:
                has_name = False
                continue
            titleLine = re.match(r'\s+', l)
            if titleLine:
                has_name = False
                continue
            headerLine = (len(l) == 1)
            headerLine = headerLine and re.match(r'[A-Z]', l)
            if headerLine:
                # print(l)
                has_name = False
                continue
            first, last = parse_name_line(l)
            city, state, zip_code = parse_city_state_zip(l)
            phone_number = parse_phone_number(l)
            email = parse_email(l)
            if (not has_name and (first or last)) or \
               (has_city_state_zip and (first or last) and state is None):
                p = person()
                p.first_name = first
                p.last_name = last
                has_name = True
                has_address = False
                has_city_state_zip = False
                has_phone = False
                has_email = False
                peopleList.append(p)
                continue
            if not has_email and email is not None:
                p.email = email
                has_email = True
                continue
            if not has_phone and phone_number is not None:
                p.phone = phone_number
                has_phone = True
                continue
            if not has_city_state_zip and state is not None:
                p.city = city
                p.state = state
                p.zip = zip_code
                has_city_state_zip = True
                continue
            if p and not has_address and len(p.address_1) < 1:
                p.address_1 = l
                has_address = True
                continue
            elif p and len(p.address_2) < 1 and not has_phone and \
              not has_email and not has_city_state_zip:
                p.address_2 = l
                has_address = True
                continue
            print('current person:')
            print(p)
            print('unclassifialb line: {}'.format(l))
            print('has_name: {}, first: {}, last: {}, \ncity: {}, state: {}, zip_code: {}, \nphone: {}, email: {}\n'.format(
                has_name, first, last, city, state, zip_code,
                phone_number, email))
                
    return peopleList
    
if __name__ == '__main__':
    import os.path
    import argparse
    parser = argparse.ArgumentParser(description='parsing text file from pdf')
    parser.add_argument('textfile', metavar='file', nargs=1,
                        help='the file to be parsed')
    args = parser.parse_args()
    print(args.textfile)

    import pandas as pd

    plist = parse_text_file(os.path.normpath(args.textfile.pop()))
    

    df = pd.DataFrame((person.to_dict() for person in plist),
                      columns=['last','first','address','city','state',
                               'zip_code','phone','email','birthday'])
    df.to_csv('rssisters.csv', index=False)
    # print(df)
    
