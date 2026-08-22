# -*- coding: utf-8 -*-
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zf_content as Z
out = {k: getattr(Z, k) for k in ('BRIEF', 'CHAPTERS', 'SPECIALS', 'MATERIALS', 'STEPS', 'CHECKS')}
json.dump(out, open('output/BP框架/zf_content.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('dumped')
