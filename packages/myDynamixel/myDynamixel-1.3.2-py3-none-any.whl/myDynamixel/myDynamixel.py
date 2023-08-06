# ver 1.3.2

import numpy as np
from dynamixel_sdk import *

class Dxlfunc:
    class Adrress:
        ModelNumber         = 0
        ModelInformation    = 2
        VersionOfFirmware   = 6
        ID                  = 7
        BaudRate            = 8
        ReturnDelayTime     = 9
        DriveMode           = 10
        OperatingMode       = 11
        SecondaryShadowID   = 12
        ProtocolVersion     = 13
        HomingOffset        = 20
        MovingThreshold     = 24
        TemperatureLimit    = 31
        MaxVoltageLimit     = 32
        MinVoltageLimit     = 34
        PWMLimit            = 36
        CurrentLimit        = 38
        AccelerationLimit   = 40
        VelocityLimit       = 44
        MaxPositionLimit    = 48
        MinPositionLimit    = 52
        Shutdown            = 63
        TorqueEnable        = 64
        LED                 = 65
        StatusReturnLevel   = 68
        RegisteredInstruction = 69
        HardwareErrorStatus = 70
        VelocityIGain       = 76
        VelocityPGain       = 78
        PositionDGain       = 80
        PositionIGain       = 82
        PositionPGain       = 84
        Feedforward2ndGain  = 88
        Feedforward1stGain  = 90
        BusWatchdog         = 98
        GoalPWM             = 100
        GoalCurrent         = 102
        GoalVelocity        = 104
        ProfileAcceleration = 108
        ProfileVelocity     = 112
        GoalPosition        = 116
        RealtimeTick        = 120
        Moving              = 122
        MovingStatus        = 123
        PresentPWM          = 124
        PresentCurrent      = 126
        PresentVelocity     = 128
        PresentPosition     = 132
        VelocityTrajectory  = 136
        PositionTrajectory  = 140
        PresentInputVoltage = 144
        PresentTemperature  = 146

    class operating_mode:
        current_control = 0
        velocity_control = 1
        position_control = 3
        extended_Position_control = 4
        current_base_position_control = 5
        pwm_control = 16

    class ModelNumber:
        XC330_M077 = 1190
        XC330_M181 = 1200
        XC330_M288 = 1240
        XC330_T181 = 1210
        XC330_T288 = 1220
        XL430_W250 = 1230
        twoXL430_W250 = 1090
        XC430_W150 = 1070
        XC430_W250 = 1080
        twoXC430_W250 = 1160
        XM430_W210 = 1030
        XH430_W210 = 1010
        XH430_V210 = 1050
        XD430_T210 = 1011
        XM430_W350 = 1020
        XH430_W350 = 1000
        XH430_V350 = 1040
        XD430_T350 = 1001
        XW430_T200 = 1280
        XW430_T333 = 1270
        XM540_W150 = 1130
        XH540_W150 = 1110
        XH540_V150 = 1150
        XM540_W270 = 1120
        XH540_W270 = 1100
        XH540_V270 = 1140
        XW540_T140 = 1180
        XW540_T260 = 1170

    class __initErrorCode:
        USB_disconnect = -3000
        PowerSource_disconnect = -3001

    class DXL_Error(Exception):
        pass

    def __init__(self):
        self._portHandler = None
        self._packetHandler = PacketHandler(2.0)
        self.IDs = []
        self.Present_OperatingMode = -1
        self._one_byte_values = [self.Adrress.ID, self.Adrress.BaudRate, self.Adrress.ReturnDelayTime,
                                 self.Adrress.DriveMode, self.Adrress.OperatingMode,
                                 self.Adrress.SecondaryShadowID, self.Adrress.ProtocolVersion,
                                 self.Adrress.TemperatureLimit, self.Adrress.Shutdown,
                                 self.Adrress.TorqueEnable, self.Adrress.LED,
                                 self.Adrress.StatusReturnLevel, self.Adrress.HardwareErrorStatus,
                                 self.Adrress.BusWatchdog, self.Adrress.Moving,
                                 self.Adrress.MovingStatus, self.Adrress.PresentTemperature]
        self._two_byte_values = [self.Adrress.ModelNumber, self.Adrress.MaxVoltageLimit, self.Adrress.MinVoltageLimit,
                                 self.Adrress.PWMLimit, self.Adrress.CurrentLimit,
                                 self.Adrress.VelocityPGain, self.Adrress.VelocityPGain,
                                 self.Adrress.PositionPGain, self.Adrress.PositionIGain,
                                 self.Adrress.PositionDGain, self.Adrress.Feedforward1stGain,
                                 self.Adrress.Feedforward2ndGain, self.Adrress.GoalPWM,
                                 self.Adrress.GoalCurrent, self.Adrress.RealtimeTick,
                                 self.Adrress.PresentPWM, self.Adrress.PresentCurrent,
                                 self.Adrress.PresentInputVoltage]
        self._four_byte_values = [self.Adrress.HomingOffset, self.Adrress.MovingThreshold,
                                 self.Adrress.AccelerationLimit, self.Adrress.VelocityLimit,
                                 self.Adrress.MaxPositionLimit, self.Adrress.MinPositionLimit,
                                 self.Adrress.GoalVelocity, self.Adrress.ProfileAcceleration,
                                 self.Adrress.ProfileVelocity, self.Adrress.GoalPosition,
                                 self.Adrress.PresentPosition, self.Adrress.PresentVelocity,
                                 self.Adrress.VelocityTrajectory, self.Adrress.PositionTrajectory]

    def init(self, com, baudrate=57600):
        self._portHandler = PortHandler(com)
        baudrates = [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000]
        try:
            if self._portHandler.openPort():
                self._portHandler.setBaudRate(baudrate)
                self.IDs = [i for i in range(10) if self._packetHandler.read1ByteTxRx(self._portHandler, i, self.Adrress.ID)[1] == 0]
                if len(self.IDs) == 0:
                    for br in baudrates:
                        self._portHandler.setBaudRate(br)
                        self.IDs = [i for i in range(10) if self._packetHandler.read1ByteTxRx(self._portHandler, i, self.Adrress.ID)[1] == 0]
                        if len(self.IDs) > 0:
                            raise self.DXL_Error("Argument baud rate is different from baud rate set in motor")
                if len(self.IDs) > 0:
                    return len(self.IDs)
                else:
                    return self.__initErrorCode.PowerSource_disconnect
            else:
                return self.__initErrorCode.USB_disconnect
        except serial.serialutil.SerialException:
            return self.__initErrorCode.USB_disconnect

    def exit(self):
        self.write('ALL', self.Adrress.TorqueEnable, 0)
        self._portHandler.closePort()

    def reboot(self):
        for i in self.IDs:
            if not self.read(i, self.Adrress.HardwareErrorStatus) == 0:
                self._packetHandler.reboot(self._portHandler, i)
                while not self.read(i, self.Adrress.HardwareErrorStatus) == 0:
                    pass

    def write(self, MotorID, INPUT_Adrress, value):
        if MotorID == 'ALL':
            for i in self.IDs:
                if INPUT_Adrress in self._one_byte_values:
                    self._packetHandler.write1ByteTxRx(self._portHandler, i, INPUT_Adrress, value)
                elif INPUT_Adrress in self._two_byte_values:
                    self._packetHandler.write2ByteTxRx(self._portHandler, i, INPUT_Adrress, value)
                elif INPUT_Adrress in self._four_byte_values:
                    self._packetHandler.write4ByteTxRx(self._portHandler, i, INPUT_Adrress, value)
        else:
            if INPUT_Adrress in self._one_byte_values:
                self._packetHandler.write1ByteTxRx(self._portHandler, MotorID, INPUT_Adrress, value)
            elif INPUT_Adrress in self._two_byte_values:
                self._packetHandler.write2ByteTxRx(self._portHandler, MotorID, INPUT_Adrress, value)
            elif INPUT_Adrress in self._four_byte_values:
                self._packetHandler.write4ByteTxRx(self._portHandler, MotorID, INPUT_Adrress, value)

    def read(self, MotorID, INPUT_Adrress):
        ret = 0
        if INPUT_Adrress in self._one_byte_values:
            ret, _, _ = self._packetHandler.read1ByteTxRx(self._portHandler, MotorID, INPUT_Adrress)
            if ret >= np.power(2, 7):
                ret = ret - np.power(2, 8)
        elif INPUT_Adrress in self._two_byte_values:
            ret, _, _ = self._packetHandler.read2ByteTxRx(self._portHandler, MotorID, INPUT_Adrress)
            if ret >= np.power(2, 15):
                ret = ret - np.power(2, 16)
        elif INPUT_Adrress in self._four_byte_values:
            ret, _, _ = self._packetHandler.read4ByteTxRx(self._portHandler, MotorID, INPUT_Adrress)
            if ret >= 2**31:
                ret = ret - 2**32
        return ret

    def readTorque(self, MotorID, LowCurrent=False):
        value2current = 0.00269  # Convert value to current[A]
        current = self.read(MotorID, self.Adrress.PresentCurrent) * value2current
        motorType = self.read(MotorID, self.Adrress.ModelNumber)
        if motorType == self.ModelNumber.XM430_W210:
            if LowCurrent:
                current2torque_p = 0.9221
                current2torque_b = 0
            else:
                current2torque_p = 1.02
                current2torque_b = -0.164
        elif motorType == self.ModelNumber.XM430_W350:
            if LowCurrent:
                current2torque_p = 1.6245
                current2torque_b = 0
            else:
                current2torque_p = 1.73
                current2torque_b = -0.13
        else:
            print('No convertion params for this motor model')
            return 0
        return current2torque_p * current + current2torque_b

    def Change_OperatingMode(self, MotorID, INPUT_OPERATING_MODE):
        if MotorID == 'ALL':
            for i in self.IDs:
                now_frag = self.read(i, self.Adrress.TorqueEnable)
                self.write(i, self.Adrress.TorqueEnable, 0)
                self.write(i, self.Adrress.OperatingMode, INPUT_OPERATING_MODE)
                self.write(i, self.Adrress.TorqueEnable, now_frag)
        else:
            now_frag = self.read(MotorID, self.Adrress.TorqueEnable)
            self.write(MotorID, self.Adrress.TorqueEnable, 0)
            self.write(MotorID, self.Adrress.OperatingMode, INPUT_OPERATING_MODE)
            self.write(MotorID, self.Adrress.TorqueEnable, now_frag)
        self.Present_OperatingMode = INPUT_OPERATING_MODE

    def PosCnt_Vbase(self, MotorID, Goal_position, Goal_velocity):
        if Goal_velocity < 0:
            raise self.DXL_Error('Goal velocity should be positive value in PosCnt_Vbase function')
        self.Change_OperatingMode(MotorID, self.operating_mode.extended_Position_control)
        self.write(MotorID, self.Adrress.TorqueEnable, False)
        self.write(MotorID, self.Adrress.DriveMode, 0)
        self.write(MotorID, self.Adrress.TorqueEnable, True)
        self.write(MotorID, self.Adrress.ProfileVelocity, Goal_velocity)
        self.write(MotorID, self.Adrress.GoalPosition, Goal_position)
        self.write(MotorID, self.Adrress.ProfileVelocity, 0)

    def PosCnt_Tbase(self, MotorID, Goal_position, Goal_Time):
        if Goal_Time < 0:
            raise self.DXL_Error('Goal time should be positive value in PosCnt_Tbase function')
        self.Change_OperatingMode(MotorID, self.operating_mode.extended_Position_control)
        self.write(MotorID, self.Adrress.TorqueEnable, False)
        self.write(MotorID, self.Adrress.DriveMode, 4)
        self.write(MotorID, self.Adrress.TorqueEnable, True)
        self.write(MotorID, self.Adrress.ProfileVelocity, Goal_Time)
        self.write(MotorID, self.Adrress.GoalPosition, Goal_position)
        self.write(MotorID, self.Adrress.ProfileVelocity, 0)

    def CurrentCnt_Vbase(self, MotorID, Goal_current, Goal_velocity):
        if Goal_velocity < 0:
            raise self.DXL_Error('Goal velocity should be positive value in CurrentCnt_Vbase function')
        if self.Present_OperatingMode != self.operating_mode.current_base_position_control:
            self.Change_OperatingMode(MotorID, self.operating_mode.current_base_position_control)
        self.write(MotorID, self.Adrress.TorqueEnable, False)
        self.write(MotorID, self.Adrress.DriveMode, 0)
        self.write(MotorID, self.Adrress.TorqueEnable, True)
        self.write(MotorID, self.Adrress.ProfileVelocity, Goal_velocity)
        self.write(MotorID, self.Adrress.GoalCurrent, np.abs(Goal_current))
        if Goal_current < 0:
            self.write(MotorID, self.Adrress.GoalPosition, -256*4096+1)
        else:
            self.write(MotorID, self.Adrress.GoalPosition, 256*4096-1)
        self.write(MotorID, self.Adrress.ProfileVelocity, 0)