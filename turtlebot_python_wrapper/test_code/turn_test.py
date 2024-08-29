try:
    from controller import Robot
except ImportError:
    from robot_wrapper import init_robot as Robot
import time

def turn_90_degrees(robot, max_speed, timestep):
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    
    # Set the motors to velocity control mode
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    
    # Enable the gyroscope
    gyro = robot.getDevice('gyro')
    gyro.enable(timestep)
    
    target_angle = 90 * (3.14 / 180)  # Convert 90 degrees to radians
    current_angle = 0.0
    initial_time = time.time()
    
    while robot.step(timestep) != -1:
        gyro_values = gyro.getValues()
        current_angular_velocity = gyro_values[2]  # Assuming Z-axis rotation
        current_time = time.time()
        elapsed_time = current_time - initial_time
        current_angle += current_angular_velocity * elapsed_time
        initial_time = current_time
        
        left_motor.setVelocity(-max_speed * 0.5)
        right_motor.setVelocity(max_speed * 0.5)
        
        if abs(current_angle) >= abs(target_angle):
            left_motor.setVelocity(0.0)
            right_motor.setVelocity(0.0)
            break

def run_robot(robot):
    timestep = 16
    max_speed = 3
    
    turn_90_degrees(robot, max_speed, timestep)
    print("The robot has turned 90 degrees.")

if __name__ == "__main__":
    robot = Robot()
    run_robot(robot)
