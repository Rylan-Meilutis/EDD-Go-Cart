from typing import NoReturn

import ctre
import gpiozero as gpio
import rev


class drivetrain:
    __pot_range = 1

    def __init__(self) -> NoReturn:
        self.__use_brake_light = True
        try:
            self.__brake_light_dev = gpio.LED(2)
        except gpio.exc.BadPinFactory:
            self.__use_brake_light = False
            pass
        self.__falcon1 = ctre.TalonFX(1)
        self.__falcon2 = ctre.TalonFX(2)
        self.__falcon3 = ctre.TalonFX(3)
        self.__falcon4 = ctre.TalonFX(4)
        self.__falcon5 = ctre.TalonFX(5)
        self.__falcon6 = ctre.TalonFX(6)
        self.__brake_actuator = rev.CANSparkMax(3, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.__brake_pid = self.__brake_actuator.getPIDController()
        self.__config()

    def __config(self) -> NoReturn:
        brake_pid = self.__brake_pid
        brake_kp = 0.8
        brake_ki = 0.0
        brake_kd = 0.0
        brake_kf = 0.0
        brake_kiz = 0.0
        brake_kim = 0.0

        self.__falcon1.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.__falcon2.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.__falcon3.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.__falcon4.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.__falcon5.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.__falcon6.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)

        brake_pid.setP(brake_kp)
        brake_pid.setI(brake_ki)
        brake_pid.setD(brake_kd)
        brake_pid.setFF(brake_kf)
        brake_pid.setIZone(brake_kiz)
        brake_pid.setIMaxAccum(brake_kim)

    def drive(self, speed: float) -> NoReturn:
        control_mode = ctre.TalonFXControlMode.PercentOutput
        self.__falcon1.set(control_mode, speed)
        self.__falcon2.set(control_mode, speed)
        self.__falcon3.set(control_mode, speed)
        self.__falcon4.set(control_mode, speed)
        self.__falcon5.set(control_mode, speed)
        self.__falcon6.set(control_mode, speed)

    def stop_motors(self) -> NoReturn:
        control_mode = ctre.TalonFXControlMode.PercentOutput
        self.__falcon1.set(control_mode, 0)
        self.__falcon2.set(control_mode, 0)
        self.__falcon3.set(control_mode, 0)
        self.__falcon4.set(control_mode, 0)
        self.__falcon5.set(control_mode, 0)
        self.__falcon6.set(control_mode, 0)

    def get_speed(self) -> float:
        return ((self.__falcon1.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.__falcon2.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.__falcon3.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.__falcon4.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.__falcon5.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.__falcon6.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) / 6

    def get_cruise_speed(self) -> float:
        return (self.__falcon1.getSelectedSensorVelocity() +
                self.__falcon2.getSelectedSensorVelocity() +
                self.__falcon3.getSelectedSensorVelocity() +
                self.__falcon4.getSelectedSensorVelocity() +
                self.__falcon5.getSelectedSensorVelocity() +
                self.__falcon6.getSelectedSensorVelocity()) / 6

    def brake(self, power: float) -> NoReturn:
        power /= self.__pot_range
        if power < 0:
            power = 0
        elif power > 1:
            power = 1
        if self.__use_brake_light:
            if power > 0:
                self.__brake_light_dev.on()
            else:
                self.__brake_light_dev.off()

        pos = power * 42
        self.__brake_pid.setReference(pos, rev.CANSparkMaxLowLevel.ControlType.kPosition)
