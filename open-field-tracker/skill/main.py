"""
Open Field Tracker Skill - Main entry point for Kimi integration.

This Skill provides a conversational interface for analyzing rat movement
trajectories without requiring Python programming knowledge.

Academic Reference:
    Liu, T. (2026). Open Field Tracker. Zenodo. 
    DOI: 10.5281/zenodo.placeholder
"""

import sys
import os

# Add parent src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from open_field_tracker import TrajectoryAnalyzer


def main():
    """Main entry point for the Skill."""
    print("🐭 旷场实验分析助手已启动")
    print("基于 Open Field Tracker v1.0.0")
    print("学术引用：DOI: 10.5281/zenodo.placeholder")
    print()
    print("功能：")
    print("1. 分析视频文件，提取运动轨迹")
    print("2. 生成轨迹图、热力图、组合图")
    print("3. 输出统计数据（总距离、平均速度等）")
    print()
    print("使用方法：")
    print('- 上传视频文件，说"分析这个视频"')
    print('- 或提供视频路径，如：/path/to/rat_video.mp4')
    print()


def analyze_video(video_path: str, output_dir: str = None):
    """
    Analyze a video file and generate reports.
    
    Args:
        video_path: Path to the video file
        output_dir: Directory for saving results
        
    Returns:
        Dictionary with results and statistics
    """
    print(f"正在分析视频: {video_path}")
    
    # Initialize analyzer
    analyzer = TrajectoryAnalyzer(video_path, output_dir)
    
    # Process video
    analyzer.process()
    
    # Generate visualizations
    analyzer.plot_trajectory()
    analyzer.plot_heatmap()
    analyzer.plot_combined()
    
    # Get statistics
    stats = analyzer.get_statistics()
    
    # Print results
    print("\n分析完成！")
    print(f"输出目录: {analyzer.output_dir}")
    print("\n统计结果:")
    print(f"  总距离: {stats['total_distance']:.1f} 像素")
    print(f"  平均速度: {stats['average_speed']:.2f} 像素/帧")
    print(f"  最大速度: {stats['max_speed']:.2f} 像素/帧")
    print(f"  追踪率: {stats['tracking_rate']:.1f}%")
    
    return {
        'output_dir': str(analyzer.output_dir),
        'statistics': stats,
    }


if __name__ == "__main__":
    main()
