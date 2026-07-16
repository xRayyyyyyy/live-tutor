#!/usr/bin/env python3
"""
信号可视化工具 — 为 Live-Tutor 生成教学用图表
用法：python3 scripts/plot_signals.py <command> [args] --output <path>

命令：
  sine        生成正弦波图         --freq <Hz> --amp <振幅> --phase <弧度> --duration <秒>
  superpose   叠加多个正弦波       --waves "f1,a1;f2,a2;..." --duration <秒>
  spectrum    频谱图（频域）        --freqs "f1,f2,..." --amps "a1,a2,..."
  compare     时域 vs 频域对比     --waves "f1,a1;f2,a2;..."
  square      方波 + 谐波分解      --harmonics <谐波数>

所有输出均为 PNG，暗色主题，与 HTML 样式统一。
"""

import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 非交互模式
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os
import sys

# ═══════════ 暗色主题配置 ═══════════
DARK_THEME = {
    'bg': '#0f172a',
    'card': '#1e293b',
    'accent': '#38bdf8',
    'star': '#fbbf24',
    'text': '#e2e8f0',
    'muted': '#94a3b8',
    'success': '#34d399',
    'warn': '#f97316',
    'purple': '#a78bfa',
    'pink': '#f472b6',
}

def apply_dark_theme(fig, ax):
    """应用暗色主题到 figure 和 axes"""
    fig.set_facecolor(DARK_THEME['card'])
    ax.set_facecolor(DARK_THEME['card'])
    ax.tick_params(colors=DARK_THEME['muted'], labelsize=10)
    ax.spines['bottom'].set_color(DARK_THEME['muted'])
    ax.spines['left'].set_color(DARK_THEME['muted'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.label.set_color(DARK_THEME['text'])
    ax.yaxis.label.set_color(DARK_THEME['text'])
    ax.title.set_color(DARK_THEME['text'])
    ax.title.set_fontsize(14)
    ax.grid(True, alpha=0.15, color=DARK_THEME['muted'])

def setup_chinese_font():
    """配置中文字体"""
    font_candidates = [
        'PingFang SC', 'Heiti SC', 'STHeiti', 'SimHei',
        'Microsoft YaHei', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC'
    ]
    import matplotlib.font_manager as fm
    available = set(f.name for f in fm.fontManager.ttflist)
    for font in font_candidates:
        if font in available:
            rcParams['font.sans-serif'] = [font, 'DejaVu Sans']
            rcParams['axes.unicode_minus'] = False
            return font
    # 回退：使用默认字体，中文可能显示为方块
    rcParams['axes.unicode_minus'] = False
    return None

# ═══════════ 绘图命令 ═══════════

def cmd_sine(args):
    """生成单个正弦波"""
    t = np.linspace(0, args.duration, 1000)
    y = args.amp * np.sin(2 * np.pi * args.freq * t + args.phase)

    fig, ax = plt.subplots(figsize=(10, 3.5))
    apply_dark_theme(fig, ax)

    ax.plot(t, y, color=DARK_THEME['accent'], linewidth=2.5)
    ax.set_xlabel('时间 t (秒)')
    ax.set_ylabel('振幅')
    ax.set_title(f'正弦波: {args.freq} Hz, 振幅={args.amp}')
    ax.set_ylim(-args.amp * 1.3, args.amp * 1.3)

    # 标注周期
    if args.freq > 0:
        T = 1 / args.freq
        if T <= args.duration:
            ax.annotate('', xy=(0, -args.amp * 1.1), xytext=(T, -args.amp * 1.1),
                       arrowprops=dict(arrowstyle='<->', color=DARK_THEME['star'], lw=1.5))
            ax.text(T/2, -args.amp * 1.25, f'T = {T:.4f}s',
                   color=DARK_THEME['star'], ha='center', fontsize=11)

    plt.tight_layout()
    plt.savefig(args.output, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'✅ 正弦波图已保存: {args.output}')

def cmd_superpose(args):
    """叠加多个正弦波"""
    waves = parse_waves(args.waves)
    t = np.linspace(0, args.duration, 1000)

    fig, axes = plt.subplots(len(waves) + 1, 1, figsize=(10, 2.5 * (len(waves) + 1)), sharex=True)
    if len(waves) + 1 == 1:
        axes = [axes]

    colors = [DARK_THEME['accent'], DARK_THEME['star'], DARK_THEME['purple'],
              DARK_THEME['pink'], DARK_THEME['success']]

    # 画各个分量
    y_total = np.zeros_like(t)
    for i, (freq, amp) in enumerate(waves):
        y = amp * np.sin(2 * np.pi * freq * t)
        y_total += y
        ax = axes[i]
        apply_dark_theme(fig, ax)
        ax.plot(t, y, color=colors[i % len(colors)], linewidth=2)
        ax.set_ylabel('振幅')
        ax.set_title(f'{freq} Hz (振幅={amp})', fontsize=12)
        ax.set_ylim(-amp * 1.3, amp * 1.3)

    # 画叠加结果
    ax = axes[-1]
    apply_dark_theme(fig, ax)
    ax.plot(t, y_total, color=DARK_THEME['warn'], linewidth=2.5)
    ax.set_xlabel('时间 t (秒)')
    ax.set_ylabel('振幅')
    ax.set_title('叠加结果（所有波相加）', fontsize=13)

    plt.tight_layout()
    plt.savefig(args.output, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'✅ 叠加波图已保存: {args.output}')

def cmd_spectrum(args):
    """生成频谱图"""
    freqs = [float(f) for f in args.freqs.split(',')]
    amps = [float(a) for a in args.amps.split(',')]

    fig, ax = plt.subplots(figsize=(10, 4))
    apply_dark_theme(fig, ax)

    colors = [DARK_THEME['accent'], DARK_THEME['star'], DARK_THEME['purple'],
              DARK_THEME['pink'], DARK_THEME['success'], DARK_THEME['warn']]

    for i, (f, a) in enumerate(zip(freqs, amps)):
        ax.bar(f, a, width=max(freqs) * 0.03, color=colors[i % len(colors)],
               alpha=0.9, edgecolor='white', linewidth=0.5)
        ax.text(f, a + max(amps) * 0.05, f'{a}', color=DARK_THEME['text'],
               ha='center', fontsize=11, fontweight='bold')

    ax.set_xlabel('频率 (Hz)')
    ax.set_ylabel('振幅')
    ax.set_title('频谱图 — 信号由哪些频率组成')
    ax.set_xlim(0, max(freqs) * 1.2)
    ax.set_ylim(0, max(amps) * 1.3)

    plt.tight_layout()
    plt.savefig(args.output, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'✅ 频谱图已保存: {args.output}')

def cmd_compare(args):
    """时域 vs 频域对比"""
    waves = parse_waves(args.waves)
    t = np.linspace(0, args.duration, 1000)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))

    # 时域
    apply_dark_theme(fig, ax1)
    y_total = np.zeros_like(t)
    for freq, amp in waves:
        y_total += amp * np.sin(2 * np.pi * freq * t)
    ax1.plot(t, y_total, color=DARK_THEME['accent'], linewidth=2)
    ax1.set_xlabel('时间 t (秒)')
    ax1.set_ylabel('振幅')
    ax1.set_title('时域 — 信号随时间变化', fontsize=13)

    # 频域
    apply_dark_theme(fig, ax2)
    freqs = [w[0] for w in waves]
    amps = [w[1] for w in waves]
    colors = [DARK_THEME['star'], DARK_THEME['purple'], DARK_THEME['pink'],
              DARK_THEME['success'], DARK_THEME['warn']]
    for i, (f, a) in enumerate(zip(freqs, amps)):
        ax2.bar(f, a, width=max(freqs) * 0.03, color=colors[i % len(colors)],
               alpha=0.9, edgecolor='white', linewidth=0.5)
        ax2.text(f, a + max(amps) * 0.05, f'{f}Hz', color=DARK_THEME['text'],
                ha='center', fontsize=10)
    ax2.set_xlabel('频率 (Hz)')
    ax2.set_ylabel('振幅')
    ax2.set_title('频域 — 信号由哪些频率组成', fontsize=13)
    ax2.set_xlim(0, max(freqs) * 1.2)
    ax2.set_ylim(0, max(amps) * 1.3)

    plt.tight_layout()
    plt.savefig(args.output, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'✅ 时域vs频域对比图已保存: {args.output}')

