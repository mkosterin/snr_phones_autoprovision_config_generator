# -*- coding: utf-8 -*-
import string
import random
from jinja2 import Template, Environment, FileSystemLoader


def password():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(random.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


baseDir = "c:\\provision"
# which extension number we should start
start_ext = 821

extensionHeader = """#cid_number,transfer,mailbox,type,qualify,hasdirectory,call-limit,host,context,fullname,secret,hasvoicemail,vmsecret,email,delete,hassip,hasiax,dahdichan,hasmanager,nat,dtmfmode,hasagent,callwaiting,videosupport,transport,encryption,srtpcapable,disallow,allow,deny,permit,callgroup,pickupgroup"""
extensionFileName = baseDir + "\\" + "users_extensions.csv"

env = Environment(loader=FileSystemLoader(baseDir))

mac = open(baseDir + "\\" + "macs.txt")
extensionFile = open(extensionFileName, "w")
extensionFile.write(extensionHeader)

templateExtension = env.get_template("templ_extensions.csv.j2")
templateMac = env.get_template("templ.cfg.j2")

ext = start_ext
for line in mac:
    data = {
        "enable": "1",
        "label": ext,
        "displayname": ext,
        "sipUsername": ext,
        "authname": ext,
        "sipPassword": password(),
        "server": "192.168.1.1",  #change it as you want
        "webUser": "admin",       #change it as you want
        "webPassword": "admin"    #change it as you want
    }
    extensionFile.write("\n" + templateExtension.render(**data))
    autopFile = open(baseDir + "\\" + line[0:-1] + ".cfg", "w")
    autopFile.write(templateMac.render(**data) + "\n")
    autopFile.close()
    ext = ext + 1



mac.close()
extensionFile.close()


