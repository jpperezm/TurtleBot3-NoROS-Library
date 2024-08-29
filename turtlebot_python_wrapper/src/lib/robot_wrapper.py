import serial
import time
import struct
import threading
import math

class Robot:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        time.sleep(2)  # Allow some time for the serial connection to establish
        self.last_time = time.time()

    def step(self, timestep):
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        time_to_wait = (timestep / 1000.0) - elapsed_time
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        self.last_time = time.time()
        return 0  # Mimic Webots step function, returning 0 to continue running

    def getDevice(self, name):
        if name == 'left wheel motor':
            return Motor('left', self.serial)
        elif name == 'right wheel motor':
            return Motor('right', self.serial)
        elif name == 'left wheel sensor':
            return PositionSensor(1, self.serial)
        elif name == 'right wheel sensor':
            return PositionSensor(2, self.serial)
        elif name == 'accelerometer':
            return Accelerometer(self.serial)
        elif name == 'gyro':
            return Gyro(self.serial)
        elif name == 'inertial unit':
            return InertialUnit(self.serial)
        elif name == 'LDS-01':
            return Lidar('/dev/ttyUSB0')  # Use the specific serial port for LiDAR
        else:
            raise ValueError("Unknown device name")

class Motor:
    def __init__(self, side, serial):
        self.side = side
        self.serial = serial
        self.max_speed = 256

    def __del__(self):
        self.setVelocity(0.0)

    def setPosition(self, position):
        # TODO: Implement this method
        pass

    def setVelocity(self, velocity):
        velocity = translateVelocity(velocity)
        command = f'SET_VELOCITY_{self.side.upper()} {velocity}'
        self.serial.write((command + '\n').encode())
        #time.sleep(0.01)  # Give some time for the command to be processed

class PositionSensor:
    def __init__(self, id, serial):
        self.id = id
        self.serial = serial
        self.encoder_value = 0
        self.distance_value = 0
        command = f'READ_SENSOR {self.id}'
        self.serial.write((command + '\n').encode())
        #time.sleep(0.1)
        response = self.serial.readline().decode().strip()

        self.initial_value = int(response)
        self.counts_per_revolution = 4096
        self.radians_per_count = 2 * 3.141592653589793 / self.counts_per_revolution

    def enable(self, timestep):
        # Assume enabling sensor just sets up a flag or similar
        pass

    def getValue(self):
        command = f'READ_SENSOR {self.id}'
        self.serial.write((command + '\n').encode())
        response = self.serial.readline().decode().strip()

        if response:
            current_value = int(response)
            if self.initial_value is None:
                self.initial_value = current_value
            adjusted_value = current_value - self.initial_value
            distance_in_radians = adjusted_value * self.radians_per_count
            return distance_in_radians
        else:
            raise ValueError("No response received from sensor")

class Accelerometer:
    def __init__(self, serial):
        self.serial = serial

    def enable(self, sampling_period):
        # Webots compatibility; not used in real robot
        pass

    def disable(self):
        # Webots compatibility; not used in real robot
        pass

    def getValues(self):
        command = 'READ_IMU_ACC'
        self.serial.write((command + '\n').encode())
        response = self.serial.readline().decode().strip()
        return list(map(float, response.split('\t')))

class Gyro:
    def __init__(self, serial):
        self.serial = serial

    def enable(self, sampling_period):
        # Webots compatibility; not used in real robot
        pass

    def disable(self):
        # Webots compatibility; not used in real robot
        pass

    def getValues(self):
        command = 'READ_IMU_GYRO'
        self.serial.write((command + '\n').encode())
        response = self.serial.readline().decode().strip()
        gyro_values = list(map(float, response.split('\t')))
        # print(f"Raw gyro values: {gyro_values}")
        # Convert the values from raw units to degrees per second and then to radians per second
        gyro_values_deg_per_sec = [value / 16.4 for value in gyro_values]
        gyro_values_rad_per_sec = [math.radians(value) for value in gyro_values_deg_per_sec]
        # print(f"Gyro values in º/s: {gyro_values_deg_per_sec}")
        return gyro_values_rad_per_sec

