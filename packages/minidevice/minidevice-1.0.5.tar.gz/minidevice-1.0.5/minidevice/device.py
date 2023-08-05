from .utils import raw2opencv
from .adb import get_sdk, get_vmsize, adb_screen, get_abi, adb_press, adb_silde
from .minicap import minicap_screen, minicap_available, minicap_install
from .minitouch import minitouch_install
from pyminitouch import MNTDevice
from uiautomator2 import Device


class CaputreScreen():
    def __init__(self, device) -> None:
        self.device = device
        self.abi = get_abi(device)
        self.sdk = get_sdk(device)
        self.vmszie = get_vmsize(device)
        if not minicap_available(device, self.vmszie):
            try:
                minicap_install(device, self.sdk, self.abi)
            except:
                print("minicap isn't available")

    def adb_screen(self):
        return raw2opencv(adb_screen(self.device))

    def minicap_screen(self):
        return raw2opencv(minicap_screen(self.device, self.sdk, self.vmszie))


class MiniDevice(MNTDevice, CaputreScreen, Device):
    def __init__(self, device):
        try:
            CaputreScreen.__init__(self, device)
            minitouch_install(device, get_abi(device))
            MNTDevice.__init__(self, device)
            self.method = "MiniDevice"
            print("use MiniDevice")
        except AssertionError:
            print("please reboot your device!")
            exit()
        except:
            try:
                Device.__init__(self, device)
                self.method = "uiautomator"
                print("use uiautomator")
            except:
                self.method = "adb"
                print("use adb")

    def miniPress(self, x, y, duration=150, pressure=100):
        if self.method == "MiniDevice":
            self.tap([(x, y)],duration,pressure)
        elif self.method == "uiautomator":
            self.long_click(x, y, duration/1000)
        elif self.method == "adb":
            adb_press(self.device, x, y, duration)

    def miniSwipe(self, pointArray, duration=500, pressure=100):
        if self.method == "MiniDevice":
            self.swipe(pointArray, duration, pressure)
        elif self.method == "uiautomator":
            self.swipe_points(pointArray, duration/1000)
        elif self.method == "adb":
            adb_silde(self.device, pointArray, duration)

    def captureScreen(self):
        if self.method == "MiniDevice":
            return self.minicap_screen()
        elif self.method == "uiautomator":
            return self.screenshot(format="opencv")
        elif self.method == "adb":
            return self.adb_screen()


if __name__ == "__main__":
    import cv2
    g = MiniDevice("127.0.0.1:5555")
    cv2.imshow("", g.captureScreen())
    cv2.waitKey()
    g.stop()
