import requests as req

class requester:
    default_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53, 7.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    def __init__(self, hostname, creds=None, headers=default_headers, verbose=False, ports = [80, 443], primary = 'https'):
        self.hostname = hostname
        self.creds = creds
        self.headers = headers
        self.verbose = verbose
        self.ports = ports
        self.protocols = {'https': [], 'http': []}
        self.urls = []
        self.primary = primary

    def quick_init(self):
        if 443 in self.ports: 
            self.protocols['https'].append("https://"+self.hostname)
            self.urls.append("https://"+self.hostname)
        elif 80 in self.ports:
            self.protocols['http'].append("http://"+self.hostname)
            self.urls.append("http://"+self.hostname)
        else:
            self.protocol_test(self)

    ## Protocol tester to identify all protocols in use for the given host (http/https) ##
    # notes: relys on internal gets and error handling for identificaiton - fall backs to pre-TLS checks likely more robust
    def protocol_test(self):
        for u in self.ports:
            url = "https://{host}:{port}".format(host=self.hostname, port=u)
            try: 
                req.get(url, headers=self.headers)
                self.protocols['https'].append(url) 
                self.urls.append(url)
            except req.exceptions.SSLError:
                try:
                    url = url.replace("https://", "http://")
                    ## TODO: address logic here - many status codes could be utilised to inicate http in use - address to a redirect case : OKAY for now though
                    if req.get(url, headers=self.headers).status_code == 200:
                        self.protocols['http'].append(url)
                        self.urls.append(url)
                except:
                    raise Exception("error w url -- protocol likely not HTTP or Network down")
            except: 
                raise Exception("error w url")
        
        if self.verbose and len(self.protocols['http']) > 0:
            print("[*] HTTP in use [*]")
            
        return
        

    def get(self, path, additional_headers={}, mode='single'):
        headers = {**self.headers, **additional_headers}
        if mode=='single':
            url = ""
            if len(self.protocols[self.primary]) > 0: url = self.protocols[self.primary][0]
            elif len(self.urls) > 0: url = self.urls[0]
            else: raise Exception("error in get URLs do not exist")
            r = req.get(url+path, headers=headers)
            return r
        elif mode=='multi':
            ret = []
            for u in self.urls:
                r = req.get(u+path, headers=headers)
                ret += r
            return ret
        else:
            raise Exception("unsupported mode in get") 

    def post(self, path, data, additional_headers={}, mode='single', rtype='utf8'):
        headers = {**self.headers, **additional_headers}
        if mode == 'single':
            url = ""
            if len(self.protocols[self.primary]) > 0: url = self.protocols[self.primary][0]
            elif len(self.urls) > 0: url = self.urls[0]
            else: raise Exception("error in get URLs do not exist")
            r = req.post(url+path, data=data, headers=headers)
            return r
        elif mode=='multi':
            ret = []
            for u in self.urls:
                r = req.post(u+path, data=data, headers=headers)
                ret += r

            return ret
        else:
            raise Exception("unsupported mode in get")
                
class srequester:
    default_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53, 7.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    def __init__(self, hostname, creds=None, headers=default_headers, verbose=False, ports = [80, 443], primary = 'https'):
        self.hostname = hostname
        self.session = req.Session()
        self.creds = creds
        self.headers = headers
        self.verbose = verbose
        self.ports = ports
        self.protocols = {'https': [], 'http': []}
        self.urls = []
        self.primary = primary

    def quick_init(self):
        if 443 in self.ports: 
            self.protocols['https'].append("https://"+self.hostname)
            self.urls.append("https://"+self.hostname)
        elif 80 in self.ports:
            self.protocols['http'].append("http://"+self.hostname)
            self.urls.append("http://"+self.hostname)
        else:
            self.protocol_test(self)
    
    ## Protocol tester to identify all protocols in use for the given host (http/https) ##
    # notes: relys on internal gets and error handling for identificaiton - fall backs to pre-TLS checks likely more robust
    def protocol_test(self):
        for u in self.ports:
            url = "https://{host}:{port}".format(host=self.hostname, port=u)
            try: 
                req.get(url, headers=self.headers)
                self.protocols['https'].append(url) 
                self.urls.append(url)
            except req.exceptions.SSLError:
                try:
                    url = url.replace("https://", "http://")
                    ## TODO: address logic here - many status codes could be utilised to inicate http in use - address to a redirect case : OKAY for now though
                    if req.get(url, headers=self.headers).status_code == 200:
                        self.protocols['http'].append(url)
                        self.urls.append(url)
                except:
                    raise Exception("error w url -- protocol likely not HTTP or Network down")
            except: 
                raise Exception("error w url")
        
        if self.verbose and len(self.protocols['http']) > 0:
            print("[*] HTTP in use [*]")
            
        return
        

    def get(self, path, additional_headers={}, mode='single'):
        headers = {**self.headers, **additional_headers}
        if mode=='single':
            url = ""
            if len(self.protocols[self.primary]) > 0: url = self.protocols[self.primary][0]
            elif len(self.urls) > 0: url = self.urls[0]
            else: raise Exception("error in get URLs do not exist")
            r = self.session.get(url+path, headers=headers)
            return r
        elif mode=='multi':
            ret = []
            for u in self.urls:
                r = self.session.get(u+path, headers=headers)
                ret += r
            return ret
        else:
            raise Exception("unsupported mode in get") 

    def post(self, path, data, additional_headers={}, mode='single', rtype='utf8'):
        headers = {**self.headers, **additional_headers}
        if mode == 'single':
            url = ""
            if len(self.protocols[self.primary]) > 0: url = self.protocols[self.primary][0]
            elif len(self.urls) > 0: url = self.urls[0]
            else: raise Exception("error in get URLs do not exist")
            r = self.session.post(url+path, data=data, headers=headers)
            return r
        elif mode=='multi':
            ret = []
            for u in self.urls:
                r = self.session.post(u+path, data=data, headers=headers)
                ret += r

            return ret
        else:
            raise Exception("unsupported mode in get")