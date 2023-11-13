class files:
    def __init__(self, r, wordlist='./wordlists/interesting.txt'):
        self.wordlist = wordlist
        self.files = test_files(r, wordlist)

def test_files(r, wordlist):
    ifiles = {'200': [], '403': [], '404': []}
    with open(wordlist, 'r') as f:
        interestingf = [l.strip() for l in f.readlines()]
    for fname in interestingf:
        try: 
            v = r.get("/"+fname)
            if str(v.status_code) in ifiles.keys():
                ifiles[str(v.status_code)].append(fname)
        except: 
            continue
    return ifiles

