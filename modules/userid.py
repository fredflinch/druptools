from lxml.html import fromstring

class users:
    def __init__(self, r, range=range(0, 20)):
        self.users = user_bf(r, range)


def user_bf(r, rangev):
    users = {'usernames': [], 'activeid': [], 'potentialid': []}
    for id in rangev:
        u = get_user(r, id)
        if u is not None:
            if u[0] != "":
                users['usernames'].append(u[0])
                users['activeid'].append(u[1])
            else:
                users['potentialid'].append(u[1])
    return users



def get_user(r, id):
    v = r.get('/user/{}'.format(str(id)))
    v_p = fromstring(r.content)
    if v.status_code == 200:
        uname = v_p.findtext('.//title')
        if " |" in uname:
            uname.split(" |")[0]
        return (uname, id)
    if v.status_code == 403:
        return ("", id)
    else:
        return