def cmd_square(args):
    """方波 + 谐波分解"""
    t = np.linspace(0, 2, 2000)
    n_harmonics = args.harmonics

    fig, axes = plt.subplots(n_harmonics + 1, 1, figsize=(10, 2 * (n_harmonics + 1)), sharex=True)

    # 画各次谐波
    y_total = np.zeros_like(t)
    colors = [DARK_THEME['accent'], DARK_THEME['star'], DARK_THEME['purple'],
              DARK_THEME['pink'], DARK_THEME['success'], DARK_THEME['warn'],
              DARK_THEME['muted']]

    for n in range(n_harmonics):
        k = 2 * n + 1  # 奇数次谐波: 1, 3, 5, 7...
        amp = 4 / (np.pi * k)
        y = amp * np.sin(2 * np.pi * k * t)
        y_total += y

        ax = axes[n]
        apply_dark_theme(fig, ax)
        ax.plot(t, y, color=colors[n % len(colors)], linewidth=1.5)
        ax.set_ylabel('振幅', fontsize=9)
        ax.set_title(f'第{k}次谐波 (振幅={amp:.3f})', fontsize=10)

    # 画叠加结果
    ax = axes[-1]
    apply_dark_theme(fig, ax)
    ax.plot(t, y_total, color=DARK_THEME['warn'], linewidth=2.5)
    ax.set_xlabel('时间 t (秒)')
    ax.set_ylabel('振幅')
    ax.set_title(f'叠加 {n_harmonics} 个奇次谐波 → 趋近方波', fontsize=13)

    plt.tight_layout()
    plt.savefig(args.output, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'✅ 方波分解图已保存: {args.output}')

