# minidevice 

## CaptureScreen类
初始化时会判断minicap在该设备是否可用 不可用时则抛出异常
### minicap_screen
使用minicap进行截图
### adb_screen
使用adb截图


## MiniDevice 类
继承CaptureScreen,uiautomator2,pyminitouh
初始化时当minitouch/minicap不可用时则替换为uiautomator2 若uiautomator2仍不可使用，则替换adb方法

### captureScreen
截图方法，返回Mat(opencv)格式图像
详细方法见[CaptureScreen类](#capturescreen类)

### miniPress
按压某点
- `x` 横坐标
- `y`纵坐标
- `duration`(可选) 持续时长 默认150ms 
- `pressure`(可选) 压力 默认100 仅使用minitouch时生效

### miniSwipe
滑动
- `pointArray` 滑动坐标列表 格式为`[(x,y),(x,y),(x,y),(x,y)]`
- `duration`(可选) 持续时长 默认500ms
- `pressure`(可选) 压力 默认100 仅使用minitouch时生效

- `minidevice`
    - `minicap/`
    - `minitouch/`
    - `adb.exe`
    - `__init__.py`
    - `adb.py`
    - `AdbWinApi.dll`
    - `AdbWinUsbApi.dll`
    - `utils.py`
项目结构