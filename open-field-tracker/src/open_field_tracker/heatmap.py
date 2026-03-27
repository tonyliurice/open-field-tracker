"""
Heatmap and visualization generation module.

This module provides tools for generating heatmaps, trajectory plots,
and combined visualizations from movement data.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Optional
from pathlib import Path


class HeatmapGenerator:
    """
    Generator for heatmaps and trajectory visualizations.
    
    This class creates publication-quality visualizations including:
    - Trajectory plots showing movement paths
    - Heatmaps showing spatial distribution
    - Combined plots with both trajectory and heatmap
    
    Attributes:
        width (int): Plot width in pixels (reference coordinate system)
        height (int): Plot height in pixels (reference coordinate system)
        title (str): Plot title
        dpi (int): Resolution for output images (default: 300)
        
    Example:
        >>> generator = HeatmapGenerator(width=854, height=480)
        >>> generator.plot_trajectory(trajectory, "output.png")
        >>> generator.plot_heatmap(trajectory, "heatmap.png")
    """
    
    def __init__(
        self,
        width: int = 854,
        height: int = 480,
        title: str = "Rat Movement Analysis",
        dpi: int = 300,
    ):
        """
        Initialize the HeatmapGenerator.
        
        Args:
            width: Plot width in pixels (default: 854)
            height: Plot height in pixels (default: 480)
            title: Plot title (default: "Rat Movement Analysis")
            dpi: Resolution for output images (default: 300)
        """
        self.width = width
        self.height = height
        self.title = title
        self.dpi = dpi
        
        # Set default style
        plt.style.use('seaborn-v0_8-whitegrid')
        
    def plot_trajectory(
        self,
        trajectory: List[Tuple[float, float]],
        save_path: str,
        show_start_end: bool = True,
    ) -> None:
        """
        Generate a trajectory plot.
        
        Args:
            trajectory: List of (x, y) coordinate tuples
            save_path: Path to save the plot
            show_start_end: Whether to mark start and end points
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Extract coordinates
        x_coords = [p[0] for p in trajectory]
        y_coords = [p[1] for p in trajectory]
        
        # Plot trajectory with gradient color
        points = np.array([x_coords, y_coords]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        from matplotlib.collections import LineCollection
        lc = LineCollection(
            segments,
            cmap='viridis',
            norm=plt.Normalize(0, len(trajectory)),
            linewidths=2,
        )
        lc.set_array(np.arange(len(trajectory)))
        ax.add_collection(lc)
        
        # Mark start and end
        if show_start_end and len(trajectory) > 0:
            ax.plot(x_coords[0], y_coords[0], 'go', markersize=10, label='Start')
            ax.plot(x_coords[-1], y_coords[-1], 'ro', markersize=10, label='End')
            ax.legend()
        
        # Set limits and labels
        ax.set_xlim(0, self.width)
        ax.set_ylim(self.height, 0)  # Invert y-axis
        ax.set_xlabel('X Position (pixels)', fontsize=12)
        ax.set_ylabel('Y Position (pixels)', fontsize=12)
        ax.set_title(self.title, fontsize=14, fontweight='bold')
        
        # Equal aspect ratio
        ax.set_aspect('equal')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
    def plot_heatmap(
        self,
        trajectory: List[Tuple[float, float]],
        save_path: str,
        bins: int = 50,
        sigma: float = 1.0,
    ) -> None:
        """
        Generate a heatmap showing spatial distribution.
        
        Args:
            trajectory: List of (x, y) coordinate tuples
            save_path: Path to save the heatmap
            bins: Number of bins for histogram (default: 50)
            sigma: Gaussian smoothing sigma (default: 1.0)
        """
        fig, ax = plt.subplots(figsize=(11, 8))
        
        # Extract coordinates
        x_coords = [p[0] for p in trajectory]
        y_coords = [p[1] for p in trajectory]
        
        # Create 2D histogram
        heatmap, xedges, yedges = np.histogram2d(
            x_coords, y_coords,
            bins=bins,
            range=[[0, self.width], [0, self.height]]
        )
        
        # Apply Gaussian smoothing
        from scipy.ndimage import gaussian_filter
        heatmap = gaussian_filter(heatmap, sigma=sigma)
        
        # Plot heatmap
        extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]]
        im = ax.imshow(
            heatmap.T,
            extent=extent,
            origin='upper',
            cmap='hot',
            aspect='auto',
        )
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Time Spent', fontsize=12)
        
        # Labels
        ax.set_xlabel('X Position (pixels)', fontsize=12)
        ax.set_ylabel('Y Position (pixels)', fontsize=12)
        ax.set_title(f"{self.title} - Heatmap", fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
    def plot_combined(
        self,
        trajectory: List[Tuple[float, float]],
        save_path: str,
        bins: int = 50,
        alpha: float = 0.6,
    ) -> None:
        """
        Generate a combined plot with both trajectory and heatmap.
        
        Args:
            trajectory: List of (x, y) coordinate tuples
            save_path: Path to save the plot
            bins: Number of bins for heatmap (default: 50)
            alpha: Transparency for heatmap (default: 0.6)
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Extract coordinates
        x_coords = [p[0] for p in trajectory]
        y_coords = [p[1] for p in trajectory]
        
        # Create heatmap (background)
        heatmap, xedges, yedges = np.histogram2d(
            x_coords, y_coords,
            bins=bins,
            range=[[0, self.width], [0, self.height]]
        )
        
        from scipy.ndimage import gaussian_filter
        heatmap = gaussian_filter(heatmap, sigma=1.0)
        
        extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]]
        ax.imshow(
            heatmap.T,
            extent=extent,
            origin='upper',
            cmap='hot',
            aspect='auto',
            alpha=alpha,
        )
        
        # Plot trajectory (overlay)
        points = np.array([x_coords, y_coords]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        from matplotlib.collections import LineCollection
        lc = LineCollection(
            segments,
            cmap='viridis',
            norm=plt.Normalize(0, len(trajectory)),
            linewidths=2,
        )
        lc.set_array(np.arange(len(trajectory)))
        ax.add_collection(lc)
        
        # Mark start and end
        if len(trajectory) > 0:
            ax.plot(x_coords[0], y_coords[0], 'go', markersize=12, 
                   markeredgecolor='white', markeredgewidth=2, label='Start')
            ax.plot(x_coords[-1], y_coords[-1], 'ro', markersize=12,
                   markeredgecolor='white', markeredgewidth=2, label='End')
            ax.legend(loc='upper right')
        
        # Labels
        ax.set_xlim(0, self.width)
        ax.set_ylim(self.height, 0)
        ax.set_xlabel('X Position (pixels)', fontsize=12)
        ax.set_ylabel('Y Position (pixels)', fontsize=12)
        ax.set_title(f"{self.title} - Combined View", fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
