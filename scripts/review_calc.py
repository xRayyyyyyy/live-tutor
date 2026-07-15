#!/usr/bin/env python3
"""
review_calc.py — 间隔复习计算工具 (SM-2 算法)

用法:
  review_calc.py check <progress.json>              查看到期复习项
  review_calc.py update <progress.json> <json_str>  更新复习结果
  review_calc.py init <progress.json> <json_str>    添加新知识点

json_str 为单行 JSON 字符串。
"""

import json
import sys
import math
from datetime import datetime, timedelta
from pathlib import Path

# ── SM-2 常量 ──────────────────────────────────────────────
MIN_EF = 1.3          # 最低 Easy Factor
DEFAULT_EF = 2.5      # 初始 EF
DEFAULT_INTERVAL = 1  # 初始间隔（天）

# 复习间隔序列（repetitions 对应的天数）
INTERVAL_SEQUENCE = [1, 3, 7, 15, 30]


def load_progress(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_progress(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── SM-2 核心计算 ──────────────────────────────────────────

def calc_next_interval(repetitions, ef, current_interval):
    """根据 repetitions 计算下次间隔"""
    if repetitions == 0:
        return 1
    elif repetitions == 1:
        return 3
    elif repetitions == 2:
        return 7
    else:
        return round(current_interval * ef)


def calc_retention(days_since, ef, interval):
    """指数衰减模型: R = e^(-t/S), S = interval × ef / 2.5"""
    s = max(interval * ef / DEFAULT_EF, 0.1)
    return math.exp(-days_since / s)


def update_ef(ef, quality):
    """SM-2 EF 更新公式。quality: 0-5"""
    new_ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    return round(max(new_ef, MIN_EF), 2)


# ── check: 查看到期复习项 ─────────────────────────────────

def cmd_check(filepath):
    data = load_progress(filepath)
    tracking = data.get('knowledge_tracking', {})
    now = datetime.now()

    results = []
    for kp_id, kp in tracking.items():
        last_reviewed = datetime.fromisoformat(kp['last_reviewed'])
        days_since = (now - last_reviewed).total_seconds() / 86400
        interval = kp.get('interval_days', DEFAULT_INTERVAL)
        ef = kp.get('ef', DEFAULT_EF)
        repetitions = kp.get('repetitions', 0)

        retention = calc_retention(days_since, ef, interval)
        next_review = last_reviewed + timedelta(days=interval)
        overdue_days = (now - next_review).total_seconds() / 86400

        if overdue_days >= -0.5:  # 到期或即将到期（半天容差）
            results.append({
                'id': kp_id,
                'chapter': kp.get('chapter', '?'),
                'title': kp.get('title', kp_id),
                'retention': round(retention * 100),
                'days_since_review': round(days_since, 1),
                'overdue_days': max(0, round(overdue_days, 1)),
                'interval': interval,
                'ef': ef,
                'repetitions': repetitions,
                'urgency': 'overdue' if overdue_days >= 0 else 'due_today'
            })

    # 按紧迫度排序：超期天数降序
    results.sort(key=lambda x: (-x['overdue_days'], x['retention']))

    # 统计
    total = len(tracking)
    overdue = len([r for r in results if r['urgency'] == 'overdue'])
    due_today = len([r for r in results if r['urgency'] == 'due_today'])

    output = {
        'timestamp': now.isoformat(timespec='seconds'),
        'summary': {
            'total_tracked': total,
            'overdue': overdue,
            'due_today': due_today,
            'upcoming_7d': len([r for r in results
                                if r['urgency'] == 'due_today' or 0 <= r['overdue_days'] <= 7])
        },
        'review_queue': results[:15]  # 最多返回 15 条
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


# ── update: 更新复习结果 ──────────────────────────────────

def cmd_update(filepath, updates_json):
    """
    updates_json 格式:
    [{"id": "ch1_info_entropy", "quality": 4}, ...]
    quality: 0=完全忘了, 1-2=模糊, 3=勉强记得, 4=记得, 5=非常熟
    """
    data = load_progress(filepath)
    tracking = data.get('knowledge_tracking', {})
    updates = json.loads(updates_json)
    now = datetime.now()
    results = []

    for upd in updates:
        kp_id = upd['id']
        quality = upd['quality']  # 0-5

        if kp_id not in tracking:
            results.append({'id': kp_id, 'status': 'not_found'})
            continue

        kp = tracking[kp_id]
        ef = kp.get('ef', DEFAULT_EF)
        repetitions = kp.get('repetitions', 0)
        interval = kp.get('interval_days', DEFAULT_INTERVAL)

        if quality >= 3:
            # 复习成功 → 增加 repetitions，延长间隔
            repetitions += 1
            ef = update_ef(ef, quality)
            interval = calc_next_interval(repetitions, ef, interval)
            status = 'success'
        else:
            # 复习失败 → 重置 repetitions，缩短间隔
            repetitions = 0
            ef = update_ef(ef, quality)
            interval = DEFAULT_INTERVAL
            status = 'reset'

        next_review = now + timedelta(days=interval)

        kp['last_reviewed'] = now.isoformat(timespec='seconds')
        kp['repetitions'] = repetitions
        kp['ef'] = ef
        kp['interval_days'] = interval
        kp['next_review'] = next_review.isoformat(timespec='seconds')
        kp.setdefault('review_history', []).append({
            'date': now.strftime('%Y-%m-%d'),
            'quality': quality,
            'interval_after': interval
        })

        tracking[kp_id] = kp
        results.append({
            'id': kp_id,
            'status': status,
            'new_interval': interval,
            'new_ef': ef,
            'next_review': next_review.strftime('%Y-%m-%d')
        })

    data['knowledge_tracking'] = tracking
    save_progress(filepath, data)
    print(json.dumps(results, ensure_ascii=False, indent=2))


# ── init: 添加新知识点 ─────────────────────────────────────

def cmd_init(filepath, kps_json):
    """
    kps_json 格式:
    [{"id": "ch1_info_entropy", "chapter": 1, "title": "自信息量", "stars": 3}, ...]
    """
    data = load_progress(filepath)
    tracking = data.get('knowledge_tracking', {})
    new_kps = json.loads(kps_json)
    now = datetime.now()
    added = []

    for kp in new_kps:
        kp_id = kp['id']
        if kp_id in tracking:
            continue  # 已存在，跳过

        tracking[kp_id] = {
            'chapter': kp['chapter'],
            'title': kp['title'],
            'stars': kp.get('stars', 3),
            'learned_at': now.isoformat(timespec='seconds'),
            'last_reviewed': now.isoformat(timespec='seconds'),
            'repetitions': 0,
            'interval_days': DEFAULT_INTERVAL,
            'ef': DEFAULT_EF,
            'next_review': (now + timedelta(days=DEFAULT_INTERVAL)).isoformat(timespec='seconds'),
            'is_error': kp.get('is_error', False),
            'review_history': [{
                'date': now.strftime('%Y-%m-%d'),
                'action': 'learned',
                'interval_after': DEFAULT_INTERVAL
            }]
        }
        added.append(kp_id)

    data['knowledge_tracking'] = tracking
    save_progress(filepath, data)

    print(json.dumps({
        'added': added,
        'total_tracked': len(tracking)
    }, ensure_ascii=False, indent=2))


# ── CLI 入口 ───────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    filepath = sys.argv[2]

    if cmd == 'check':
        cmd_check(filepath)
    elif cmd == 'update':
        if len(sys.argv) < 4:
            print('Error: update 需要 json_str 参数')
            sys.exit(1)
        cmd_update(filepath, sys.argv[3])
    elif cmd == 'init':
        if len(sys.argv) < 4:
            print('Error: init 需要 json_str 参数')
            sys.exit(1)
        cmd_init(filepath, sys.argv[3])
    else:
        print(f'Unknown command: {cmd}')
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
