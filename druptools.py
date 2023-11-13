from modules.tfabrute import tfabrute
from lib.requester import srequester, requester
from lib.core import core
import argparse

# c = core('')
# print("Version Identified: {}".format(c.version))
# print("Files of interest:  {}".format(c.files['200']))

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-u", "--url", help="domain name to scan")
    p.add_argument("--username", help="username when performing authenticated scanning")
    p.add_argument("--password", help="password when performing authenticated scanning")
    p.add_argument("-m", "--mode", help="Scan mode - modes supported:\n- tfabrute\n- users\n- files\n- versionid")
    args = p.parse_args()

    if args.url is None or args.mode is None:
        print("Please provide the required arguments...")
        quit()

    if args.mode == "tfabrute":
        r = srequester(args.url)
        r.quick_init()
        bruter = tfabrute(uname=args.username, passwd=args.password, requestor=r)
        bruter.tfabrute()
     