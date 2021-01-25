import time
import json

class Car:
    def __init__(self):
        self.battery = 100
        self.temperature = 20
        self.speed = 0
        self.total_distance = 0
        self.direction = [0, 1]
        self.location = [0, 0]
        self.last_update_time = time.time()
        self.speed_delta = 10
        
    def update(self):
        new_update_time = time.time()
        elapsed_time = new_update_time - self.last_update_time
        distance = elapsed_time * self.speed
        
        self.last_update_time = new_update_time
        self.total_distance += distance
        self.location[0] += self.direction[0] * distance
        self.location[1] += self.direction[1] * distance
        
    def get_data(self):
        self.update()
        return json.dumps(self.__dict__)
    
    def process_command(self, command):
        response = "OK"
        
        self.update()
        
        if command == "accelerate":
            self.speed += self.speed_delta
        elif command == "brake":
            self.speed = max(0, self.speed - self.speed_delta)
        elif command == "left":
            self.direction = [-self.direction[1], self.direction[0]]
        elif command == "right":
            self.direction = [self.direction[1], -self.direction[0]]
        else:
            response = "ERROR"

        return response
