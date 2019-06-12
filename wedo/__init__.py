from functools import wraps

from wedo.distance import interpolate_distance_data
from wedo.motor import processMotorValues
from wedo.tilt import process_tilt
from wedo.tilt import FLAT, TILT_BACK, TILT_FORWARD, TILT_LEFT, TILT_RIGHT

import os
import hid

ID_VENDOR = 0x0694
ID_PRODUCT = 0x0003
WEDO_INTERFACE = 0
WEDO_CONFIGURATION = 1

UNAVAILABLE = 0
TILTSENSOR = (38, 39, 40)
DISTANCESENSOR = (176, 177, 178, 179, 180)
MOTOR = (0, 1, 2, 3, 99, 100, 101, 102, 203, 204, 238, 239, 240)

# limit the visibility to simplify the usage
__all__ = ["scan_for_devices", "WeDo", "FLAT",
    "TILT_BACK", "TILT_FORWARD", "TILT_LEFT", "TILT_RIGHT"]

class WeDo(object):
    """
        Each instance of this class represents a physical WeDo device.

        Usage :

        >>> from wedo import WeDo
        >>> wd = WeDo()

        Activating the first motor full forward:
        >>> wd.motor_a = 100

        Activating the second motor half speed/force backward:
        >>> wd.motor_b = -50

        Current value of the tilt sensor:
        >>> wd.tilt

        Current distance value in meters of the distance sensor:
        >>> wd.distance
    """

    def __init__(self, device=None):
        """
        If a device is not given, it will attach this instance to the first one found.
        Otherwise you can pass a specific one from the list returned by scan_for_devices.
        """
        self.number = 0
        self.dev = device
        if self.dev is None:
            self.dev = hid.device()
            self.dev.open(ID_VENDOR, ID_PRODUCT)
            self.dev.set_nonblocking(1)
        self.valMotorA = 0
        self.valMotorB = 0

    def getRawData(self):
        """Read 64 bytes from the WeDo's endpoint, but only
        return the last eight."""
        try:
            self.dev.write([0x0, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            return self.dev.read(64)
        except:
            print "Could not read from WeDo device"
        return None

    def setMotors(self):
        """
        Arguments should be in form of a number between 0
        and 100, positive or negative. Magic numbers used for
        the ctrl_transfer derived from sniffing USB coms.
        """
        data = [0x0, 0x40,
                    processMotorValues(self.valMotorA) & 0xFF,
                    processMotorValues(self.valMotorB) & 0xFF,
                    0x00, 0x00, 0x00, 0x00, 0x00]
        try:
            self.dev.write(data)
        except:
            print "Could not write to driver"

    def getData(self):
        """
        Sensor data is contained in the 2nd and 4th byte, with
        sensor IDs being contained in the 3rd and 5th byte
        respectively.
        """
        rawData = self.getRawData()
        if rawData is not None:
            sensorData = {rawData[3]: rawData[2], rawData[5]: rawData[4]}
        else:
            sensorData = {}
        return sensorData

    @property
    def raw_tilt(self):
        """
        Returns the raw tilt direction (arbitrary units)
        """
        data = self.getData()
        for num in data:
            if num in TILTSENSOR:
                return data[num]
        return UNAVAILABLE

    @property
    def tilt(self):
        """
        Returns the tilt direction (one of the FLAT, TILT_FORWARD, TILT_LEFT, TILT_RIGHT, TILT_BACK constants)
        """
        raw_data = self.raw_tilt
        if raw_data is UNAVAILABLE:
            return UNAVAILABLE
        return process_tilt(raw_data)

    @property
    def raw_distance(self):
        """
        Return the raw evaluated distance from the distance meter (arbitrary units)
        """
        data = self.getData()
        for num in data:
            if num in DISTANCESENSOR:
                return data[num]
        return UNAVAILABLE

    @property
    def distance(self):
        """
        Return the evaluated distance in meters from the distance meter.
        (Note: this is the ideal distance without any objets on the side, you might have to adapt it depending on your construction)
        """

        raw_data = self.raw_distance
        if raw_data is UNAVAILABLE:
            return UNAVAILABLE
        return interpolate_distance_data(raw_data)

    @property
    def motor_a(self):
        """ Get back the last speed/force set for motor A
        """
        return self.valMotorA

    @property
    def motor_b(self):
        """ Get back the last speed/force set for motor A
        """
        return self.valMotorB

    @motor_a.setter
    def motor_a(self, value):
        """ Sets the speed/force of the motor A, expects a value between -100 and 100
        """
        if value > 100 or value < -100:
            print "A motor can only be between -100 and 100"
        self.valMotorA = value
        self.setMotors()

    @motor_b.setter
    def motor_b(self, value):
        """ Sets the speed/force of the motor B, expects a value between -100 and 100
        """
        if value > 100 or value < -100:
            print "A motor can only be between -100 and 100"
        self.valMotorB = value
        self.setMotors()

