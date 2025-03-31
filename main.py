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
                "funcs" : [
                    {
                        "name" : "Namelog",
                        "func" : namelog,
                        "args" : ["First Name", "Last Name"],
                        "report_key" : "NAME"
                    }
                ]
            },
            {
                "name" : "Bank",
                "arg" : "Bin",
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
                        "args" : ["Ip", "Port"],
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
                "name" : "Online",
                "arg" : "Url",
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
        self.report = {}

    def setup(self):
        info_config = {}
        for mod in self.modules:
            self.report[mod["name"]] = {}
            print("[ {}".format(mod["name"]))
            info_config[mod["name"]] = {}
            info_config[mod["name"]]["funcs"] = []
            for func in mod["funcs"]:
                info_config[mod["name"]]["funcs"].append({
                    "name" : func["name"],
                    "func" : func["func"],
                    "mod"  : mod["name"],
                    "args" : []
                })
                print("| ARGS FOR {}".format(func["name"]))
                for arg in func["args"]:
                    input_arg = input(f"[ {arg} : ")
                    if input_arg:
                        info_config[mod["name"]]["funcs"][-1]["args"].append(input_arg)
        return info_config
    
    def run(self, info_config):
        for mod in info_config:
            module_data = info_config[mod]
            for func in module_data["funcs"]:
                if func["args"] == []:
                    print("Skipping {}".format(func["name"]))
                    continue
                print("Running {}".format(func["name"]))
                func_name = func["name"]
                args      = func["args"]
                func_func = func["func"]
                self.report[mod][func_name] = func_func(self, self.session, *args)

    def main(self):
        data = self.setup()
        self.run(data)

        print(self.report)
        create(self.report)
        show(self.report)
        with open("report.json", "w") as f:
            f.write(json.dumps(self.report, indent=4))

if __name__ == "__main__":
    main = Main()
    main.main()