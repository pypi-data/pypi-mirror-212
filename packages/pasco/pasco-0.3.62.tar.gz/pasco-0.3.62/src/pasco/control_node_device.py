from .pasco_ble_device import PASCOBLEDevice
import time


class ControlNodeDevice(PASCOBLEDevice):
    #TODO: make a context manager that handles connecting and disconnecting from the codeNode

    # Control Node commands
    CTRLNODE_CMD_SET_SERVO = 3              # Enables PWM to servo
    CTRLNODE_CMD_SET_STEPPER = 4            # Enables stepper motor
    CTRLNODE_CMD_SET_SIGNALS = 5            # Sets motor control signals directly
    CTRLNODE_CMD_XFER_ACCESSORY = 6         # Write I2C accessory and read response
    CTRLNODE_CMD_READ_LINE_FOLLOWER = 7     # Read the line follower accessory
    CTRLNODE_CMD_GET_STEPPER_INFO = 8       # Get stepper remaining distance and remaining angular velocity to accelerate to
    CTRLNODE_CMD_STOP_ACCESSORIES = 9       # Turn off all steppers, servos, and accessories
    CTRLNODE_CMD_SET_BEEPER = 10            # Set beeper frequency

    CN_ACC_ID_NONE = 0
    CN_ACC_ID_MOTOR_BASE = 2500
    CN_ACC_ID_STEPPER_480 = 2501
    CN_ACC_ID_STEPPER_4800 = 2502
    CN_ACC_ID_MOTOR_3 = 2503
    CN_ACC_ID_LINE_FOLLOWER = 2504
    CN_ACC_ID_RANGE_SENSOR = 2505

    STEPPER_A_CHANNEL = 1
    STEPPER_B_CHANNEL = 2
    BOTH_STEPPER_CHANNEL = 3

