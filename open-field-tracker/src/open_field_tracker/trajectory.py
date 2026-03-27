"""
Trajectory analysis module for rat movement tracking.

This module provides the core functionality for extracting, processing,
and analyzing rat movement trajectories from video files.
"""

import cv2
import numpy as np
import pandas as pd
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path
from scipy.ndimage import gaussian_filter1d


class TrajectoryAnalyzer:
    """
    Main class for analyzing rat movement trajectories.
    
    This class provides a complete pipeline for:
    1. Video processing and object tracking
    2. Trajectory smoothing and filtering
    3. Coordinate normalization
    4. Statistical analysis
    5. Visualization generation
    
    Attributes:
        video_path (Path): Path to the input video file
        output_dir (Path): Directory for saving results
        width (int): Video width in pixels
        height (int): Video height in pixels
        fps (float): Video frame rate
        
    Example:
        >>> analyzer = TrajectoryAnalyzer("rat_video.mp4", output_dir="results/")
        >>> analyzer.process()
        >>> stats = analyzer.get_statistics()
        >>> print(f"Total distance: {stats['total_distance']:.1f} pixels")
    """
    
    def __init__(
        self,
        video_path: str,
        output_dir: Optional[str] = None,
        reference_width: int = 854,
        reference_height: int = 480,
        max_jump: int = 150,
        skip_frames: int = 6,
    ):
        """
        Initialize the TrajectoryAnalyzer.
        
        Args:
            video_path: Path to the input video file
            output_dir: Directory for saving results (default: video_name_output/)
            reference_width: Reference width for coordinate normalization (default: 854)
            reference_height: Reference height for coordinate normalization (default: 480)
            max_jump: Maximum allowed jump distance between frames (default: 150)
            skip_frames: Process every Nth frame (default: 6)
        """
        self.video_path = Path(video_path)
        self.reference_width = reference_width
        self.reference_height = reference_height
        self.max_jump = max_jump
        self.skip_frames = skip_frames
        
        # Set output directory
        if output_dir is None:
            self.output_dir = self.video_path.parent / f"{self.video_path.stem}_output"
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize video properties
        self._load_video_properties()
        
        # Initialize trajectory storage
        self.raw_trajectory: List[Tuple[float, float]] = []
        self.filtered_trajectory: List[Tuple[float, float]] = []
        self.normalized_trajectory: List[Tuple[float, float]] = []
        
    def _load_video_properties(self) -> None:
        """Load video properties using OpenCV."""
        cap = cv2.VideoCapture(str(self.video_path))
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {self.video_path}")
        
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        cap.release()
        
    def process(self) -> "TrajectoryAnalyzer":
        """
        Process the video and extract trajectory.
        
        This method runs the complete processing pipeline:
        1. Track object in video
        2. Filter outliers
        3. Smooth trajectory
        4. Normalize coordinates
        5. Save results
        
        Returns:
            self for method chaining
        """
        # Step 1: Track object
        self._track_object()
        
        # Step 2: Filter and smooth
        self._filter_trajectory()
        self._smooth_trajectory()
        
        # Step 3: Normalize coordinates
        self._normalize_coordinates()
        
        # Step 4: Save results
        self._save_trajectory()
        
        return self
        
    def _track_object(self) -> None:
        """
        Track object in video using background subtraction.
        
        Note: This is a simplified implementation. In production,
        you would use more sophisticated tracking algorithms.
        """
        # Placeholder for actual tracking implementation
        # This would integrate with the actual tracking code
        pass
        
    def _filter_trajectory(self) -> None:
        """Filter outliers using median filtering."""
        if len(self.raw_trajectory) < 5:
            self.filtered_trajectory = self.raw_trajectory
            return
            
        # Median filter for outlier removal
        points = np.array(self.raw_trajectory)
        filtered_points = []
        
        window_size = 5
        for i in range(len(points)):
            start = max(0, i - window_size // 2)
            end = min(len(points), i + window_size // 2 + 1)
            window = points[start:end]
            
            median = np.median(window, axis=0)
            dist = np.linalg.norm(points[i] - median)
            
            if dist < self.max_jump:
                filtered_points.append(tuple(points[i]))
            else:
                filtered_points.append(tuple(median))
                
        self.filtered_trajectory = filtered_points
        
    def _smooth_trajectory(self) -> None:
        """Apply Gaussian smoothing to trajectory."""
        if len(self.filtered_trajectory) < 3:
            return
            
        points = np.array(self.filtered_trajectory)
        x_smooth = gaussian_filter1d(points[:, 0], sigma=1.0)
        y_smooth = gaussian_filter1d(points[:, 1], sigma=1.0)
        
        self.filtered_trajectory = list(zip(x_smooth, y_smooth))
        
    def _normalize_coordinates(self) -> None:
        """Normalize coordinates to reference frame."""
        scale_x = self.reference_width / self.width
        scale_y = self.reference_height / self.height
        
        self.normalized_trajectory = [
            (x * scale_x, y * scale_y)
            for x, y in self.filtered_trajectory
        ]
        
    def _save_trajectory(self) -> None:
        """Save trajectory data to CSV."""
        df = pd.DataFrame(
            self.normalized_trajectory,
            columns=['x', 'y']
        )
        df['frame'] = range(len(df))
        df = df[['frame', 'x', 'y']]
        
        output_path = self.output_dir / "trajectory_processed.csv"
        df.to_csv(output_path, index=False)
        
    def get_statistics(self) -> Dict[str, float]:
        """
        Calculate movement statistics.
        
        Returns:
            Dictionary containing:
            - total_distance: Total movement distance in pixels
            - average_speed: Average speed in pixels/frame
            - max_speed: Maximum speed in pixels/frame
            - tracking_rate: Percentage of frames successfully tracked
        """
        if len(self.normalized_trajectory) < 2:
            return {
                'total_distance': 0.0,
                'average_speed': 0.0,
                'max_speed': 0.0,
                'tracking_rate': 0.0,
            }
            
        points = np.array(self.normalized_trajectory)
        
        # Calculate distances
        distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
        total_distance = np.sum(distances)
        
        # Calculate speeds
        speeds = distances / self.skip_frames
        average_speed = np.mean(speeds)
        max_speed = np.max(speeds)
        
        # Calculate tracking rate
        expected_frames = self.total_frames // self.skip_frames
        tracking_rate = len(self.normalized_trajectory) / expected_frames * 100
        
        return {
            'total_distance': float(total_distance),
            'average_speed': float(average_speed),
            'max_speed': float(max_speed),
            'tracking_rate': float(tracking_rate),
        }
        
    def plot_trajectory(self, save_path: Optional[str] = None) -> None:
        """
        Generate trajectory plot.
        
        Args:
            save_path: Path to save the plot (default: output_dir/trajectory_plot.png)
        """
        from .heatmap import HeatmapGenerator
        
        generator = HeatmapGenerator(
            width=self.reference_width,
            height=self.reference_height,
            title="Rat Movement Trajectory"
        )
        
        if save_path is None:
            save_path = self.output_dir / "trajectory_plot.png"
            
        generator.plot_trajectory(self.normalized_trajectory, str(save_path))
        
    def plot_heatmap(self, save_path: Optional[str] = None) -> None:
        """
        Generate heatmap.
        
        Args:
            save_path: Path to save the heatmap (default: output_dir/trajectory_heatmap.png)
        """
        from .heatmap import HeatmapGenerator
        
        generator = HeatmapGenerator(
            width=self.reference_width,
            height=self.reference_height,
            title="Rat Movement Heatmap"
        )
        
        if save_path is None:
            save_path = self.output_dir / "trajectory_heatmap.png"
            
        generator.plot_heatmap(self.normalized_trajectory, str(save_path))
        
    def plot_combined(self, save_path: Optional[str] = None) -> None:
        """
        Generate combined trajectory + heatmap plot.
        
        Args:
            save_path: Path to save the plot (default: output_dir/trajectory_combined.png)
        """
        from .heatmap import HeatmapGenerator
        
        generator = HeatmapGenerator(
            width=self.reference_width,
            height=self.reference_height,
            title="Rat Movement Analysis"
        )
        
        if save_path is None:
            save_path = self.output_dir / "trajectory_combined.png"
            
        generator.plot_combined(self.normalized_trajectory, str(save_path))
