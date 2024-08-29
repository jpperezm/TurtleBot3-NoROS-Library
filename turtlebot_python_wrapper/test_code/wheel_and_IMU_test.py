try:
    from controller import Robot, Accelerometer, Gyro
except ImportError:
    from robot_wrapper import init_robot as Robot

def run_robot(robot):
    timestep = 64
    max_speed = 6.67
    distance_to_travel = 0.25
    rotation_speed = 1.0
    
    # Get the motor devices
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    
    # Set the motors to velocity control mode
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    
    # Enable the position sensors
    left_position_sensor = robot.getDevice('left wheel sensor')
    left_position_sensor.enable(timestep)
    right_position_sensor = robot.getDevice('right wheel sensor')
    right_position_sensor.enable(timestep)
    
    # Enable the IMU devices
    accelerometer = robot.getDevice('accelerometer')
    gyro = robot.getDevice('gyro')
    accelerometer.enable(timestep)
    gyro.enable(timestep)
    
    ps_values = [0, 0]
    dist_values = [0, 0]
    wheel_radius = 0.066 / 2
    wheel_circumference = 2 * 3.14 * wheel_radius
    encoder_unit = wheel_circumference / 6.28

    # Move forward 25 cm
    while robot.step(timestep) != -1:
        ps_values[0] = left_position_sensor.getValue()
        ps_values[1] = right_position_sensor.getValue()
        
        for i in range(2):
            dist_values[i] = ps_values[i] * encoder_unit
        
        accelerometer_values = accelerometer.getValues()
        print(f"Accelerometer values: x={accelerometer_values[0]:.2f}, y={accelerometer_values[1]:.2f}, z={accelerometer_values[2]:.2f}")
        print(f"Distance values: left={dist_values[0]:.2f}, right={dist_values[1]:.2f}")
        
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(max_speed)
        
        if dist_values[0] >= distance_to_travel:
            left_motor.setVelocity(0.0)
        
        if dist_values[1] >= distance_to_travel:
            right_motor.setVelocity(0.0)
        
        if dist_values[0] >= distance_to_travel and dist_values[1] >= distance_to_travel:
            break

    # Wait for a moment before starting the next test
    for _ in range(20):
        robot.step(timestep)

    # Rotate in circles and print gyroscope values
    left_motor.setVelocity(rotation_speed)
    right_motor.setVelocity(-rotation_speed)
    time_elapsed = 0
    while robot.step(timestep) != -1:
        gyro_values = gyro.getValues()
        time_elapsed += timestep / 1000.0
        print(f"Time: {time_elapsed:.2f} s, Gyroscope values: X: {gyro_values[0]:.5f}, Y: {gyro_values[1]:.5f}, Z: {gyro_values[2]:.5f}")
    
        if time_elapsed > 10.0:
            break

    # Stop the robot's motion
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)

if __name__ == "__main__":
    # Create the Robot instance
    robot = Robot()
    run_robot(robot)

