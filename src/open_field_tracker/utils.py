"""
Utility functions for video processing and statistics.
"""

import cv2
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
from pathlib import Path


class VideoProcessor:
    """Utility class for video processing operations."""
    
    @staticmethod
    def get_video_properties(video_path: str) -> Dict[str, float]:
        """Get video properties (width, height, fps, frame count)."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        props = {
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS),
        }
        
        cap.release()
        return props


class StatisticsCalculator:
    """Utility class for calculating movement statistics."""
    
    @staticmethod
    def calculate_distance(trajectory: List[Tuple[float, float]]) -> float:
        """Calculate total distance traveled."""
        if len(trajectory) < 2:
            return 0.0
        
        points = np.array(trajectory)
        distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
        return float(np.sum(distances))
    
    @staticmethod
    def calculate_speeds(
        trajectory: List[Tuple[float, float]],
        frame_interval: int = 1,
    ) -> np.ndarray:
        """Calculate instantaneous speeds."""
        if len(trajectory) < 2:
            return np.array([])
        
        points = np.array(trajectory)
        distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
        speeds = distances / frame_interval
        
        return speeds
    
    @staticmethod
    def calculate_exploration_metrics(
        trajectory: List[Tuple[float, float]],
        arena_width: float,
        arena_height: float,
        n_zones: int = 4,
    ) -> Dict[str, float]:
        """
        Calculate exploration metrics (center time, peripheral time, etc.).
        
        Args:
            trajectory: List of (x, y) coordinates
            arena_width: Width of the arena
            arena_height: Height of the arena
            n_zones: Number of zones to divide the arena into
            
        Returns:
            Dictionary with exploration metrics
        """
        if not trajectory:
            return {
                'center_time_ratio': 0.0,
                'periphery_time_ratio': 0.0,
                'zone_transitions': 0,
            }
        
        points = np.array(trajectory)
        
        # Define center zone (inner 50% of arena)
        center_x_min, center_x_max = arena_width * 0.25, arena_width * 0.75
        center_y_min, center_y_max = arena_height * 0.25, arena_height * 0.75
        
        # Calculate time in center vs periphery
        in_center = (
            (points[:, 0] >= center_x_min) &
            (points[:, 0] <= center_x_max) &
            (points[:, 1] >= center_y_min) &
            (points[:, 1] <= center_y_max)
        )
        
        center_time_ratio = np.sum(in_center) / len(points)
        periphery_time_ratio = 1 - center_time_ratio
        
        # Calculate zone transitions
        zone_size_x = arena_width / n_zones
        zone_size_y = arena_height / n_zones
        
        zones_x = (points[:, 0] / zone_size_x).astype(int)
        zones_y = (points[:, 1] / zone_size_y).astype(int)
        
        zone_changes = np.sum(
            (np.diff(zones_x) != 0) | (np.diff(zones_y) != 0)
        )
        
        return {
            'center_time_ratio': float(center_time_ratio),
            'periphery_time_ratio': float(periphery_time_ratio),
            'zone_transitions': int(zone_changes),
        }
