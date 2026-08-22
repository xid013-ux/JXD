# -*- coding: utf-8 -*-
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zf_user_content as U
json.dump({'COVER': U.COVER, 'OUTLINE': U.OUTLINE, 'CHAPTERS': U.CHAPTERS},
          open('output/BP框架/zf_user.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('dumped')
