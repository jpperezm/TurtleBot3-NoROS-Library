try:
    from controller import Robot
except ImportError:
    from robot_wrapper import init_robot as Robot
import math

def move_forward(robot, distance_to_travel, max_speed, timestep):
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
    
    wheel_radius = 0.066 / 2
    wheel_circumference = 2 * 3.14 * wheel_radius
    encoder_unit = wheel_circumference / 6.28
    
    ps_values = [0, 0]
    dist_values = [0, 0]
    
    while robot.step(timestep) != -1:
        ps_values[0] = left_position_sensor.getValue()
        ps_values[1] = right_position_sensor.getValue()
        
        for i in range(2):
            dist_values[i] = ps_values[i] * encoder_unit
        
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(max_speed)
        
        if dist_values[0] >= distance_to_travel:
            left_motor.setVelocity(0.0)
        if dist_values[1] >= distance_to_travel:
            right_motor.setVelocity(0.0)
        
        if dist_values[0] >= distance_to_travel and dist_values[1] >= distance_to_travel:
            break

def turn(robot, angle_in_degrees, max_speed, timestep):
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
    
    target_angle = angle_in_degrees * (math.pi / 180)  # Convert degrees to radians
    current_angle = 0.0
    
    while robot.step(timestep) != -1:
        gyro_values = gyro.getValues()
        current_angular_velocity = gyro_values[2]  # Assuming Z-axis rotation
        current_angle += current_angular_velocity * (timestep / 1000.0)  # timestep in ms, convert to seconds
        print("Angle turned: ", current_angle)
   
        if angle_in_degrees > 0:
            left_motor.setVelocity(-max_speed * 0.5)
            right_motor.setVelocity(max_speed * 0.5)
        else:
            left_motor.setVelocity(max_speed * 0.5)
            right_motor.setVelocity(-max_speed * 0.5)
        
        if abs(current_angle) >= abs(target_angle):
            left_motor.setVelocity(0.0)
            right_motor.setVelocity(0.0)
            break

def avoid_obstacles(robot, max_speed, timestep):
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
    
    safe_distance = 0.2
    
    while robot.step(timestep) != -1:
        range_image = lidar.getRangeImage()
        front_range_image = range_image[135:225]
        min_distance = min(front_range_image)
        minpos = front_range_image.index(min(front_range_image))
        front_value = range_image[180]
        #print("Min Distance index:")
        #print(minpos)
        #print("Min Distance:")
        #print(min_distance)
        #print(front_value)
        if min_distance < safe_distance:
            obstacle_direction = front_range_image.index(min_distance)
            if obstacle_direction < len(front_range_image) / 2:
                # Obstacle is on the left, turn right 90 degrees
                turn(robot, -90, max_speed, timestep)
            else:
                # Obstacle is on the right, turn left 90 degrees
                turn(robot, 90, max_speed, timestep)
        else:
            left_motor.setVelocity(max_speed)
            right_motor.setVelocity(max_speed)

def run_robot(robot):
    timestep = 16
    max_speed = 2.5
    
    move_forward(robot, 0.40, max_speed, timestep)
    turn(robot, 90, max_speed, timestep)
    avoid_obstacles(robot, max_speed, timestep)

if __name__ == "__main__":
    robot = Robot()
    run_robot(robot)