import sys
from cryptography.fernet import Fernet
import json

def helper():
    print("Usage:")
    print("python3 config.py generate_key")
    print("python3 config.py set_secret <secret>")
    print("python3 config.py request_header <true/false> [header_name]")
    sys.exit(1)

with open('config.json', 'r') as f:
    p = json.load(f)
    try:
        if sys.argv[1] == 'generate_key':
            p['key'] = Fernet.generate_key().decode()
            with open('config.json', 'w') as f:
                json.dump(p, f)

        elif sys.argv[1] == 'set_secret':
            p['sign'] = sys.argv[2]
            with open('config.json', 'w') as f:
                json.dump(p, f)

        elif sys.argv[1] == 'request_header':
            if sys.argv[2] == 'true':
                p['ext-req'] = True
                p['ext-hed'] = sys.argv[3]
                with open('config.json', 'w') as f:
                    json.dump(p, f)

            elif sys.argv[2] == 'false':
                p['ext-req'] = False
                with open('config.json', 'w') as f:
                    json.dump(p, f)
                    
            else:
                print("Wrong input. please use true or false")
        else:
            helper()
    except IndexError:
        helper()