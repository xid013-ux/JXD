# ---------- schema order fix-up ----------
PPR_ORDER = ['w:pStyle','w:keepNext','w:keepLines','w:pageBreakBefore','w:framePr','w:widowControl',
 'w:numPr','w:suppressLineNumbers','w:pBdr','w:shd','w:tabs','w:suppressAutoHyphens','w:kinsoku',
 'w:wordWrap','w:overflowPunct','w:topLinePunct','w:autoSpaceDE','w:autoSpaceDN','w:bidi',
 'w:adjustRightInd','w:snapToGrid','w:spacing','w:ind','w:contextualSpacing','w:mirrorIndents',
 'w:suppressOverlap','w:jc','w:textDirection','w:textAlignment','w:textboxTightWrap','w:outlineLvl',
 'w:divId','w:cnfStyle','w:rPr','w:sectPr','w:pPrChange']
TBLPR_ORDER = ['w:tblStyle','w:tblpPr','w:tblOverlap','w:bidiVisual','w:tblStyleRowBandSize',
 'w:tblStyleColBandSize','w:tblW','w:jc','w:tblCellSpacing','w:tblInd','w:tblBorders','w:shd',
 'w:tblLayout','w:tblCellMar','w:tblLook','w:tblCaption','w:tblDescription']
TCPR_ORDER = ['w:cnfStyle','w:tcW','w:gridSpan','w:hMerge','w:vMerge','w:tcBorders','w:shd',
 'w:noWrap','w:tcMar','w:textDirection','w:tcFitText','w:vAlign','w:hideMark']
TRPR_ORDER = ['w:cnfStyle','w:divId','w:gridBefore','w:gridAfter','w:wBefore','w:wAfter',
 'w:cantSplit','w:trHeight','w:tblHeader','w:tblCellSpacing','w:jc','w:hidden']

def _reorder(el, order):
    idx = {qn(t): i for i, t in enumerate(order)}
    kids = list(el)
    kids.sort(key=lambda c: idx.get(c.tag, len(order)))
    for c in kids:
        el.append(c)

for _tag, _order in (('w:pPr', PPR_ORDER), ('w:tblPr', TBLPR_ORDER),
                     ('w:tcPr', TCPR_ORDER), ('w:trPr', TRPR_ORDER)):
    for _el in doc.element.body.iter(qn(_tag)):
        _reorder(_el, _order)

doc.save(OUT)
print('saved', OUT)
