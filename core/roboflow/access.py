from inference_sdk import InferenceHTTPClient

from core.roboflow.initialization import RoboflowClient


# Получение клиента Roboflow
async def get_roboflow() -> InferenceHTTPClient:
    return RoboflowClient.get_roboflow()
