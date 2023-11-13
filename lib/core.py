from lib.requester import srequester, requester
from  modules.versionid import versionid
from  modules.files import files
from  modules.userid import users


class core:
    def __init__(self, hostname, ports=[80, 443], verbose=False):
        fast_req = requester(hostname, ports=ports, verbose=verbose)
        fast_req.quick_init()

        self.hostname = hostname
        self.version = versionid(fast_req).version
        self.files = files(fast_req).files
        self.users = users(fast_req).users['usernames']
        self.requester = fast_req

        ## add more as needed for a core initalisation