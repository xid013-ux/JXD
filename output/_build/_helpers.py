# -*- coding: utf-8 -*-
import copy, os
from docx import Document
from docx.shared import Pt, Emu, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image

TPL = '/tmp/claude-0/-home-user-JXD/b33c1a84-553f-5c48-a1f8-b4ca1cd8f155/scratchpad/template.docx'
import os
OUT = os.environ.get('DOCX_OUT','/home/user/JXD/output/out.docx')
CH  = '/home/user/JXD/output/charts/'

doc = Document(TPL)
body = doc.element.body
sectPr = body.find(qn('w:sectPr'))
for child in list(body):
    if child is not sectPr:
        body.remove(child)

def _rpr(el, bold=False, sz=None, color='000000'):
    rPr = OxmlElement('w:rPr')
    f = OxmlElement('w:rFonts'); f.set(qn('w:hint'), 'eastAsia'); rPr.append(f)
    if bold: rPr.append(OxmlElement('w:b'))
    c = OxmlElement('w:color'); c.set(qn('w:val'), color); rPr.append(c)
    if sz:
        s = OxmlElement('w:sz'); s.set(qn('w:val'), str(sz)); rPr.append(s)
    el.append(rPr)

def title(text):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    for tag, attrs in (('w:keepNext', {}), ('w:widowControl', {}),
                       ('w:spacing', {'w:before':'156','w:after':'156','w:line':'360','w:lineRule':'auto'}),
                       ('w:jc', {'w:val':'center'})):
        e = OxmlElement(tag)
        for k, v in attrs.items(): e.set(qn(k), v)
        pPr.append(e)
    r = p.add_run(text)
    rf = r._element.get_or_add_rPr().get_or_add_rFonts()
    for a in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'): rf.set(qn(a), '宋体')
    rf.set(qn('w:hint'), 'eastAsia')
    r.bold = True; r.font.size = Pt(18)
    return p

def h2(text):
    p = doc.add_paragraph(style='Heading 2')
    pPr = p._p.get_or_add_pPr()
    sp = OxmlElement('w:spacing'); sp.set(qn('w:before'),'156'); sp.set(qn('w:after'),'156'); pPr.append(sp)
    r = p.add_run(text); r.bold = True
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:hint'),'eastAsia')
    return p

def h3(text):
    p = doc.add_paragraph(style='Heading 3')
    pPr = p._p.get_or_add_pPr()
    npr = OxmlElement('w:numPr')
    il = OxmlElement('w:ilvl'); il.set(qn('w:val'),'0'); npr.append(il)
    ni = OxmlElement('w:numId'); ni.set(qn('w:val'),'0'); npr.append(ni)
    pPr.append(npr)
    sp = OxmlElement('w:spacing'); sp.set(qn('w:before'),'156'); sp.set(qn('w:after'),'156'); pPr.append(sp)
    r = p.add_run(text)
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:hint'),'eastAsia')
    return p

def para(text):
    p = doc.add_paragraph(style='Normal Indent')
    r = p.add_run(text)
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:hint'),'eastAsia')
    return p

def note(text):
    p = doc.add_paragraph(style='表格后说明')
    r = p.add_run(text)
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:hint'),'eastAsia')
    return p

def blank():
    return doc.add_paragraph()

CONTENT_EMU = 5074920

def figure(fname, caption, source):
    img = Image.open(CH + fname); w, h = img.size
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    kn = OxmlElement('w:keepNext'); pPr.append(kn)
    p.add_run().add_picture(CH + fname, width=Emu(CONTENT_EMU), height=Emu(int(CONTENT_EMU * h / w)))
    cp = doc.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cp.add_run(caption); r.bold = True; r.font.size = Pt(10.5)
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:hint'),'eastAsia')
    note(source)

def set_borders(el, top=None, bottom=None, left=None, right=None, iH=None, iV=None):
    b = OxmlElement('w:tblBorders') if el.tag == qn('w:tblPr') else OxmlElement('w:tcBorders')
    for tag, sz in (('w:top',top),('w:left',left),('w:bottom',bottom),('w:right',right),
                    ('w:insideH',iH),('w:insideV',iV)):
        if sz is None: continue
        e = OxmlElement(tag); e.set(qn('w:val'),'single'); e.set(qn('w:sz'),str(sz))
        e.set(qn('w:space'),'0'); e.set(qn('w:color'),'010000'); b.append(e)
    el.append(b)

def table(headers, rows, widths, caption=None, source=None, aligns=None):
    """widths: list of pct-of-table numbers summing to 5000-ish scale handled internally."""
    if caption:
        cp = doc.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pPr = cp._p.get_or_add_pPr(); pPr.append(OxmlElement('w:keepNext'))
        r = cp.add_run(caption); r.bold = True; r.font.size = Pt(10.5)
        r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:hint'),'eastAsia')
    ncol = len(headers)
    tot = sum(widths)
    pcts = [int(round(w / tot * 5000)) for w in widths]
    tbl = doc.add_table(rows=0, cols=ncol)
    tblPr = tbl._tbl.tblPr
    for ch in list(tblPr):
        if ch.tag in (qn('w:tblW'), qn('w:tblBorders'), qn('w:jc'), qn('w:tblStyle')):
            tblPr.remove(ch)
    tw = OxmlElement('w:tblW'); tw.set(qn('w:w'),'5352'); tw.set(qn('w:type'),'pct'); tblPr.append(tw)
    jc = OxmlElement('w:jc'); jc.set(qn('w:val'),'center'); tblPr.append(jc)
    set_borders(tblPr, top=12, bottom=12, left=12, right=12, iH=4, iV=4)

    def fill(cells, texts, header):
        for i, (c, t) in enumerate(zip(cells, texts)):
            tcPr = c._tc.get_or_add_tcPr()
            for ch in list(tcPr):
                if ch.tag == qn('w:tcW'): tcPr.remove(ch)
            w = OxmlElement('w:tcW'); w.set(qn('w:w'),str(pcts[i])); w.set(qn('w:type'),'pct'); tcPr.append(w)
            if header: set_borders(tcPr, top=12, bottom=4)
            else: set_borders(tcPr, top=4)
            va = OxmlElement('w:vAlign'); va.set(qn('w:val'),'center'); tcPr.append(va)
            c.paragraphs[0].text = ''
            lines = str(t).split('\n')
            for j, ln in enumerate(lines):
                p = c.paragraphs[0] if j == 0 else c.add_paragraph()
                pPr = p._p.get_or_add_pPr()
                if header: pPr.append(OxmlElement('w:keepNext'))
                a = OxmlElement('w:jc')
                if header: a.set(qn('w:val'),'center')
                else:
                    al = (aligns[i] if aligns else 'left')
                    a.set(qn('w:val'), al)
                pPr.append(a)
                r = p.add_run(ln)
                rPr = r._element.get_or_add_rPr()
                rPr.get_or_add_rFonts().set(qn('w:hint'),'eastAsia')
                if header: r.bold = True
                r.font.size = Pt(10.5)
                r.font.color.rgb = RGBColor(0,0,0)

    hr = tbl.add_row()
    trPr = hr._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit')); trPr.append(OxmlElement('w:tblHeader'))
    j = OxmlElement('w:jc'); j.set(qn('w:val'),'center'); trPr.append(j)
    fill(hr.cells, headers, True)
    for row in rows:
        tr = tbl.add_row()
        trPr = tr._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        j = OxmlElement('w:jc'); j.set(qn('w:val'),'center'); trPr.append(j)
        fill(tr.cells, row, False)
    if source: note(source)
    return tbl
