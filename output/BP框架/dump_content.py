# -*- coding: utf-8 -*-
"""把 bp_content.py 导出成 JSON，供 PPT 构建脚本读取。"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bp_content as B
out = {k: getattr(B, k) for k in ('PARTS', 'EXTRAS', 'CHECKS', 'DESENSITIZE', 'MATERIALS', 'STEPS')}
json.dump(out, open('output/BP框架/bp_content.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('dumped')
