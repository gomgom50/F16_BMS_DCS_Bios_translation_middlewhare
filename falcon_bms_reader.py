#!/usr/bin/python

# Falcon BMS shared memory reader
# Copyright 2024 Dino Duratović

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import ctypes
import struct
import mmap

class FlightData(ctypes.Structure):
    name = "FalconSharedMemoryArea"
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("xDot", ctypes.c_float),
        ("yDot", ctypes.c_float),
        ("zDot", ctypes.c_float),
        ("alpha", ctypes.c_float),
        ("beta", ctypes.c_float),
        ("gamma", ctypes.c_float),
        ("pitch", ctypes.c_float),
        ("roll", ctypes.c_float),
        ("yaw", ctypes.c_float),
        ("mach", ctypes.c_float),
        ("kias", ctypes.c_float),
        ("vt", ctypes.c_float),
        ("gs", ctypes.c_float),
        ("windOffset", ctypes.c_float),
        ("nozzlePos", ctypes.c_float),
        ("internalFuel", ctypes.c_float),
        ("externalFuel", ctypes.c_float),
        ("fuelFlow", ctypes.c_float),
        ("rpm", ctypes.c_float),
        ("ftit", ctypes.c_float),
        ("gearPos", ctypes.c_float),
        ("speedBrake", ctypes.c_float),
        ("epuFuel", ctypes.c_float),
        ("oilPressure", ctypes.c_float),
        ("lightBits", ctypes.c_uint),
        ("headPitch", ctypes.c_float),
        ("headRoll", ctypes.c_float),
        ("headYaw", ctypes.c_float),
        ("lightBits2", ctypes.c_uint),
        ("lightBits3", ctypes.c_uint),
        ("ChaffCount", ctypes.c_float),
        ("FlareCount", ctypes.c_float),
        ("NoseGearPos", ctypes.c_float),
        ("LeftGearPos", ctypes.c_float),
        ("RightGearPos", ctypes.c_float),
        ("AdiIlsHorPos", ctypes.c_float),
        ("AdiIlsVerPos", ctypes.c_float),
        ("courseState", ctypes.c_int),
        ("headingState", ctypes.c_int),
        ("totalStates", ctypes.c_int),
        ("courseDeviation", ctypes.c_float),
        ("desiredCourse", ctypes.c_float),
        ("distanceToBeacon", ctypes.c_float),
        ("bearingToBeacon", ctypes.c_float),
        ("currentHeading", ctypes.c_float),
        ("desiredHeading", ctypes.c_float),
        ("deviationLimit", ctypes.c_float),
        ("halfDeviationLimit", ctypes.c_float),
        ("localizerCourse", ctypes.c_float),
        ("airbaseX", ctypes.c_float),
        ("airbaseY", ctypes.c_float),
        ("totalValues", ctypes.c_float),
        ("TrimPitch", ctypes.c_float),
        ("TrimRoll", ctypes.c_float),
        ("TrimYaw", ctypes.c_float),
        ("hsiBits", ctypes.c_uint),
        ("DEDLines", (ctypes.c_char * 26) * 5),
        ("Invert", ctypes.c_char * 5 * 26),
        ("PFLLines", ctypes.c_char * 5 * 26),
        ("PFLInvert", ctypes.c_char * 5 * 26),
        ("UFCTChan", ctypes.c_int),
        ("AUXTChan", ctypes.c_int),
        ("RwrObjectCount", ctypes.c_int),
        ("RWRsymbol", ctypes.c_int * 40),
        ("bearing", ctypes.c_float * 40),
        ("missileActivity", ctypes.c_ulong * 40),
        ("missileLaunch", ctypes.c_ulong * 40),
        ("selected", ctypes.c_ulong * 40),
        ("lethality", ctypes.c_float * 40),
        ("newDetection", ctypes.c_ulong * 40),
        ("fwd", ctypes.c_float),
        ("aft", ctypes.c_float),
        ("total", ctypes.c_float),
        ("VersionNum", ctypes.c_int),
        ("headX", ctypes.c_float),
        ("headY", ctypes.c_float),
        ("headZ", ctypes.c_float),
        ("MainPower", ctypes.c_int),
        ]

