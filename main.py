import ctre
import cv2
import numpy as np

pot_range = 10000
brake_actuator = ctre.TalonSRX(3)
left_falcon = ctre.TalonFX(1)
right_falcon = ctre.TalonFX(2)
right_falcon.setInverted(True)


def main():
    brake_actuator.configSelectedFeedbackSensor(ctre.FeedbackDevice.Analog, 0)
    while True:
        text = str(get_speed()) + " MPH"
        frame = np.zeros(shape=(1920, 1080, 3))
        cv2.putText(frame, text, (420, 800), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2, 2)
        cv2.imshow("Speedometer", frame)
        pot_pos = brake_actuator.getSelectedSensorPosition(0)
        if pot_pos > 10:
            left_falcon.set(ctre.TalonFXControlMode.PercentOutput, pot_pos/pot_range)
            right_falcon.set(ctre.TalonFXControlMode.PercentOutput, pot_pos/pot_range)
            brake_actuator.set(ctre.TalonSRXControlMode.PercentOutput, 0)
        elif pot_pos < -10:
            left_falcon.set(ctre.TalonFXControlMode.PercentOutput, 0)
            right_falcon.set(ctre.TalonFXControlMode.PercentOutput, 0)
            brake_actuator.set(ctre.TalonSRXControlMode.PercentOutput, pot_pos/pot_range)


def get_speed():
    return (((left_falcon.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + (right_falcon.
                                                                                       getSelectedSensorVelocity() * 10
                                                                                       / 2048 * 60) * 8 / 1056) / 2


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting cuz of keyboard interrupt")
        exit(69420)
