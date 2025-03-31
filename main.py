import json, tls_client
from core.modules.report.create import create
from core.modules.report.format import show

# Bank
from core.modules.bank.bincheck import bincheck

# Email

from core.modules.email.intelx import intelx
from core.modules.email.getgmailpfp import emailpfp
from core.modules.email.protonmail import protonmail

# Identity

from core.modules.identity.namelog import namelog

# IP
from core.modules.ip.lookup import lookup
from core.modules.ip.getbanner import get_banner
from core.modules.ip.known_vpn import known_vpn
from core.modules.ip.portscan import portscan

# Location
from core.modules.location.addresslog import addresslog

# Online
from core.modules.online.username import username_lookup

# Phone

from core.modules.phone.basic import phone_basic
from core.modules.phone.codeinfo import codeinfo



class Main:
    def __init__(self):
        self.session = tls_client.Session()
        self.modules = [
            {
                "name" : "Identity",
                "arg" : "Identity",
                "format" : "(first_name) (last_name)",
                "funcs" : [
                    {
                        "name" : "Namelog",
                        "func" : namelog,
                        "args" : ["Name"],
                        "report_key" : "NAME"
                    }
                ]
            },
            {
                "name" : "Bank",
                "arg" : "Bin",
                "format" : "xxxxxxxx",
                "funcs" : [
                    {
                        "name" : "Bincheck",
                        "func" : bincheck,
                        "args" : ["Bin"],
                        "report_key" : "BIN_RESULT"
                    }
                ]
            },
            {
                "name" : "Email",
                "arg" : "Email",
                "format" : "something@provider.tld",
                "funcs" : [
                    {
                        "name" : "Intelx",
                        "func" : intelx,
                        "args" : ["Email"],
                        "report_key" : "EMAIL_RESULT"
                    },
                    {
                        "name" : "Email PFP",
                        "func" : emailpfp,
                        "args" : ["Email"],
                        "report_key" : "EMAIL_PFP_RESULT"
                    },
                    {
                        "name" : "Protonmail",
                        "func" : protonmail,
                        "args" : ["Email"],
                        "report_key" : "PROTONMAIL_RESULT"
                    }
                ]
            },

            {
                "name" : "IP",
                "arg" : "Ip",
                "format" : "x.x.x.x",
                "funcs" : [
                    {
                        "name" : "Lookup",
                        "func" : lookup,
                        "args" : ["Ip"],
                        "report_key" : "IP_LOOKUP_RESULT"
                    },
                    {
                        "name" : "Banner",
                        "func" : get_banner,
                        "args" : ["Ip", 22],
                        "report_key" : "IP_BANNER_RESULT"
                    },
                    {
                        "name" : "Known VPN",
                        "func" : known_vpn,
                        "args" : ["Ip"],
                        "report_key" : "KNOWN_VPN_RESULT"
                    },
                    {
                        "name" : "Portscan",
                        "func" : portscan,
                        "args" : ["Ip"],
                        "report_key" : "PORTSCAN_RESULT"
                    }
                ]
            },
            {
                "name" : "Location",
                "arg" : "Address",
                "format" : "(house number), (street), (city), (state/county), (country), (postal code)",
                "funcs" : [
                    {
                        "name" : "Addresslog",
                        "func" : addresslog,
                        "args" : ["Address"],
                        "report_key" : "ADDRESSLOG_RESULT"
                    }
                ]
            },
            {
                "name" : "Online",
                "arg" : "Url",
                "format" : "username",
                "funcs" : [
                    {
                        "name" : "Username",
                        "func" : username_lookup,
                        "args" : ["Username"],
                        "report_key" : "ONLINE_USERNAME_RESULT"
                    }
                ]
            },
            {
                "name" : "Phone",
                "arg" : "Phone",
                "format" : "+xx-xxxxxxxxxxx",
                "funcs" : [
                    {
                        "name" : "Basic",
                        "func" : phone_basic,
                        "args" : ["Phone"],
                        "report_key" : "PHONE_BASIC_RESULT"
                    },
                    {
                        "name" : "Codeinfo",
                        "func" : codeinfo,
                        "args" : ["Phone"],
                        "report_key" : "PHONE_CODEINFO_RESULT"
                    }
                ]
            }
        ]
        self.report = {
            "Identity" : {},
            "Bank" : {},
            "Email" : {},
            "IP" : {},
            "Location" : {},
            "Online" : {},
            "Phone" : {}
        }

    def setup(self):
        info_config = {}
        print("If you do not know the data for a module, leave it blank. If the module has multiple sections then put N/A.")
        for mod in self.modules:
            name = mod["name"]
            sections = " | ".join([f"[{func['name']}]" for func in mod["funcs"]])
            print("Data for: {}".format(sections))
            print("Format: <{}>".format(mod["format"]))
            data = input(name + " : ")
            if data:
                info_config[name] = {"data" : data, "section" : name}
        return info_config
    
    def run(self, info_config):
        for mod in info_config:
            for modules in self.modules:
                if modules["name"] == mod:
                    for func in modules["funcs"]:
                        print("Running {} for {}...".format(func["name"], mod))
                        try:
                            self.report[mod][func["name"]] = func["func"](self, self.session, info_config[mod]["data"])
                        except Exception as e:
                            print(e)

    def main(self):
        data = self.setup()
        self.run(data)

        with open("report.json", "w") as f:
            f.write(json.dumps(self.report, indent=4))
        create(self.report)
        show(self.report)

if __name__ == "__main__":
    main = Main()
    main.main()