# ----------- Steppers --------------

    def _send_stepper_command(self, speedA, accelerationA, distanceA, speedB, accelerationB, distanceB):
        """
        Arguments:
        speed: degrees/second
        acceleration: degrees/second/second
        distance: degrees or 'continous'

        If distance == 'continous' then the steppers rotate continuously
        To send a command to only one stepper, set the other stepper's parameters to None.
        i.e. if accelerationA is None then only stepper B will run.

        """

        # determine what steppers we are sending commands to
        stepper_channel = self.BOTH_STEPPER_CHANNEL
        if accelerationA == None and accelerationB != None:
            stepper_channel = self.STEPPER_B_CHANNEL
            accelerationA = 0
            speedA = 0
            distanceA = 0
        if accelerationB == None and accelerationA != None: 
            stepper_channel = self.STEPPER_A_CHANNEL
            accelerationB = 0
            speedB = 0
            distanceB = 0

        # deal with rotating stepper continuously
        continous1 = distanceA == 'continuous'
        continous2 = distanceB == 'continuous'

        mul = {}
        for sensor in self._setup_sensors:
            if 'channel_id_tag' in sensor:
                mul[sensor['id']] = 10 if sensor['sensor_id'] == self.CN_ACC_ID_STEPPER_4800 else 1

        # Convert speeds from deg/s[/s] to decisteps/s[/s] and distances from deg to steps
        STEPS_PER_REV = 960
        DEGREES_PER_REV = 360
        DECISTEPS_PER_STEP = 10
        
        speedA = speedA * mul[0] * DECISTEPS_PER_STEP * STEPS_PER_REV / DEGREES_PER_REV
        speedB = speedB * mul[1] * DECISTEPS_PER_STEP * STEPS_PER_REV / DEGREES_PER_REV
        accelerationA = accelerationA * mul[0] * DECISTEPS_PER_STEP * STEPS_PER_REV / DEGREES_PER_REV
        accelerationB = accelerationB * mul[1] * DECISTEPS_PER_STEP * STEPS_PER_REV / DEGREES_PER_REV
        distanceA = 0 if continous1 else distanceA * mul[0] * STEPS_PER_REV / DEGREES_PER_REV
        distanceB = 0 if continous2 else distanceB * mul[1] * STEPS_PER_REV / DEGREES_PER_REV

        speedA = int(self._limit( speedA, -19200, 19200 ))
        accelerationA = int(self._limit( accelerationA, 0, 65535 ))
        distanceA = int(self._limit( distanceA, 0, 65535 ))
        speedB = int(self._limit( speedB, -19200, 19200 ))
        accelerationB = int(self._limit( accelerationB, 0, 65535 ))
        distanceB = int(self._limit( distanceB, 0, 65535 ))

        """
        Stepper command has 16 bits:
        - command "set stepper"
        - channels (1, 2, 3 <-> port A, B, both)
        - 2 bits target speed channel 1
        - 2 bits acceleration channel 1
        - 2 bits distance channel 1
        - 2 bits target speed channel 2
        - 2 bits acceleration channel 2
        - 2 bits distance channel 2
        - extra bit distance channel 1
        - extra bit distance channel 2
        """

        command = [ self.GCMD_CONTROL_NODE_CMD, self.CTRLNODE_CMD_SET_STEPPER, stepper_channel, 
            speedA & 0xFF, speedA>>8 & 0XFF,
            accelerationA & 0xFF, accelerationA>>8 & 0XFF,
            distanceA & 0xFF, distanceA>>8 & 0XFF,
            speedB & 0xFF, speedB>>8 & 0XFF,
            accelerationB & 0xFF, accelerationB>>8 & 0XFF,
            distanceB & 0xFF, distanceB>>8 & 0XFF
        ]

        self._loop.run_until_complete(self.write_await_callback(self.SENSOR_SERVICE_ID, command))


    def rotate_steppers_continuously(self, speedA, accelerationA, speedB, accelerationB):
        """
        rotate steppers continuously at given accelerations to given speeds

        """
        if not self.is_connected():
            raise self.DeviceNotConnected()
        
        self._send_stepper_command(
            speedA, accelerationA, 'continuous', speedB, accelerationB, 'continuous')


    def rotate_stepper_continuously(self, port, speed, acceleration):
        """
        Rotate a single stepper continously
        """
        if port.upper() == "A":
            self.rotate_steppers_continuously(speed, acceleration, None, None)
        elif port.upper() == "B":
            self.rotate_steppers_continuously(None, None, speed, acceleration)    
        else:
            raise self.InvalidParameter()


    def stop_steppers(self, accelerationA, accelerationB):
        """
        Decelarate steppers at given accelerations until they stop
        Args:
            accelerationA (double): acceleration at which to stop stepper A
            accelerationB (double): acceleration at which to stop stepper B

        """
        self._send_stepper_command(
            0, accelerationA, 'continuous', 0, accelerationB, 'continuous')
        

    def stop_stepper(self, port, acceleration):
        """
        Stop the stepper in the given port with given acceleration
        """
        if port.upper() == "A":
            self.stop_steppers(acceleration, None)
        elif port.upper() == "B":
            self.stop_steppers(None, acceleration)  
        else:
            raise self.InvalidParameter()
        pass


    def rotate_steppers_through(self, speedA, accelerationA, distanceA, speedB, accelerationB, distanceB):
        # TODO: implement a wait for complete functionality like the 
        # "wait for completion" checkbox in Blockly
        """
        Set the Control Node stepper motors

        Args:
            speed1 (float): deg/s
            accel1 (float): deg/s/s
            distance1 (float): degrees
            speed2 (float): deg/s
            accel2 (float): deg/s/s
            distance2 (float): degrees

               
        check if the service uuid is in self._services_awaiting_callback. if so then wait on it?
        if await_completion then synchronously await the callback with write_await_callback()
        else asynchronously await completion, checking for callback in reset()

        """
        if self.is_connected() is False:
            raise self.DeviceNotConnected()

        self._send_stepper_command(
            speedA, accelerationA, distanceA, speedB, accelerationB, distanceB
        )


    def rotate_stepper_through(self, port, speed, acceleration, distance):
        """
        Rotate a single stepper through the given distance
        """
        if port.upper() == "A":
            self.rotate_steppers_through(speed, acceleration, distance, None, None, None)
        elif port.upper() == "B":
            self.rotate_steppers_through(None, None, None, speed, acceleration, distance) 
        else:
            raise self.InvalidParameter()

#TODO: write code for low speed steppers
# in Blockly the measurements for stepper movement don't correspond for the 
# low speed stepper. It seems it is sending the same command as for the high speed stepper

# ------------ Sensors --------------

#TODO: sense what is plugged into Sensor and Power Out ports A and B. 
#TODO: read data from external sensors:
# - Sensor port
# - Stepper angle and velocity measures
# - Servo current



