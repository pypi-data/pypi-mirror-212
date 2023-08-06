# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pylibftdi', 'pylibftdi.examples']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylibftdi',
    'version': '0.21.0',
    'description': 'Pythonic interface to FTDI devices using libftdi.',
    'long_description': 'pylibftdi\n=========\n\npylibftdi is a minimal Pythonic interface to FTDI devices using libftdi_.\n\n.. _libftdi: http://www.intra2net.com/en/developer/libftdi/\n\n:Features:\n\n - No dependencies beyond standard library and a `libftdi` install.\n - Supports parallel and serial devices\n - Support for multiple devices\n - File-like interface wherever appropriate\n - Cross-platform\n\n:Limitations:\n\n - The API might change prior to reaching a 1.0 release.\n\nUsage\n-----\n\nThe primary interface is the ``Device`` class in the pylibftdi package; this\ngives serial access on relevant FTDI devices (e.g. the UM232R), providing a\nfile-like interface (read, write).  Baudrate is controlled with the ``baudrate``\nproperty.\n\nIf a Device instance is created with ``mode=\'t\'`` (text mode) then read() and\nwrite() can use the given ``encoding`` (defaulting to latin-1). This allows\neasier integration with passing unicode strings between devices.\n\nMultiple devices are supported by passing the desired device serial number (as\na string) in the ``device_id`` parameter - this is the first parameter in both\nDevice() and BitBangDevice() constructors. Alternatively the device \'description\'\ncan be given, and an attempt will be made to match this if matching by serial\nnumber fails.\n\nExamples\n~~~~~~~~\n\n::\n\n    >>> from pylibftdi import Device\n    >>>\n    >>> with Device(mode=\'t\') as dev:\n    ...     dev.baudrate = 115200\n    ...     dev.write(\'Hello World\')\n\nThe pylibftdi.BitBangDevice wrapper provides access to the parallel IO mode of\noperation through the ``port`` and ``direction`` properties.  These provide an\n8 bit IO port including all the relevant bit operations to make things simple.\n\n::\n\n    >>> from pylibftdi import BitBangDevice\n    >>>\n    >>> with BitBangDevice(\'FTE00P4L\') as bb:\n    ...     bb.direction = 0x0F  # four LSB are output(1), four MSB are input(0)\n    ...     bb.port |= 2         # set bit 1\n    ...     bb.port &= 0xFE      # clear bit 0\n\nThere is support for a number of external devices and protocols, including\ninterfacing with HD44780 LCDs using the 4-bit interface.\n\nHistory & Motivation\n--------------------\nThis package is the result of various bits of work using FTDI\'s\ndevices, primarily for controlling external devices.  Some of this\nis documented on the codedstructure blog, codedstructure.blogspot.com\n\nSeveral other open-source Python FTDI wrappers exist, and each may be\nbest for some projects. Some aim at closely wrapping the libftdi interface,\nothers use FTDI\'s own D2XX driver (ftd2xx_) or talk directly to USB via\nlibusb or similar (such as pyftdi_).\n\n.. _ftd2xx: http://pypi.python.org/pypi/ftd2xx\n.. _pyftdi: https://github.com/eblot/pyftdi\n\nThe aim for pylibftdi is to work with libftdi, but to provide\na high-level Pythonic interface.  Various wrappers and utility\nfunctions are also part of the distribution; following Python\'s\nbatteries included approach, there are various interesting devices\nsupported out-of-the-box - or at least there will be soon!\n\nPlans\n-----\n * Add more examples: SPI devices, knight-rider effects, input devices, MIDI...\n * Perhaps add support for D2XX driver, though the name then becomes a\n   slight liability ;)\n\nLicense\n-------\n\nCopyright (c) 2010-2023 Ben Bass <benbass@codedstructure.net>\n\npylibftdi is released under the MIT licence; see the file "LICENSE.txt"\nfor information.\n\nAll trademarks referenced herein are property of their respective\nholders.\nlibFTDI itself is developed by Intra2net AG.  No association with\nIntra2net is claimed or implied, but I have found their library\nhelpful and had fun with it...\n\n',
    'author': 'Ben Bass',
    'author_email': 'benbass@codedstructure.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codedstructure/pylibftdi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0',
}


setup(**setup_kwargs)
