from typing import NoReturn

import gpiozero as gpio
import ctre
import rev


class drivetrain:
    pot_range = 1

    def __init__(self) -> NoReturn:
        self.brake_light_dev = gpio.LED(2)
        self.falcon1 = ctre.TalonFX(1)
        self.falcon2 = ctre.TalonFX(2)
        self.falcon3 = ctre.TalonFX(3)
        self.falcon4 = ctre.TalonFX(4)
        self.falcon5 = ctre.TalonFX(5)
        self.falcon6 = ctre.TalonFX(6)
        self.brake_actuator = rev.CANSparkMax(3, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.brake_pid = self.brake_actuator.getPIDController()

    def config(self) -> NoReturn:
        brake_pid = self.brake_pid
        brake_kp = 0.8
        brake_ki = 0.0
        brake_kd = 0.0
        brake_kf = 0.0
        brake_kiz = 0.0
        brake_kim = 0.0

        self.falcon1.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.falcon2.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.falcon3.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.falcon4.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.falcon5.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.falcon6.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)

        brake_pid.setP(brake_kp)
        brake_pid.setI(brake_ki)
        brake_pid.setD(brake_kd)
        brake_pid.setFF(brake_kf)
        brake_pid.setIZone(brake_kiz)
        brake_pid.setIMaxAccum(brake_kim)

    def drive(self, speed: float) -> NoReturn:
        control_mode = ctre.TalonFXControlMode.PercentOutput
        self.falcon1.set(control_mode, speed)
        self.falcon2.set(control_mode, speed)
        self.falcon3.set(control_mode, speed)
        self.falcon4.set(control_mode, speed)
        self.falcon5.set(control_mode, speed)
        self.falcon6.set(control_mode, speed)

    def stop_motors(self) -> NoReturn:
        control_mode = ctre.TalonFXControlMode.PercentOutput
        self.falcon1.set(control_mode, 0)
        self.falcon2.set(control_mode, 0)
        self.falcon3.set(control_mode, 0)
        self.falcon4.set(control_mode, 0)
        self.falcon5.set(control_mode, 0)
        self.falcon6.set(control_mode, 0)

    def get_speed(self) -> float:
        return ((self.falcon1.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.falcon2.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.falcon3.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.falcon4.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.falcon5.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
               ((self.falcon6.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) / 6

    def get_cruise_speed(self) -> float:
        return (self.falcon1.getSelectedSensorVelocity() +
                self.falcon2.getSelectedSensorVelocity() +
                self.falcon3.getSelectedSensorVelocity() +
                self.falcon4.getSelectedSensorVelocity() +
                self.falcon5.getSelectedSensorVelocity() +
                self.falcon6.getSelectedSensorVelocity()) / 6

    def brake(self, power: float) -> NoReturn:
        power /= self.pot_range
        if power < 0:
            power = 0
        elif power > 1:
            power = 1

        if power > 0:
            self.brake_light_dev.on()
        else:
            self.brake_light_dev.off()

        pos = power * 42
        self.brake_pid.setReference(pos, rev.CANSparkMaxLowLevel.ControlType.kPosition)
