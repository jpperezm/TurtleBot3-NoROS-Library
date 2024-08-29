try:
    from controller import Robot, Accelerometer, Gyro
except ImportError:
    from robot_wrapper import init_robot as Robot

def run_robot(robot):
    timestep = 64
    max_speed = 6.67
    distance_to_travel = 0.25
    rotation_speed = 1.0
    safe_distance = 0.35
    
    # Get the motor devices
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    
    # Set the motors to velocity control mode
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    
    # LIDAR
    lidar = robot.getDevice('LDS-01')
    lidar.enable(timestep)
    # lidar.enablePointCloud()
    

    while robot.step(timestep) != -1:
        range_image = lidar.getRangeImage()
        print("{}".format(range_image))
        
        front_range_image = range_image[135:225]
        
        min_distance = min(front_range_image)
        
        # If an obstacle is detected within the safe distance, turn the robot
        if min_distance < safe_distance:
            # Determine the direction to turn based on the obstacle position
            obstacle_direction = front_range_image.index(min_distance)
            if obstacle_direction < len(front_range_image) / 2:
                # Obstacle is on the left, turn right
                left_motor.setVelocity(max_speed * 0.5)
                right_motor.setVelocity(-max_speed * 0.5)
            else:
                # Obstacle is on the right, turn left
                left_motor.setVelocity(-max_speed * 0.5)
                right_motor.setVelocity(max_speed * 0.5)
        else:
            # No obstacle, move forward
            left_motor.setVelocity(max_speed * 0.5)
            right_motor.setVelocity(max_speed * 0.5)

if __name__ == "__main__":
    # Create the Robot instance
    robot = Robot()
    run_robot(robot)
