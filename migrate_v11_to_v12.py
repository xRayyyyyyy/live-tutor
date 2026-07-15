#!/usr/bin/env python3
"""
Live-Tutor progress.json migration script: v1.1 → v1.2

Migrates existing progress.json files to the new v1.2 schema.
Adds: persona, persona_history, per-chapter current_level, precheck_level,
      diagnostic.mode, error_review_schedule, micro_quizzes.

Usage:
  python3 migrate_v11_to_v12.py output/随机信号分析/progress.json
"""

import json
import sys
import os
from datetime import date


def migrate(progress_path):
    with open(progress_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changes = []

    # 1. Add persona field (if missing)
    if 'persona' not in data:
        data['persona'] = '标准教师'  # default
        changes.append('Added persona field (default: 标准教师)')

    # 2. Add persona_history (if missing)
    if 'persona_history' not in data:
        data['persona_history'] = [
            {
                'chapters': list(range(1, data.get('total_chapters', 0) + 1)),
                'persona': data['persona'],
                'reason': '初始选择（v1.1 迁移）'
            }
        ]
        changes.append('Added persona_history')

    # 3. Migrate diagnostic object
    if 'diagnostic' in data:
        diag = data['diagnostic']
        if 'mode' not in diag:
            diag['mode'] = '深度'  # v1.1 only had deep mode
            changes.append('Added diagnostic.mode (default: 深度)')
        if 'level_mode' not in diag:
            diag['level_mode'] = diag.get('mode', None)
            # Map old "mode" string field to "level_mode"
            if diag.get('mode') in ['基础模式', '巩固模式', '提升模式', '全面模式']:
                diag['level_mode'] = diag['mode']
                diag['mode'] = '深度'
            changes.append('Added diagnostic.level_mode')

    # 4. Remove global current_level/current_mode (replaced by per-chapter)
    old_global_level = data.pop('current_level', None)
    old_global_mode = data.pop('current_mode', None)
    if old_global_level:
        changes.append(f'Removed global current_level ({old_global_level}) → per-chapter tracking')
    if old_global_mode:
        changes.append(f'Removed global current_mode ({old_global_mode})')

    # 5. Per-chapter migration
    for ch in data.get('chapters', []):
        # Add current_level (per-chapter)
        if 'current_level' not in ch:
            # Use the last history entry's level_after, or the old global level
            last_level = None
            if ch.get('history'):
                for h in reversed(ch['history']):
                    if h.get('level_after'):
                        last_level = h['level_after']
                        break
            ch['current_level'] = last_level or old_global_level or 'L1'
            changes.append(f'Chapter {ch["num"]}: added current_level = {ch["current_level"]}')

        # Add precheck_level
        if 'precheck_level' not in ch:
            ch['precheck_level'] = None
            changes.append(f'Chapter {ch["num"]}: added precheck_level (null, not yet prechecked)')

        # Add error_review_schedule
        if 'error_review_schedule' not in ch:
            ch['error_review_schedule'] = []

        # Fix history entries
        for h in ch.get('history', []):
            if 'micro_quizzes' not in h:
                h['micro_quizzes'] = []
            if 'error_count' not in h:
                h['error_count'] = None

    # 6. Add error_adapted_count to final_exam
    if data.get('final_exam') and 'error_adapted_count' not in data['final_exam']:
        data['final_exam']['error_adapted_count'] = 0

    # Write migrated file
    # Backup first
    backup_path = progress_path + '.v11.bak'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(progress_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'✅ Migration complete: {progress_path}')
    print(f'   Backup saved to: {backup_path}')
    print(f'   Changes ({len(changes)}):')
    for c in changes:
        print(f'   - {c}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 migrate_v11_to_v12.py <path-to-progress.json>')
        sys.exit(1)

    for path in sys.argv[1:]:
        if os.path.exists(path):
            migrate(path)
        else:
            print(f'❌ File not found: {path}')
