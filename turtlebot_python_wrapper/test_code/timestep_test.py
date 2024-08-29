try:
    from controller import Robot
except ImportError:
    from robot_wrapper import init_robot as Robot
import time

def run_robot(robot):
    timestep = 64
    max_speed = 3
    move_duration = 4.0  # Move forward for 5 seconds
    
    # Get the motor devices
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    
    # Set the motors to velocity control mode
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    
    # Main loop:
    start_time = time.time()
    while robot.step(timestep) != -1:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if elapsed_time >= move_duration:
            break
        
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(max_speed)
    
    # Print the total time the robot moved
    total_time = time.time() - start_time
    print(f"The robot moved for {total_time:.2f} seconds.")

    # Stop the motors after moving
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)


if __name__ == "__main__":
    # Create the Robot instance
    robot = Robot()
    run_robot(robot)
