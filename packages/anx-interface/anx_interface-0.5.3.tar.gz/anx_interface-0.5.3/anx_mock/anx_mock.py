import time
from concurrent.futures import ThreadPoolExecutor
import signal

from progress.spinner import PixelSpinner as Spinner
import zmq

from anx_mock.utils import Rate
import anx_proto.python.assets_pb2 as assets_pb2
import anx_proto.python.device_pb2 as device_pb2
import anx_proto.python.common_pb2 as common_pb2
from anx_mock.assets.device_imu import DeviceImu
from anx_mock.assets.device_gnss import DeviceGnss
from anx_mock.assets.device_camera import DeviceCamera

class AnxMock:
    def __init__(self):
        self.active = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.executor = ThreadPoolExecutor()

        self.ctx = zmq.Context()

        self.socket_rpc = self.ctx.socket(zmq.REP)
        self.socket_rpc.bind("ipc:///ipc/device_rpc")
        self.poller_rpc = zmq.Poller()
        self.poller_rpc.register(self.socket_rpc, zmq.POLLIN)

        self.rpc = {
                b"GetAssetState": self.get_asset_state,
                b"StartDeviceImu": self.start_device_imu,
                b"StartDeviceGnss": self.start_device_gnss,
                b"StartDeviceCamera": self.start_device_camera,
                b"StopDeviceImu": self.stop_device_imu,
                b"StopDeviceGnss": self.stop_device_gnss,
                b"StopDeviceCamera": self.stop_device_camera,
                b"GetImeiNumbers": self.get_imei_numbers,
                b"Shutdown": self.shutdown,
                b"Reboot": self.reboot,
                b"RestartAnxService": self.restart_anx_service,
                b"SetWifi": self.set_wifi,
                b"SetHotspot": self.set_hotspot,
                b"GetFloOsVersion": self.get_floos_version,
                b"GetAnxVersion": self.get_anx_version,
                b"StartAndroidLogs": self.start_android_logs,
                b"StopAndroidLogs": self.stop_android_logs
        }

        self.device_imu = DeviceImu(self.executor)
        self.device_gnss = DeviceGnss(self.executor)
        self.device_camera = DeviceCamera(self.executor)

    # Blocking call
    def start(self):
        if self.active:
            return

        self.active = True
        self.executor.submit(self.rpc_handler)

        spinner = Spinner('AnxMock running ')
        while self.active:
            spinner.next()
            time.sleep(0.1)

        self.executor.shutdown(wait=True)

    def signal_handler(self, sig, fram):
        self.active = False
        self.device_imu.stop()
        self.device_gnss.stop()
        self.device_camera.stop()
        print("\nAnxMock stopped running")

    def rpc_handler(self):
        while self.active:
            events = self.poller_rpc.poll(100)
            if events:
                name, req_bytes = self.socket_rpc.recv_multipart()
                if name in self.rpc.keys():
                    self.rpc[name](req_bytes)

    def get_asset_state(self, req_bytes):
        rep = assets_pb2.AssetState()

        rep.imu.fps.extend(self.device_imu.get_fps())
        rep.gnss.available = True
        rep.camera.camera_streams.extend(self.device_camera.get_camera_streams())

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def start_device_imu(self, req_bytes):
        req = assets_pb2.StartDeviceImu()
        req.ParseFromString(req_bytes)

        rep = common_pb2.StdResponse()
        rep.success = self.device_imu.start(req.fps)

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def start_device_gnss(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = self.device_gnss.start()

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def start_device_camera(self, req_bytes):
        req = assets_pb2.StartDeviceCamera()
        req.ParseFromString(req_bytes)

        rep = common_pb2.StdResponse()
        rep.success = self.device_camera.start(
            req.camera_stream.fps,
            req.camera_stream.width,
            req.camera_stream.height,
            req.camera_stream.pixel_format
        )

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def stop_device_imu(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = self.device_imu.stop()

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def stop_device_gnss(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = self.device_gnss.stop()

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def stop_device_camera(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = self.device_camera.stop()

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def get_imei_numbers(self, req_bytes):
        rep = device_pb2.GetImeiNumbersResponse()
        rep.imeis.extend(["869781035780142", "869781035780159"])
        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def shutdown(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = True
        rep.message = "Shutting down!!"

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def reboot(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = True
        rep.message = "Rebooting!!"

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def restart_anx_service(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = True
        rep.message = "Restar initiated.."

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def set_wifi(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = True
        rep.message = "wifi set!!"

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def set_hotspot(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = True
        rep.message = "hotspot set!!"

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def get_floos_version(self, req_bytes):
        rep = device_pb2.VersionResponse()
        rep.version = "0.1.0"

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def get_anx_version(self, req_bytes):
        rep = device_pb2.VersionResponse()
        rep.version = "0.1.0"

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def start_android_logs(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = True
        rep.message = "Started android logs!!"

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

    def stop_android_logs(self, req_bytes):
        rep = common_pb2.StdResponse()
        rep.success = True
        rep.message = "Stopped android logs!!"

        rep_bytes = rep.SerializeToString()
        self.socket_rpc.send(rep_bytes)

def main():
    anx_mock = AnxMock()
    anx_mock.start()

if __name__ == '__main__':
    main()