# -------------- Servos ----------------

    def _calculate_on_time(self, measure_type, value):
        """
        Calculate the on-time of the PWM command.
        Servos are controlled by Pulse Width Manipulation: commands are sent via 20 ms
        pulses, where the width of the pulse corresponds to the value of the command.
        The formula of the relation depends on the command:
        - angle:   t = (angle + 150) [10 microseconds]
        - % speed: t = 0.2p   + 150  [10 microseconds] (where p is a percent of the total speed)
        The control Node interprets the data in units of 10 microseconds = 100 ms.
        """
        on_time = 0
        if measure_type == "standard":
            on_time = int(value + 150)
        elif measure_type == "continuous":
            on_time = int(0.2*value + 150)

        return on_time

    def set_servos(self, ch_1_type, ch_1_value, ch_2_type, ch_2_value):
        """
        set the servos in channels 1 and 2
        Args:
            ch_1_type (str): "standard" or "continuous" servo type
            ch_1_value (float): value of either degrees or percent speed
            ch_2_type [same]
            ch_2_value [same]
        """
        if not self.is_connected:
            raise self.DeviceNotConnected()
        
        if self.is_connected() is False:
            raise self.DeviceNotConnected()

        # determine what servo channels you are powering:
        # 1: channel 1 only
        # 2: channel 2 only
        # 3: channel 1 and channel 2
        channels = int(ch_1_type != 0) + 2*int(ch_2_type != 0)
        # set_servos(0, 0, 0, 0) means ALL OFF and needs to go to both channels
        channels = 3 if channels == 0 else channels
        
        period1 = 2000 # 20 ms period (servo value)
        period2 = 2000 # 20 ms period (servo value)
        onTime1 = self._calculate_on_time(ch_1_type, ch_1_value)
        onTime2 = self._calculate_on_time(ch_2_type, ch_2_value)

        cmd = [ self.GCMD_CONTROL_NODE_CMD, self.CTRLNODE_CMD_SET_SERVO, channels, 
            onTime1 & 0xFF, onTime1>>8 & 0XFF,
            period1 & 0xFF, period1>>8 & 0XFF,
            onTime2 & 0xFF, onTime2>>8 & 0XFF,
            period2 & 0xFF, period2>>8 & 0XFF,
        ]
        self._loop.run_until_complete(self.write_await_callback(self.SENSOR_SERVICE_ID, cmd))

    def set_servo(self, port, type, value):
        """
        set a single servo
        Args:
            port (int): which servo channel to power (1 or 2)
            type (str): servo type. "standard" or "continuous".
            value (float): value of either degrees or percent speed
        """
        if port == 1:
            self.set_servos(type, value, 0, 0)
        elif port == 2:
            self.set_servos(0, 0, type, value)
        else:
            raise self.InvalidParameter()

    
# --------- Power Board ----------------


    # TODO: Test this
    def set_power_out(self):
        """
        Control the power output board

        Args:
        """
        signalBits = 2
        pwmPeriod = 1000
        pwmValues = [10, 10, 10, 10, 10, 10, 10, 10]
        
        cmd = [ self.GCMD_CONTROL_NODE_CMD, self.CTRLNODE_CMD_SET_SIGNALS, signalBits, 
            pwmPeriod & 0xFF, pwmPeriod>>8 & 0XFF,
            pwmValues[0], pwmValues[1], pwmValues[2], pwmValues[3],
            pwmValues[4], pwmValues[5], pwmValues[6], pwmValues[7]
        ]
        self._loop.run_until_complete(self.write_await_callback(self.SENSOR_SERVICE_ID, cmd))


    def set_sound_frequency(self, frequency):
        """
        Set the frequency of the control node's built in speaker

        Args:
            Frequency (in hertz)
        """
        if self.is_connected() is False:
            raise self.DeviceNotConnected()

        if frequency and type(frequency) not in (int, float):
            raise self.InvalidParameter

        frequency = self._limit(frequency, 0, 20000)

        cmd = [ self.GCMD_CONTROL_NODE_CMD, self.CTRLNODE_CMD_SET_BEEPER, frequency & 0xFF, frequency>>8 & 0XFF ]
        self._loop.run_until_complete(self.write_await_callback(self.SENSOR_SERVICE_ID, cmd))


# --------- Convenience -----------

    def reset(self):
        """
        Reset the speaker and LEDs on the code node
        """
        
        if self.is_connected() is False:
            raise self.DeviceNotConnected()

        self.set_sound_frequency(0)
        self.set_servos(0, 0, 0, 0)
        self.rotate_steppers_through(0, 0, 0, 0, 0, 0)


def main():
    
    device = ControlNodeDevice()

    found_devices = device.scan()

    if len(found_devices) == 0:
        print("No devices found")
        exit(1)

    print('Devices Found')
    for i, ble_device in enumerate(found_devices):
        print(f'{i}: {ble_device.name}')

    selected_device = input('Select a device: ') if len(found_devices) > 1 else 0
    ble_device = found_devices[int(selected_device)]

    device.connect(ble_device)

    device.set_sound_frequency(500)

    """
    speed1 = 100
    accel1 = 0
    distance1 = 360
    speed2 = 100
    accel2 = 0
    distance2 = 360

    device.set_steppers(speed1, accel1, distance1, speed2, accel2, distance2)
    """

    
    for i in range(-100,101, 10):
        device.set_servos(2, i, 0, i)
        time.sleep(1)

    i = 0
    device.set_servos(1, i, 0, i)

    #device.controlnode_signals()

    device.disconnect()
    #for i in range(100):
    #    for m in measurements:
    #        print(f'{m} : {my_sensor.read_data(m)}')


if __name__ == "__main__":
    main()
