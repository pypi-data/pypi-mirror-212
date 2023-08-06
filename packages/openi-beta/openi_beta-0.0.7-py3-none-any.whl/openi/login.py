import os
import re
from getpass import getpass
from .constants import (
    TOKEN_PATH,
    TOKEN_PATTERN
)

def login(force: bool = False) -> None:
    print("""     
     ██████╗   ██████╗  ███████╗  ███╗   ██╗  ██████╗
    ██╔═══██╗  ██╔══██╗ ██╔════╝  ████╗  ██║    ██╔═╝
    ██║   ██║  ██████╔╝ █████╗    ██╔██╗ ██║    ██║
    ██║   ██║  ██╔═══╝  ██╔══╝    ██║╚██╗██║    ██║
    ╚██████╔╝  ██║      ███████╗  ██║ ╚████║  ██████╗
     ╚═════╝   ╚═╝      ╚══════╝  ╚═╝  ╚═══╝  ╚═════╝                                                                        
    """)

    print("  To use this package, `OPENI` requires an access token generated from https://openi.pcl.ac.cn/user/settings/applications \n")

    if check_token():
        if force:
            print("  [WARNING] A token already exists in this project, enter a new token will overwrite the existing one. \n "
                "           you can press 'ctrl+c' to cancel login. \n")
        else:
            print("  A valid token was found in this project, login successfully!\n"
                  "  use `login(force=True)` to enter a new token.\n")
            return

    token = getpass(prompt="Access Token: ") # 82118d7b5dc63c5599872d9b6cc260ad37abfb63 #aaaa8d7b5dc63c5599872d9b6cc260ad37abfb63
    save_token(token)
    print("\n  Login successfully!\n"
          f"  Your token has been saved to {TOKEN_PATH} \n")

def check_token() -> bool:
    """
    check if token path exists and token is valid
    """
    if os.path.exists(TOKEN_PATH):
        with open(file=TOKEN_PATH, mode='r') as f:
            _token = f.read()
        return re.match(TOKEN_PATTERN, _token)
    else:
        return False

def save_token(token: str) -> None:
    """
    simple validation and save token
    """
    if re.match(TOKEN_PATTERN, token):
        with open(file=TOKEN_PATH, mode='w') as f:
            f.write(token)
    else:
        raise ValueError("Invalid token passed!")

def get_token() -> str:
    msg = f"❌Unauthorized, please login with token first! see example below: \n    from openi import login\n    login()\n"
    if os.path.exists(TOKEN_PATH):
        with open(file=TOKEN_PATH, mode='r') as f:
            _token = f.read()
        return _token
    else:
        raise KeyError(msg)