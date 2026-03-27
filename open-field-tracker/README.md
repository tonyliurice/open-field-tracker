# Open Field Tracker

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.placeholder.svg)](https://doi.org/10.5281/zenodo.placeholder)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🐭 **Open Field Tracker** - A Python toolkit for analyzing rat movement trajectories in open field tests, generating heatmaps, trajectory plots, and statistical reports.

## 📦 Installation

```bash
pip install open-field-tracker
```

Or install from source:

```bash
git clone https://github.com/tonyliurice/open-field-tracker.git
cd open-field-tracker
pip install -e .
```

## 🎯 Features

- **Trajectory Analysis**: Extract and smooth movement trajectories from video
- **Heatmap Generation**: Visualize spatial distribution of movement
- **Statistical Reports**: Distance, speed, and tracking rate metrics
- **Batch Processing**: Handle multiple videos efficiently
- **Unified Coordinates**: Map different video resolutions to standard reference frame

## 📖 Usage

```python
from open_field_tracker import TrajectoryAnalyzer

# Initialize analyzer
analyzer = TrajectoryAnalyzer(
    video_path="rat_video.mp4",
    output_dir="results/"
)

# Process video
analyzer.process()

# Generate visualizations
analyzer.plot_trajectory()
analyzer.plot_heatmap()
analyzer.plot_combined()

# Get statistics
stats = analyzer.get_statistics()
print(f"Total distance: {stats['total_distance']:.1f} pixels")
print(f"Average speed: {stats['average_speed']:.2f} pixels/frame")
```

See [examples/demo.ipynb](examples/demo.ipynb) for detailed tutorials.

## 📚 Academic Citation

If you use this tool in your research, please cite:

```bibtex
@software{liu_open_field_tracker_2026,
  author = {Liu, Tianyi},
  title = {Open Field Tracker: A Python toolkit for rat movement trajectory analysis},
  year = {2026},
  publisher = {Zenodo},
  version = {1.0.0},
  doi = {10.5281/zenodo.placeholder}
}
```

## 🔬 Research Applications

This tool has been used in studies involving:
- Behavioral neuroscience research
- Drug efficacy assessment
- Neurodegenerative disease models
- Stress and anxiety studies

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📧 Contact

- GitHub Issues: [https://github.com/tonyliurice/open-field-tracker/issues](https://github.com/tonyliurice/open-field-tracker/issues)
- ORCID: [0009-0004-2339-1945](https://orcid.org/0009-0004-2339-1945)

---

*Last updated: 2026-03-27*
