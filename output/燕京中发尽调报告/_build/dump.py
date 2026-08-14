import sys, docx
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

def iter_block(parent):
    body = parent.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

d = docx.Document(sys.argv[1])
show_fmt = len(sys.argv) > 2 and sys.argv[2] == 'fmt'
i = 0
for b in iter_block(d):
    if isinstance(b, Paragraph):
        t = b.text.strip()
        if not t:
            i += 1
            continue
        info = ''
        if show_fmt:
            pf = b.paragraph_format
            r = b.runs[0] if b.runs else None
            eaf = None
            if r is not None:
                rpr = r._element.rPr
                if rpr is not None and rpr.rFonts is not None:
                    eaf = rpr.rFonts.get(qn('w:eastAsia')) or rpr.rFonts.get(qn('w:ascii'))
            info = f" [style={b.style.name}|font={eaf}|sz={r.font.size.pt if r is not None and r.font.size else None}|b={r.font.bold if r is not None else None}|ind1st={pf.first_line_indent}|indL={pf.left_indent}|align={pf.alignment}]"
        print(f"P{i}: {t}{info}")
    else:
        print(f"T{i}: TABLE {len(b.rows)}x{len(b.columns)}")
        for ri,row in enumerate(b.rows):
            cells=[c.text.strip().replace('\n','/') for c in row.cells]
            print("   | " + " | ".join(cells))
            if ri>40: print("   ...trunc"); break
    i += 1
