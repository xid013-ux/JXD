# -*- coding: utf-8 -*-
"""以《国泰海通关于巨蟹智能之尽职调查报告V7.docx》为模板，
只保留第六章的版式外壳，重建正文。

版式实测值（取自模板正文第六章）：
  页面    A4 纵向 11906x16838 twips，上下边距 1440、左右 1800（版心 8306）
  一级标题 黑体 14pt，行距 1.5，段前段后 6pt，无首行缩进
  二三四级 宋体加粗 12pt，首行缩进 2 字符，段前 6pt
  正文     宋体 12pt / 西文 Times New Roman，首行缩进 2 字符，行距 1.5，段前 6pt，两端对齐
  资料来源 10.5pt，无缩进
  表格     宽度 100%，fixed 布局，外框 sz=12、内线 sz=4，色 010000
           首行 tblHeader + cantSplit + 加粗居中，单元格 10.5pt
"""
import copy
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

TPL = '../v7.docx'
CONTENT_TW = 8306          # 版心宽度
BORDER = '010000'


def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn('w:' + k), str(v))
    return e


class Builder:
    def __init__(self, tpl=TPL):
        self.doc = Document(tpl)
        body = self.doc.element.body
        # 取正文第六章所在节的 sectPr（模板 body 第 635 个元素内），作为全文唯一分节
        sect = None
        for el in list(body):
            if el.tag == qn('w:p'):
                pPr = el.find(qn('w:pPr'))
                if pPr is not None and pPr.find(qn('w:sectPr')) is not None:
                    sect = copy.deepcopy(pPr.find(qn('w:sectPr')))
                    break_at = el
                    # 只取第一个符合正文页面设置（纵向 A4）的
                    pg = sect.find(qn('w:pgSz'))
                    if pg is not None and pg.get(qn('w:w')) == '11906' \
                            and pg.get(qn('w:orient')) is None:
                        break
        # 清空 body
        for el in list(body):
            body.remove(el)
        if sect is not None:
            body.append(sect)
        self.body = body
        self.sect = sect

    # ---------- 段落 ----------
    def _p(self):
        p = self.doc.add_paragraph()
        # add_paragraph 会追加到 body 末尾（sectPr 之后），需移到 sectPr 之前
        if self.sect is not None:
            self.body.remove(p._p)
            self.sect.addprevious(p._p)
        return p

    def _rpr(self, run, size=12, bold=False, hei='宋体'):
        run.font.size = Pt(size)
        run.bold = bold
        rPr = run._element.get_or_add_rPr()
        f = rPr.find(qn('w:rFonts'))
        if f is None:
            f = OxmlElement('w:rFonts')
            rPr.insert(0, f)
        f.set(qn('w:ascii'), 'Times New Roman')
        f.set(qn('w:hAnsi'), 'Times New Roman')
        f.set(qn('w:eastAsia'), hei)

    def h1(self, text):
        """六、xxx —— 黑体 14pt"""
        p = self._p()
        pf = p.paragraph_format
        pf.line_spacing = 1.5
        pf.space_before = Pt(6)
        pf.space_after = Pt(6)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self._rpr(p.add_run(text), 14, False, '黑体')
        return p

    def h(self, text):
        """（一）/ 1、/（1）—— 宋体加粗 12pt，首行缩进 2 字符"""
        p = self._p()
        pf = p.paragraph_format
        pf.line_spacing = 1.5
        pf.space_before = Pt(6)
        pf.first_line_indent = Pt(24.1)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self._rpr(p.add_run(text), 12, True)
        return p

    def para(self, text):
        p = self._p()
        pf = p.paragraph_format
        pf.line_spacing = 1.5
        pf.space_before = Pt(6)
        pf.first_line_indent = Pt(24)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self._rpr(p.add_run(text), 12, False)
        return p

    def src(self, text):
        """资料来源行：10.5pt，无缩进"""
        p = self._p()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.space_before = Pt(0)
        pf.space_after = Pt(6)
        self._rpr(p.add_run(text), 10.5, False)
        return p

    def pic(self, path, width_in):
        """插图：居中，无首行缩进"""
        p = self._p()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.space_before = Pt(6)
        pf.space_after = Pt(3)
        # 图与其下方的资料来源行必须同页
        p._p.get_or_add_pPr().append(OxmlElement('w:keepNext'))
        p.add_run().add_picture(path, width=Inches(width_in))
        return p

    # ---------- 表格 ----------
    def table(self, rows, widths=None):
        """rows[0] 为表头。widths 为相对列宽，按版心折算为绝对列宽。"""
        ncol = len(rows[0])
        tbl = self.doc.add_table(rows=len(rows), cols=ncol)
        if self.sect is not None:
            self.body.remove(tbl._tbl)
            self.sect.addprevious(tbl._tbl)

        t = tbl._tbl
        # --- tblPr ---
        old = t.find(qn('w:tblPr'))
        if old is not None:
            t.remove(old)
        tblPr = OxmlElement('w:tblPr')
        tblPr.append(_el('w:tblW', w='5000', type='pct'))
        tblPr.append(_el('w:jc', val='center'))
        bd = OxmlElement('w:tblBorders')
        for side, sz in (('top', 12), ('left', 12), ('bottom', 12), ('right', 12),
                         ('insideH', 4), ('insideV', 4)):
            bd.append(_el('w:' + side, val='single', sz=sz, space=0, color=BORDER))
        tblPr.append(bd)
        tblPr.append(_el('w:tblLayout', type='fixed'))
        cm = OxmlElement('w:tblCellMar')
        cm.append(_el('w:left', w='57', type='dxa'))
        cm.append(_el('w:right', w='57', type='dxa'))
        tblPr.append(cm)
        t.insert(0, tblPr)

        # --- 列宽 ---
        if widths is None:
            widths = [1] * ncol
        tot = sum(widths)
        cols = [int(w / tot * CONTENT_TW) for w in widths]
        cols[cols.index(max(cols))] += CONTENT_TW - sum(cols)
        grid = t.find(qn('w:tblGrid'))
        if grid is not None:
            for gc, w in zip(grid.findall(qn('w:gridCol')), cols):
                gc.set(qn('w:w'), str(w))

        for ri, row in enumerate(rows):
            tr = tbl.rows[ri]._tr
            trPr = tr.get_or_add_trPr()
            trPr.append(OxmlElement('w:cantSplit'))
            trPr.append(_el('w:trHeight', val='397'))
            if ri == 0:
                trPr.append(OxmlElement('w:tblHeader'))
            trPr.append(_el('w:jc', val='center'))

            for ci, val in enumerate(row):
                cell = tbl.cell(ri, ci)
                tcPr = cell._tc.get_or_add_tcPr()
                for tag in (qn('w:tcW'),):
                    old = tcPr.find(tag)
                    if old is not None:
                        tcPr.remove(old)
                tcPr.append(_el('w:tcW', w=str(cols[ci]), type='dxa'))
                tcPr.append(_el('w:vAlign', val='center'))

                p = cell.paragraphs[0]
                pf = p.paragraph_format
                pf.space_before = Pt(0)
                pf.space_after = Pt(0)
                if ri == 0:
                    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p._p.get_or_add_pPr().append(OxmlElement('w:keepNext'))
                self._rpr(p.add_run(str(val)), 10.5, ri == 0)
        return tbl

    # ---------- 收尾 ----------
    def save(self, path):
        # 清空模板带入的文档属性，不写入任何署名信息
        cp = self.doc.core_properties
        for k in ('author', 'last_modified_by', 'title', 'subject',
                  'comments', 'category', 'keywords'):
            setattr(cp, k, '')
        cp.revision = 1
        self.doc.save(path)
