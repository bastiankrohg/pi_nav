import numpy as np
import grpc
from telemetry_proto.telemetry_pb2 import NavigationUpdate, Position, Empty
from telemetry_proto.telemetry_pb2_grpc import TelemetryStub

class PathFollower:
    # Initialize with gRPC channel
    def __init__(self, path, look_ahead_distance=2.0, grid_size=(50, 50), grpc_channel=None):
        self.path = path
        self.current_position = path[0]
        self.traveled_path = []
        self.obstacles = []  # Populate with detected obstacles
        self.grpc_client = TelemetryStub(grpc_channel) if grpc_channel else None

    def send_update(self):
        if self.grpc_client:
            update = NavigationUpdate(
                current_position=list(self.current_position),
                traveled_path=[Position(x=p[0], y=p[1]) for p in self.traveled_path],
                path=[Position(x=p[0], y=p[1]) for p in self.path],
                obstacles=[Position(x=o[0], y=o[1]) for o in self.obstacles]
            )
            self.grpc_client.SendUpdate(update)

    def move_with_pure_pursuit_obstacle_avoidance(self, speed=1.0, pause=0.1):
        # Example navigation loop with gRPC telemetry
        for waypoint in self.path:
            while True:
                direction = waypoint - self.current_position
                if np.linalg.norm(direction) < 0.5:
                    self.traveled_path.append(self.current_position)
                    self.send_update()  # Send updates after each step
                    break
                self.current_position += direction / np.linalg.norm(direction) * speed
                self.send_update()