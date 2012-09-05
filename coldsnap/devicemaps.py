"""
"""

import os
import platform

class BaseDeviceMap(dict):
    """
    """

    def __init__(self, *pargs, **kwargs):
        super(LinuxDeviceMap, self).__init__(*pargs, **kwargs)
        self._update_map()
        del self.__setitem__ #make read-only

    def _update_map(self):
        raise NotImplemented()

class LinuxDeviceMap(BaseDeviceMap):
    """
    """

    def _update_map(self):
        with open('/proc/mounts', 'r') as mounts_file:
            mount_lines = [line.strip().split(' ', 3) \
                for line in mounts_file if line.startswith('/dev/')]
        for (device, mount_point, fs_type, __) in mount_lines:
            self[mount_point] = {
                'device': os.path.realpath(device),
                'major_minor': self._get_device_major_minor(mount_point),
                'fs_type': fs_type,
            }

    def _get_device_major_minor(self, mount_point):
        stat = os.stat(mount_point)
        return (int(stat.st_dev >> 8), int(stat.st_int & 0xFF))

class WindowsDeviceMap(BaseDeviceMap):
    """
    """

    pass

class OSXDeviceMap(BaseDeviceMap):
    """
    """

    pass

def get_device_map():
    maps = {
        'Linux':        LinuxDeviceMap,
        'Windows':      WindowsDeviceMap,
        'Darwin':       OSXDeviceMap,
    }
    try:
        map_class = maps.get(platform.system())
    except KeyError as err:
        raise ValueError('Unsupported platform: {0}'.format(err))
    else:
        return map_class()