# ═══════════ 工具函数 ═══════════

def parse_waves(wave_str):
    """解析波形参数: "f1,a1;f2,a2;..." """
    waves = []
    for pair in wave_str.split(';'):
        parts = pair.strip().split(',')
        freq = float(parts[0])
        amp = float(parts[1]) if len(parts) > 1 else 1.0
        waves.append((freq, amp))
    return waves

# ═══════════ CLI 入口 ═══════════

def main():
    parser = argparse.ArgumentParser(description='Live-Tutor 信号可视化工具')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # 公共参数函数
    def add_common_args(p):
        p.add_argument('--output', '-o', required=True, help='输出 PNG 路径')

    # sine
    p_sine = subparsers.add_parser('sine')
    add_common_args(p_sine)
    p_sine.add_argument('--freq', type=float, required=True)
    p_sine.add_argument('--amp', type=float, default=1.0)
    p_sine.add_argument('--phase', type=float, default=0.0)
    p_sine.add_argument('--duration', type=float, default=1.0)

    # superpose
    p_super = subparsers.add_parser('superpose')
    add_common_args(p_super)
    p_super.add_argument('--waves', required=True, help='"f1,a1;f2,a2;..."')
    p_super.add_argument('--duration', type=float, default=1.0)

    # spectrum
    p_spec = subparsers.add_parser('spectrum')
    add_common_args(p_spec)
    p_spec.add_argument('--freqs', required=True, help='"f1,f2,..."')
    p_spec.add_argument('--amps', required=True, help='"a1,a2,..."')

    # compare
    p_cmp = subparsers.add_parser('compare')
    add_common_args(p_cmp)
    p_cmp.add_argument('--waves', required=True, help='"f1,a1;f2,a2;..."')
    p_cmp.add_argument('--duration', type=float, default=1.0)

    # square
    p_sq = subparsers.add_parser('square')
    add_common_args(p_sq)
    p_sq.add_argument('--harmonics', type=int, default=5)

    args = parser.parse_args()

    # 确保输出目录存在
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)

    # 设置中文字体
    font = setup_chinese_font()
    if font:
        print(f'📝 使用字体: {font}')

    # 执行命令
    commands = {
        'sine': cmd_sine,
        'superpose': cmd_superpose,
        'spectrum': cmd_spectrum,
        'compare': cmd_compare,
        'square': cmd_square,
    }
    commands[args.command](args)

if __name__ == '__main__':
    main()
