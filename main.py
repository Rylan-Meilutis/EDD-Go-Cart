from typing import *
from ctre import *
import cv2
import numpy as np
# import RPi.GPIO as gpio

pot_range = 10000
brake_actuator = TalonSRX(3)
left_falcon = TalonFX(1)
right_falcon = TalonFX(2)


def main() -> NoReturn:
    while True:
        right_falcon.setInverted(True)
        left_falcon.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)
        right_falcon.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)
        brake_actuator.configSelectedFeedbackSensor(FeedbackDevice.Analog, 0)
        text = str(int(get_speed() + 0.5)) + " MPH"
        frame = np.zeros(shape=(1920, 1080, 3))
        cv2.putText(frame, text, (420, 800), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2, 2)
        cv2.imshow("Speedometer", frame)
        pot_pos = brake_actuator.getSelectedSensorPosition(0)
        if pot_pos > 10:
            left_falcon.set(TalonFXControlMode.PercentOutput, pot_pos/pot_range)
            right_falcon.set(TalonFXControlMode.PercentOutput, pot_pos/pot_range)
            brake_actuator.set(TalonSRXControlMode.PercentOutput, 0)
        elif pot_pos < -10:
            left_falcon.set(TalonFXControlMode.PercentOutput, 0)
            right_falcon.set(TalonFXControlMode.PercentOutput, 0)
            brake_actuator.set(TalonSRXControlMode.PercentOutput, pot_pos/pot_range)


def get_speed() -> float:
    return (((left_falcon.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + (right_falcon.
                                                                                       getSelectedSensorVelocity() * 10
                                                                                       / 2048 * 60) * 8 / 1056) / 2


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting cuz of keyboard interrupt")
        exit(69420)
