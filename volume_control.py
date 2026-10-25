import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeController:

    def __init__(self):

        
        device = AudioUtilities.GetSpeakers()

        
        try:
            interface = device.Activate(
                IAudioEndpointVolume._iid_,
                CLSCTX_ALL,
                None
            )
        except AttributeError:
            interface = device._dev.Activate(
                IAudioEndpointVolume._iid_,
                CLSCTX_ALL,
                None
            )

        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        vol_range = self.volume.GetVolumeRange()
        self.minVol = vol_range[0]
        self.maxVol = vol_range[1]

    def set_volume_from_distance(self, distance):

        vol = np.interp(distance, [30, 200], [self.minVol, self.maxVol])
        self.volume.SetMasterVolumeLevel(vol, None)

        vol_percent = np.interp(distance, [30, 200], [0, 100])

        return int(vol_percent)
    