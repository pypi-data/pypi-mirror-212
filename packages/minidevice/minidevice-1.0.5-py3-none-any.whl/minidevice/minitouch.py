import subprocess

from .config import ADB_PATH,MINITOUCH_PATH

def minitouch_install(device, abi):
    """minitouch

    Args:
        device (_type_): _description_
    """

    MNT_HOME = "/data/local/tmp/minitouch"

    subprocess.run([
        ADB_PATH, "-s", device, "push",
        F"{MINITOUCH_PATH}/{abi}/minitouch",
        MNT_HOME],
        stdout=subprocess.DEVNULL)

    subprocess.run([ADB_PATH, "-s", device, "shell", "chmod", "777", MNT_HOME])

