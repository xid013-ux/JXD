# 无锡金源半导体专题材料 —— 尽职调查报告体例 Word 正文
#
# 正文取自同目录下的《正文.md》，本脚本只负责版式与表图。
# 改文字改 正文.md，不要改这个文件。
import sys, os, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DD_OUT', 'output/金源/专题/无锡金源半导体专题材料.docx')
os.environ.setdefault('DD_CHARTS', 'output/金源/专题/charts')
from _dd import h1, para, table, figure, set_header, save

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '正文.md')

# 表与图的版式参数，正文里用 <<表1>> <<图1>> 占位
SPECS = {
    '表1': dict(
        headers=['品类', '2024 年全球规模', '2031 年预测', '复合增长率', '竞争格局'],
        rows=[
            ['半导体喷淋头', '11.73 亿美元', '19.70 亿美元', '7.8%',
             '前五合计约 78%，亚太占 60%、北美 32%、欧洲 7%'],
            ['半导体用氮化铝陶瓷加热器', '6.22 亿美元', '9.53 亿美元', '6.2%',
             '日本碍子约 48%，日本作为生产地区占 52%'],
            ['半导体级全氟醚橡胶密封件', '无独立公开统计', '—', '—',
             '杜邦、Greene Tweed、Trelleborg 等境外企业主导'],
        ],
        widths=[19, 15, 14, 11, 41],
        aligns=['left', 'center', 'center', 'center', 'left'],
        caption='表1  三个对应品类的市场规模与竞争格局',
        source='资料来源：QYResearch《2025-2031 全球与中国半导体喷淋头市场现状及未来发展趋势》、'
               '《2025-2031 全球及中国半导体用氮化铝（AlN）陶瓷加热器行业研究及十五五规划分析报告》。'
               '注：两份报告基年均为 2025 年，复合增长率区间为 2025 至 2031 年。',
    ),
    '表2': dict(
        headers=['客户类型', '客户', '对应供货路径'],
        rows=[
            ['设备整机厂商', '拓荆科技、北方华创、盛美上海、中科仪（南通）', '新机配套'],
            ['晶圆制造厂商', '长江存储、长鑫存储、北电集成', '产线备件与新线装机'],
        ],
        widths=[18, 52, 30],
        aligns=['center', 'left', 'center'],
        caption='表2  客户结构',
        source='注：中科仪（南通）指中科仪（南通）半导体设备有限责任公司，'
               '系中国科学院沈阳科学仪器股份有限公司全资子公司，主营半导体干式真空泵；'
               '北电集成指北京电控集成电路制造有限责任公司，其 12 英寸生产线于 2025 年四季度'
               '启动设备搬入，计划 2026 年底量产，当前对应新线装机采购。',
    ),
    '表3': dict(
        headers=['专利类型', '数量', '法律状态'],
        rows=[
            ['发明专利', '19', '授权有效，2023 年至 2026 年陆续取得'],
            ['实用新型', '35', '授权 34 项'],
            ['发明公布', '16', '实质审查 13 项'],
            ['外观设计', '3', '授权有效'],
            ['合计', '73', '有效授权 56 项'],
        ],
        widths=[22, 12, 66],
        aligns=['center', 'center', 'left'],
        caption='表3  公司专利结构',
        source='资料来源：国家知识产权局公开信息，经企查查整理',
    ),
    '图1': dict(
        fname='fig1.png',
        caption='图1  中国晶圆厂零部件采购额及直接采购占比（2020—2029E）',
        source='资料来源：弗若斯特沙利文，经重庆臻宝科技股份有限公司招股说明书（注册稿）披露。'
               '注：直接采购占比由采购额测算得出。',
    ),
}


def build():
    set_header('无锡金源半导体科技有限公司', '专题材料')
    used = set()
    for raw in open(SRC, encoding='utf-8').read().split('\n'):
        line = raw.strip()
        if not line or line.startswith('# '):
            continue
        if line.startswith('> '):
            para(line[2:].strip())
        elif line.startswith('## '):
            h1(line[3:].strip())
        elif re.fullmatch(r'<<(表\d+|图\d+)>>', line):
            key = line[2:-2]
            spec = SPECS[key]
            used.add(key)
            (figure(**spec) if key.startswith('图') else table(**spec))
        else:
            para(line)
    missing = set(SPECS) - used
    if missing:
        raise AssertionError(f'正文.md 中缺少占位符：{sorted(missing)}')
    save()


if __name__ == '__main__':
    build()
