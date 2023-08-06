# AMTIUSBDeviceWrapper

## Description

Python wrapper for AMTI USB Device dynamically linked shared library via ctypes module.

## Getting Started

### Dependencies
* Windows 7 64/32-bit and later
* Python V 3.9.13 and later
* AMTI USB Device SDK V 1.3

### Installation

* How/where to download your program
* Any modifications needed to be made to files/folders

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

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Jordy Larrea Rodriguez ([CasuallyAlive](https://github.com/CasuallyAlive), jordy.larrearodriguez@gmail.com)

## Version History

* 0.2
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