class FlightData2(ctypes.Structure):
    name = "FalconSharedMemoryArea2"
    _fields_ = [
        ("nozzlePos2", ctypes.c_float),
        ("rpm2", ctypes.c_float),
        ("ftit2", ctypes.c_float),
        ("oilPressure2", ctypes.c_float),
        ("navMode", ctypes.c_byte),
        ("AAUZ", ctypes.c_float),
        ("tacanInfo", ctypes.c_char * 2),
        ("AltCalReading", ctypes.c_int),
        ("altBits", ctypes.c_uint),
        ("powerBits", ctypes.c_uint),
        ("blinkBits", ctypes.c_uint),
        ("cmdsMode", ctypes.c_int),
        ("uhf_panel_preset", ctypes.c_int),
        ("uhf_panel_frequency", ctypes.c_int),
        ("cabinAlt", ctypes.c_float),
        ("hydPressureA", ctypes.c_float),
        ("hydPressureB", ctypes.c_float),
        ("currentTime", ctypes.c_int),
        ("vehicleACD", ctypes.c_short),
        ("VersionNum", ctypes.c_int),
        ("fuelFlow2", ctypes.c_float),
        ("RwrInfo", ctypes.c_char * 512),
        ("lefPos", ctypes.c_float),
        ("tefPos", ctypes.c_float),
        ("vtolPos", ctypes.c_float),
        ("pilotsOnline", ctypes.c_char),
        ("pilotsCallsign", (ctypes.c_char * 12) * 32),
        ("pilotsStatus", ctypes.c_char * 32),
        ("bumpIntensity", ctypes.c_float),
        ("latitude", ctypes.c_float),
        ("longitude", ctypes.c_float),
        ("RTT_size", ctypes.c_ushort * 2),
        ("RTT_area", (ctypes.c_ushort * 7) * 4),
        ("iffBackupMode1Digit1", ctypes.c_char),
        ("iffBackupMode1Digit2", ctypes.c_char),
        ("iffBackupMode3ADigit1", ctypes.c_char),
        ("iffBackupMode3ADigit2", ctypes.c_char),
        ("instrLight", ctypes.c_char),
        ("bettyBits", ctypes.c_uint),
        ("miscBits", ctypes.c_uint),
        ("RALT", ctypes.c_float),
        ("bingoFuel", ctypes.c_float),
        ("caraAlow", ctypes.c_float),
        ("bullseyeX", ctypes.c_float),
        ("bullseyeY", ctypes.c_float),
        ("BMSVersionMajor", ctypes.c_int),
        ("BMSVersionMinor", ctypes.c_int),
        ("BMSVersionMicro", ctypes.c_int),
        ("BMSBuildNumber", ctypes.c_int),
        ("StringAreaSize", ctypes.c_uint),
        ("StringAreaTime", ctypes.c_uint),
        ("DrawingAreaSize", ctypes.c_uint),
        ("turnRate", ctypes.c_float),
        ("floodConsole", ctypes.c_char),
        ("magDeviationSystem", ctypes.c_float),
        ("magDeviationReal", ctypes.c_float),
        ("ecmBits", ctypes.c_uint * 5),
        ("ecmOper", ctypes.c_char),
        ("RWRjammingStatus", ctypes.c_char * 40),
        ("radio2_preset", ctypes.c_int),
        ("radio2_frequency", ctypes.c_int),
        ("iffTransponderActiveCode1", ctypes.c_char),
        ("iffTransponderActiveCode2", ctypes.c_short),
        ("iffTransponderActiveCode3A", ctypes.c_short),
        ("iffTransponderActiveCodeC", ctypes.c_short),
        ("iffTransponderActiveCode4", ctypes.c_short),
        ]

