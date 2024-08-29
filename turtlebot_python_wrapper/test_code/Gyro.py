try:
    from controller import Robot
except ImportError:
    from robot_wrapper import init_robot as Robot
    
def run_robot(robot):
    timestep = 16
    max_speed = 6.67
    rotation_speed = 1.0
    
    # Get the motor devices
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    
    # Set the motors to velocity control mode
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    
    # Get the IMU devices
    accelerometer = robot.getDevice('accelerometer')
    gyro = robot.getDevice('gyro')
    
    # Enable the IMU devices (if necessary)
    accelerometer.enable(timestep)
    gyro.enable(timestep)

    # Set the initial motor speeds for rotation
    left_motor.setVelocity(rotation_speed)
    right_motor.setVelocity(-rotation_speed)
    
    # Main loop
    time_elapsed = 0
    while robot.step(timestep) != -1:
        # Read the gyroscope values
        gyro_values = gyro.getValues()
        time_elapsed += timestep / 1000.0
        print(f"Time: {time_elapsed:.2f} s, Gyroscope values: X: {gyro_values[0]:.5f}, Y: {gyro_values[1]:.5f}, Z: {gyro_values[2]:.5f}")
    
        # Stop the loop after a certain condition (for example, after 10 seconds, this only works in webots)
        if time_elapsed > 10.0:
            break
    
    # Stop the robot's motion
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)
    

if __name__ == "__main__":
    robot = Robot()
    run_robot(robot)