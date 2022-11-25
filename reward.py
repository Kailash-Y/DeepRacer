
import math

def reward_function(params):
    '''
    Example of penalize steering, which helps mitigate zig-zag behaviors
    '''
    
    
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    track_width = params['track_width']
    
    reward = 1e-3
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward = 1.0
        # Distance from center reward
        if distance_from_center <= 0.1 * track_width:
            reward = 1.0
        elif distance_from_center <= 0.25 * track_width:
            reward = 0.5
        elif distance_from_center <= 0.5 * track_width:
            reward = 0.1
        else:
            return float(1e-3)

        # Steering Angle Reward
        ABS_STEERING_THRESHOLD = 20 
        abs_steering = abs(params['steering_angle'])
        if abs_steering > ABS_STEERING_THRESHOLD:
            reward *= 0.8

        # Direction Reward
        waypoints = params['waypoints']
        closest_waypoints = params['closest_waypoints']
        heading = params['heading']
        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]
        track_direction = math.degrees(math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]))
        direction_diff = abs(track_direction - heading)
        if direction_diff > 180:
            direction_diff = 360 - direction_diff
        DIRECTION_THRESHOLD = 10.0
        if direction_diff > DIRECTION_THRESHOLD:
            reward *= 0.5

        # Progress Reward
        steps = params['steps']
        progress = params['progress']
        TOTAL_NUM_STEPS = 500
        if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
            reward += 10.0

        # Speed Reward
        reward *= params['speed']

    return float(reward)
