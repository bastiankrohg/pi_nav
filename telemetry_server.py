import time
import grpc
from concurrent import futures
from telemetry_proto.telemetry_pb2 import TelemetryData, Resource
from telemetry_proto import telemetry_pb2_grpc


class TelemetryServiceServicer(telemetry_pb2_grpc.TelemetryServiceServicer):
    def StreamTelemetry(self, request, context):
        """
        Streams telemetry data to the client.
        """
        print("Client connected. Streaming telemetry data...")

        while True:
            # Mock data generation
            data = TelemetryData(
                ultrasound_distance=1.2,  # Example value in meters
                odometer=10.5,  # Total distance traveled in meters
                current_position="x: 12.3, y: -7.4",
                heading=45.0,  # Heading in degrees
                search_mode="Pattern Pursuit",
                battery_status="85%",
                resources_found=[
                    Resource(type="rock", x_coordinate=15.0, y_coordinate=-3.0),
                    Resource(type="water", x_coordinate=10.0, y_coordinate=5.0),
                ],
            )
            yield data
            time.sleep(1)  # Adjust streaming rate as necessary


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    telemetry_pb2_grpc.add_TelemetryServiceServicer_to_server(TelemetryServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("Telemetry server started on port 50051.")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()