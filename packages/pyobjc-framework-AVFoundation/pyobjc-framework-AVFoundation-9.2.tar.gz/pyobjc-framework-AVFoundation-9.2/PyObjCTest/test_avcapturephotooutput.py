import AVFoundation
from PyObjCTools.TestSupport import TestCase, min_os_level


class TestAVCapturePhotoOutput(TestCase):
    @min_os_level("13.0")
    def test_methods13_0(self):
        self.assertResultIsBOOL(
            AVFoundation.AVCapturePhotoSettings.isHighResolutionPhotoEnabled
        )
        self.assertArgIsBOOL(
            AVFoundation.AVCapturePhotoSettings.setHighResolutionPhotoEnabled_, 0
        )
        self.assertResultIsBOOL(
            AVFoundation.AVCapturePhotoSettings_Tundra.isHighResolutionPhotoEnabled
        )
        self.assertArgIsBOOL(
            AVFoundation.AVCapturePhotoSettings_Tundra.setHighResolutionPhotoEnabled_, 0
        )

        self.assertResultIsBOOL(
            AVFoundation.AVCapturePhotoOutput.preservesLivePhotoCaptureSuspendedOnSessionStop
        )
        self.assertArgIsBOOL(
            AVFoundation.AVCapturePhotoOutput.setPreservesLivePhotoCaptureSuspendedOnSessionStop_,
            0,
        )
        self.assertResultIsBOOL(
            AVFoundation.AVCapturePhotoOutput.preservesLivePhotoCaptureSuspendedOnSessionStop
        )
        self.assertArgIsBOOL(
            AVFoundation.AVCapturePhotoOutput.setPreservesLivePhotoCaptureSuspendedOnSessionStop_,
            0,
        )
