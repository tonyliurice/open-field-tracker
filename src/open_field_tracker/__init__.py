"""
Open Field Tracker - A Python toolkit for rat movement trajectory analysis.

This package provides tools for analyzing rat movement trajectories in open field tests,
generating heatmaps, trajectory plots, and statistical reports.

Academic Citation:
    Liu, T. (2026). Open Field Tracker: A Python toolkit for rat movement 
    trajectory analysis. Zenodo. https://doi.org/10.5281/zenodo.placeholder

Example:
    >>> from open_field_tracker import TrajectoryAnalyzer
    >>> analyzer = TrajectoryAnalyzer("video.mp4")
    >>> analyzer.process()
    >>> analyzer.plot_heatmap()

License:
    MIT License - See LICENSE file for details.

Author:
    Tianyi Liu (ORCID: 0009-0004-2339-1945)

Version:
    1.0.0
"""

__version__ = "1.0.0"
__author__ = "Tianyi Liu"
__email__ = "liutianyi@example.com"
__license__ = "MIT"
__url__ = "https://github.com/tonyliurice/open-field-tracker"
__doi__ = "10.5281/zenodo.placeholder"

from .trajectory import TrajectoryAnalyzer
from .heatmap import HeatmapGenerator
from .utils import VideoProcessor, StatisticsCalculator

__all__ = [
    "TrajectoryAnalyzer",
    "HeatmapGenerator", 
    "VideoProcessor",
    "StatisticsCalculator",
]