class InertialUnit:
    def __init__(self, serial):
        self.serial = serial

    def enable(self, sampling_period):
        # Webots compatibility; not used in real robot
        pass

    def disable(self):
        # Webots compatibility; not used in real robot
        pass

    def getRollPitchYaw(self):
        command = 'READ_IMU_RPY'
        self.serial.write((command + '\n').encode())
        response = self.serial.readline().decode().strip()
        return list(map(float, response.split('\t')))


# Lidar Class with threading for continuous data grabbing
class Lidar:
    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.serial = serial.Serial(self.serial_port, 230400, timeout=1)
        self.distance_list = [None] * 360
        self.data_lock = threading.Lock()
        self.is_running = False
        self.data_thread = threading.Thread(target=self.grab_data)
    
    def enable(self, timestep):
        self.is_running = True
        self.serial.write(b'b')  # Start scanning
        self.data_thread.start()
        #time.sleep(0.01)  # Give some time for the command to be processed

    def disable(self):
        self.is_running = False
        self.serial.write(b'e')  # Stop scanning
        self.data_thread.join()
        #time.sleep(0.01)  # Give some time for the command to be processed
    
    def grab_data(self):
        try:
            while self.is_running:
                result = self.serial.read(42)
                if len(result) != 42:
                    continue  # Ensure we read the full packet

                if result[-1] == result[-2]:  # Simple checksum verification
                    rpm = result[3] * 256 + result[2]
                    base_angle = (result[1] - 160) * 6

                    with self.data_lock:
                        for m in range(6):
                            angle = (base_angle + m) % 360  # Ensure angle is within 0-359
                            distance = result[((6 * (m + 1)) + 1)] * 256 + result[((6 * (m + 1)))]

                            if distance > 0:
                                self.distance_list[angle] = distance / 1000
                            else:
                                self.distance_list[angle] = None

        except IndexError:
            self.serial.write(b'e')
            print('Stopped! Out of sync.')
        except Exception as e:
            print(f"Error: {e}")

    def getRangeImage(self):
        with self.data_lock:
            range_image = list(self.distance_list)
        # Replace None with float('inf')
        range_image = [x if x is not None else float('inf') for x in range_image]
        """         aux_range = range_image[0:179]
        range_image[0:179] = range_image[180:359]
        range_image[180:359] = aux_range """
        range_image[0:179], range_image[180:359] = range_image[180:359], range_image[0:179]
        # print(range_image)
        return range_image
    
    def get_layer_range_image(self, layer):
        # For simplicity, we'll return the same range image for all layers
        return self.getRangeImage()

    def get_frequency(self):
        # Placeholder, as the actual frequency might not be settable/readable in this way
        return 10

    def set_frequency(self, frequency):
        # Placeholder, as the actual frequency might not be settable in this way
        pass

    def get_horizontal_resolution(self):
        # Placeholder value
        return 512

    def get_number_of_layers(self):
        # Placeholder value
        return 1

    def get_min_frequency(self):
        return 1

    def get_max_frequency(self):
        return 25

    def get_fov(self):
        # Placeholder value
        return 1.5708

    def get_vertical_fov(self):
        # Placeholder value
        return 0.2

    def get_min_range(self):
        return 0.01

    def get_max_range(self):
        return 1.0

def init_robot():
    return Robot()

def translateVelocity(webots_velocity):
    # Webots values range
    webots_min = 0
    webots_max = 6.67
    
    # Real robot values range
    real_min = 0
    real_max = 265
    
    # Translate the webots_velocity to real robot velocity
    real_velocity = ((webots_velocity - webots_min) / (webots_max - webots_min)) * (real_max - real_min) + real_min
    
    return real_velocity