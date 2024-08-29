try:
    from controller import Robot
except ImportError:
    from robot_wrapper import init_robot as Robot

def run_robot(robot):
    timestep = 64
    max_speed = 6.67/2
    distance_to_travel = 0.25
    
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
    
    ps_values = [0, 0]
    dist_values = [0, 0]
    
    wheel_radius = 0.066 / 2
    wheel_circumference = 2 * 3.14 * wheel_radius
    encoder_unit = wheel_circumference / 6.28
    
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        ps_values[0] = left_position_sensor.getValue()
        ps_values[1] = right_position_sensor.getValue()
        
        print("-------------------------")
        print("position sensor values: {} {}".format(ps_values[0], ps_values[1]))
        
        for i in range(2):
            dist_values[i] = ps_values[i] * encoder_unit
        
        print("distance values: {} {}".format(dist_values[0], dist_values[1]))
        
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(max_speed)
        
        if dist_values[0] >= distance_to_travel:
            left_motor.setVelocity(0.0)
            
        if dist_values[1] >= distance_to_travel:
            right_motor.setVelocity(0.0)
            
        if dist_values[0] >= distance_to_travel and dist_values[1] >= distance_to_travel:
            break
        
if __name__ == "__main__":

    # create the Robot instance.
    robot = Robot()
    run_robot(robot)