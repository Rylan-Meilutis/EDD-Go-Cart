import ctre


def main():
    pot_range = 10000
    brake_actuator = ctre.TalonSRX(3)
    left_falcon = ctre.TalonFX(1)
    right_falcon = ctre.TalonFX(2)

    brake_actuator.configSelectedFeedbackSensor(FeedbackDevice.Analog, 0)

    while True:
        pot_pos = brake_actuator.getSelectedSensorPosition()
        if pot_pos > 10:
            left_falcon.set(ctre.TalonFXControlMode.PercentOutput, pot_pos/pot_range)
            right_falcon.set(ctre.TalonFXControlMode.PercentOutput, pot_pos/pot_range)
            brake_actuator.set(ctre.TalonSRXControlMode.PercentOutput, 0)
        elif pot_pos < -10:
            left_falcon.set(ctre.TalonFXControlMode.PercentOutput, 0)
            right_falcon.set(ctre.TalonFXControlMode.PercentOutput, 0)
            brake_actuator.set(ctre.TalonSRXControlMode.PercentOutput, pot_pos/pot_range)


if __name__ == "main":
    main()
