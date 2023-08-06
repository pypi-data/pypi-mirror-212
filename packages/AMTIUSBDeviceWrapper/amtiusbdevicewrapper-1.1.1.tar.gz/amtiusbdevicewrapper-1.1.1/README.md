# AMTIUSBDeviceWrapper

## Description

Python wrapper for AMTI USB Device dynamically linked shared library via ctypes module.

## Getting Started

### Dependencies
* Windows 7 64/32-bit and later
* Python V 3.9.13 and later
* AMTI USB Device SDK V 1.3

### Installation
* Place AMTI DLL where convenient
* Recommended install
```
python3 -m pip install amtiusbdevicewrapper
```

### Execution

* Build the package
```
py -m build # Windows
python -m build # Unix
```
* Install the package
```
pip install C:/some-dir/AMTIUSBDeviceWrapper/amtiusbdevicewrapper-<>.whl
```
* Import package
```
from AMTIUSBDeviceWrapper import AMTIUSBDevice as amti
```

## Help

Ensure that you are using a version of python compatible with this package.

## Authors

Jordy Larrea Rodriguez ([CasuallyAlive](https://github.com/CasuallyAlive), jordy.larrearodriguez@gmail.com)

## Version History
* 1.1
    * Supports all basic functionality for interfacing Gen5 signal conditioners
    * Passes all tests
* 1.0
    * Data acquisition is functional
    * Broadcast functions nonspecific to AMTI parameter configuration are functional
    * MISC bug fixes
* 0.2
    * C++ API is closed without issue
    * initialization functions pass tests
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the Creative Commons Zero License.

## Acknowledgments

* [AMTI](https://www.amti.biz/)

## References

* The AMTI USB Device Software Development Kit Reference Manual, v1.3.0, AMTI Force and Motion, March 2017. Accessed: April 09, 2023. Available: [AMTI](https://www.amti.biz/)
