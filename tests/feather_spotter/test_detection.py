"""Implements tests for Feather Spotter Detection module."""
import torch

from feather_spotter.detection import parse_detections


def test_parse_detections() -> None:
    """Tests parse_detections function."""
    boxes = [
        torch.tensor([[0.0, 1.0, 2.0, 3.0, 0.9, 0.0]]),
        torch.tensor([[4.0, 5.0, 6.0, 7.0, 0.8, 1.0]]),
    ]
    names = {0: "mock_0", 1: "mock_1"}
    detections = parse_detections(boxes, names)
    assert len(detections) == 2
    assert detections[0].name == "mock_0"
    assert detections[0].confidence == 90.0
    assert detections[0].index == 0
    assert detections[0].box == (0, 1, 2, 3)
    assert detections[1].name == "mock_1"
    assert detections[1].confidence == 80.0
    assert detections[1].index == 1
    assert detections[1].box == (4, 5, 6, 7)
