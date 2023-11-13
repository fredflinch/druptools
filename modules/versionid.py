## Logic for identification taken from drupwn - https://github.com/immunIT/drupwn ##
import re

class versionid:
    def __init__(self, r, fast=False, wordlist='./wordlist/versionid.txt'):
        self.version = identify(r, fast, wordlist)

def identify(r, fast, wordlist):
    vers = []
    v = r.get('/')
    if v.status_code == 200:
        vers.append(header_method(v))
        vers.append(genorator_method(v))
            
    return definative(vers)

def definative(vers):
    vers = list(dict.fromkeys(vers))
    vers = [i for i in vers if i is not None]
    if len(vers)==0: return None
    elif len(vers) == 1: return vers[0]
    else:
        print("[!] Definative version cannot be establised - mulitple versions identified [!]")
        for v in vers:
            print("found version: " + v)

def header_method(resp):
    if 'X-Generator' in resp.headers.keys():
        return resp.headers['X-Generator']
    else: return

def genorator_method(resp):
        gen_rex = re.compile(r'<meta name="(g|G)enerator" content="(?P<gen>[^\"]+)\"')
        basepage = resp.content.decode('utf8')
        gen_tag = gen_rex.search(basepage)
        if gen_tag is not None:
            if "Drupal" in gen_tag.group('gen'):
                return re.search(r'Drupal (?P<ver>[\S]+)', gen_tag.group('gen')).group('ver')
        else: return


#TODO: flesh this to work -- requires examples to be found!
def sensitive_file(r, wordlist):
    with open(wordlist, 'r') as f:
        sensitivef = [l.strip() for l in f.readlines()]
    for fname in sensitivef:
        v = r.get(fname.split(",")[0])
        if v.status_code == 200:
            c = v.content.decode('utf8')
            rex = fname.split(",")[1]
            ## add discovery logic for version - missing atm as files tested dont leak version info
        

