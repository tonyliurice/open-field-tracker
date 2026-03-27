# 旷场实验分析助手

🐭 **基于 Open Field Tracker 的智能分析工具**

## 功能

- 分析大鼠旷场实验视频
- 自动生成运动轨迹图
- 生成热力图显示停留区域
- 输出统计数据（总距离、速度等）

## 学术引用

如果您在论文中使用此工具，请引用：

```bibtex
@software{liu_open_field_tracker_2026,
  author = {Liu, Tianyi},
  title = {Open Field Tracker},
  year = {2026},
  publisher = {Zenodo},
  version = {1.0.0},
  doi = {10.5281/zenodo.placeholder}
}
```

## 使用方法

1. 上传视频文件（MP4/AVI/MOV 格式）
2. 系统自动分析运动轨迹
3. 下载生成的图表和统计数据

## 输出文件

- `trajectory_plot.png` - 运动轨迹图
- `trajectory_heatmap.png` - 热力图
- `trajectory_combined.png` - 组合图
- `trajectory_processed.csv` - 轨迹数据（CSV格式）

## 技术说明

本 Skill 基于开源 Python 包 Open Field Tracker 构建：
- GitHub: https://github.com/tonyliurice/open-field-tracker
- 文档: 详见 GitHub README

## 作者

- Tianyi Liu
- ORCID: 0009-0004-2339-1945