class IntellivibeData(ctypes.Structure):
    name = "FalconIntellivibeSharedMemoryArea"
    _fields_ = [
        ("AAMissileFired", ctypes.c_ubyte),
        ("AGMissileFired", ctypes.c_ubyte),
        ("BombDropped", ctypes.c_ubyte),
        ("FlareDropped", ctypes.c_ubyte),
        ("ChaffDropped", ctypes.c_ubyte),
        ("BulletsFired", ctypes.c_ubyte),
        ("CollisionCounter", ctypes.c_int),
        ("IsFiringGun", ctypes.c_bool),
        ("IsEndFlight", ctypes.c_bool),
        ("IsEjecting", ctypes.c_bool),
        ("In3D", ctypes.c_bool),
        ("IsPaused", ctypes.c_bool),
        ("IsFrozen", ctypes.c_bool),
        ("IsOverG", ctypes.c_bool),
        ("IsOnGround", ctypes.c_bool),
        ("IsExitGame", ctypes.c_bool),
        ("Gforce", ctypes.c_float),
        ("eyex", ctypes.c_float),
        ("eyey", ctypes.c_float),
        ("eyez", ctypes.c_float),
        ("lastdamage", ctypes.c_int),
        ("damageforce", ctypes.c_float),
        ("whendamage", ctypes.c_uint),
        ]

class Strings():
    name = "FalconSharedMemoryAreaString"
    area_size_max = 1024 * 1024
    id = [
        "BmsExe",
        "KeyFile",
        "BmsBasedir",
        "BmsBinDirectory",
        "BmsDataDirectory",
        "BmsUIArtDirectory",
        "BmsUserDirectory",
        "BmsAcmiDirectory",
        "BmsBriefingsDirectory",
        "BmsConfigDirectory",
        "BmsLogsDirectory",
        "BmsPatchDirectory",
        "BmsPictureDirectory",
        "ThrName",
        "ThrCampaigndir",
        "ThrTerraindir",
        "ThrArtdir",
        "ThrMoviedir",
        "ThrUisounddir",
        "ThrObjectdir",
        "Thr3ddatadir",
        "ThrMisctexdir",
        "ThrSounddir",
        "ThrTacrefdir",
        "ThrSplashdir",
        "ThrCockpitdir",
        "ThrSimdatadir",
        "ThrSubtitlesdir",
        "ThrTacrefpicsdir",
        "AcName",
        "AcNCTR",
        "ButtonsFile",
        "CockpitFile",
        "NavPoint",
        "ThrTerrdatadir"
    ]

    def add(self, id, value):
        setattr(self, id, value)

def read_shared_memory(structure):
    try:
        sm = mmap.mmap(-1, ctypes.sizeof(structure), structure.name, access=mmap.ACCESS_READ)
        buffer = sm.read(ctypes.sizeof(structure))
        data = structure.from_buffer_copy(buffer)
        sm.close()
        return data
    except Exception as e:
        print("Error reading shared memory '{}': {}".format(structure.name, e))
        return None

def read_shared_memory_strings():
    try:
        sm = mmap.mmap(-1, Strings.area_size_max, Strings.name, access=mmap.ACCESS_READ)
        version_num = struct.unpack('I', sm.read(4))[0]
        num_strings = struct.unpack('I', sm.read(4))[0]
        data_size = struct.unpack('I', sm.read(4))[0]
        instance = Strings()
        for id in Strings.id:
            str_id = struct.unpack('I', sm.read(4))[0]
            str_length = struct.unpack('I', sm.read(4))[0]
            str_data = sm.read(str_length + 1).decode('utf-8').rstrip('\x00')
            instance.add(id, str_data)
        sm.close()
        return instance
    except Exception as e:
        print("Error reading shared memory '{}': {}".format(Strings.name, e))
        return None

def examples():
    flightdata = read_shared_memory(FlightData)
    flightdata2 = read_shared_memory(FlightData2)
    intellivibe = read_shared_memory(IntellivibeData)
    strings = read_shared_memory_strings()
    print(flightdata.VersionNum)
    print(flightdata2.caraAlow)
    print(intellivibe.In3D)
    print(strings.BmsExe)

if __name__ == "__main__":
    examples()