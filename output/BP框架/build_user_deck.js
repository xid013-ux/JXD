// 燕京中发融资 BP 框架 —— 版式重做（内容取自用户修订版，未做改写）
const fs = require('fs');
const pptxgen = require('pptxgenjs');
const D = JSON.parse(fs.readFileSync('output/BP框架/zf_user.json', 'utf8'));

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
const W = 13.333, H = 7.5;
const DEEP='123F63', MID='2E6C97', STEEL='5B93B8', MIST='C3D6E3',
      PAPER='F4F7FA', LINE='DCE5EC', INK='22303C', GRAY='63707C';
const CN = '微软雅黑';
const M = 0.75, CW = W - M * 2;

const total = 2 + D.CHAPTERS.length + D.CHAPTERS.reduce((n, c) => n + c[3].length, 0);
let idx = 0;

function footer(s, label) {
  s.addShape(pres.ShapeType.line, { x:M, y:7.12, w:CW, h:0, line:{ color:LINE, width:1 } });
  s.addText('燕京中发　融资 BP 框架', { x:M, y:7.16, w:6, h:0.28, fontFace:CN, fontSize:9.5, color:GRAY, margin:0 });
  s.addText(label, { x:W - M - 4, y:7.16, w:4, h:0.28, fontFace:CN, fontSize:9.5, color:GRAY, align:'right', margin:0 });
}

// 带编号的条目组
function numbered(s, x, y, w, h, arr) {
  const parts = [];
  arr.forEach((t, i) => {
    parts.push({ text: String(i + 1).padStart(2, '0') + '   ', options:{ color:STEEL, bold:true } });
    parts.push({ text: t, options:{ color:INK, breakLine: i !== arr.length - 1, paraSpaceAfter: 12 } });
  });
  s.addText(parts, { x:x, y:y, w:w, h:h, fontFace:CN, fontSize:15,
                     lineSpacingMultiple:1.28, margin:0, valign:'middle' });
}

function card(s, x, y, w, h, title, items) {
  s.addShape(pres.ShapeType.rect, { x:x, y:y, w:w, h:h, fill:{ color:PAPER } });
  s.addShape(pres.ShapeType.rect, { x:x, y:y, w:w, h:0.46, fill:{ color:MIST } });
  s.addShape(pres.ShapeType.rect, { x:x, y:y, w:0.16, h:0.46, fill:{ color:DEEP } });
  s.addText(title, { x:x + 0.36, y:y + 0.05, w:w - 0.6, h:0.36, fontFace:CN, fontSize:14, bold:true, color:DEEP, margin:0 });
  numbered(s, x + 0.36, y + 0.62, w - 0.72, h - 0.9, items);
}

// ---------------- 封面 ----------------
(function () {
  const s = pres.addSlide();
  s.background = { color: DEEP };
  s.addShape(pres.ShapeType.rect, { x:8.9, y:0, w:4.45, h:H, fill:{ color:'0E3454' } });
  s.addShape(pres.ShapeType.rect, { x:9.55, y:0, w:0.9, h:H, fill:{ color:MID } });
  s.addShape(pres.ShapeType.rect, { x:10.75, y:0, w:0.34, h:H, fill:{ color:STEEL } });
  s.addShape(pres.ShapeType.rect, { x:11.4, y:0, w:0.14, h:H, fill:{ color:MIST } });

  s.addText(D.COVER.title, { x:1.0, y:2.35, w:7.6, h:0.95, fontFace:CN, fontSize:40, bold:true, color:'FFFFFF', margin:0 });
  s.addText(D.COVER.sub, { x:1.0, y:3.4, w:7.6, h:0.45, fontFace:CN, fontSize:17, color:MIST, margin:0 });
  s.addShape(pres.ShapeType.rect, { x:1.0, y:4.12, w:1.5, h:0.06, fill:{ color:STEEL } });
  s.addText(D.COVER.line1, { x:1.0, y:4.5, w:7.6, h:0.35, fontFace:CN, fontSize:13.5, color:'D8E4EE', margin:0 });
  s.addText(D.COVER.line2, { x:1.0, y:4.95, w:7.6, h:0.35, fontFace:CN, fontSize:13.5, color:'D8E4EE', margin:0 });
  s.addShape(pres.ShapeType.line, { x:1.0, y:6.15, w:7.6, h:0, line:{ color:'2A5476', width:1 } });
  s.addText(D.COVER.org, { x:1.0, y:6.3, w:7.6, h:0.35, fontFace:CN, fontSize:13, color:MIST, margin:0 });
})();

// ---------------- 大纲页 ----------------
(function () {
  const s = pres.addSlide(); idx++;
  s.addShape(pres.ShapeType.rect, { x:M, y:0.5, w:0.16, h:0.5, fill:{ color:DEEP } });
  s.addText(D.OUTLINE.title, { x:M + 0.34, y:0.46, w:8, h:0.56, fontFace:CN, fontSize:26, bold:true, color:DEEP, margin:0 });
  s.addText(D.OUTLINE.lead, { x:M + 0.34, y:1.06, w:9, h:0.34, fontFace:CN, fontSize:14, color:GRAY, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.56, w:CW, h:0, line:{ color:LINE, width:1.25 } });

  const gap = 0.16, colW = (CW - gap * 4) / 5;
  D.CHAPTERS.forEach((ch, ci) => {
    const x = M + ci * (colW + gap);
    s.addShape(pres.ShapeType.rect, { x:x, y:1.9, w:colW, h:0.96, fill:{ color:DEEP } });
    s.addText(ch[0], { x:x + 0.18, y:1.99, w:colW - 0.36, h:0.28, fontFace:CN, fontSize:11, color:MIST, margin:0 });
    s.addText(ch[1], { x:x + 0.18, y:2.27, w:colW - 0.36, h:0.44, fontFace:CN, fontSize:17, bold:true, color:'FFFFFF', margin:0 });
    ch[3].forEach((p, pi) => {
      const y = 3.0 + pi * 0.5;
      s.addShape(pres.ShapeType.rect, { x:x, y:y, w:colW, h:0.44, fill:{ color: pi % 2 ? 'FFFFFF' : PAPER } });
      s.addShape(pres.ShapeType.rect, { x:x, y:y, w:0.05, h:0.44, fill:{ color: pi % 2 ? LINE : MIST } });
      s.addText(p[0], { x:x + 0.16, y:y + 0.08, w:0.42, h:0.28, fontFace:CN, fontSize:11, bold:true, color:STEEL, margin:0 });
      s.addText(p[1].replace('（每个独立产品开一页）', ''),
        { x:x + 0.62, y:y + 0.06, w:colW - 0.76, h:0.34, fontFace:CN, fontSize:11.5, color:INK, margin:0, valign:'top' });
    });
  });
  s.addText('全篇 21 页 · 五章 · 每页均给出所需材料、写法与注意事项',
    { x:M, y:6.6, w:CW, h:0.35, fontFace:CN, fontSize:12, color:GRAY, margin:0 });
  footer(s, `${String(idx).padStart(2, '0')} / ${String(total - 1).padStart(2, '0')}`);
})();

// ---------------- 各章 ----------------
D.CHAPTERS.forEach((ch, ci) => {
  // 章封面
  const d = pres.addSlide(); idx++;
  d.addShape(pres.ShapeType.rect, { x:0, y:0, w:4.9, h:H, fill:{ color:DEEP } });
  d.addShape(pres.ShapeType.rect, { x:4.9, y:0, w:0.12, h:H, fill:{ color:STEEL } });
  d.addText(String(ci + 1).padStart(2, '0'), { x:0.9, y:2.5, w:3.4, h:2.0, fontFace:CN, fontSize:110, bold:true, color:'1B5079', margin:0 });
  d.addText(ch[0], { x:1.0, y:4.55, w:3.4, h:0.42, fontFace:CN, fontSize:19, color:MIST, margin:0 });
  d.addText(ch[1], { x:5.7, y:2.75, w:7.2, h:0.95, fontFace:CN, fontSize:40, bold:true, color:DEEP, margin:0 });
  if (ch[2]) d.addText(ch[2], { x:5.7, y:3.8, w:7.0, h:0.4, fontFace:CN, fontSize:15, color:GRAY, margin:0 });
  d.addShape(pres.ShapeType.rect, { x:5.7, y:4.35, w:1.2, h:0.05, fill:{ color:STEEL } });
  ch[3].forEach((p, pi) => {
    const y = 4.7 + Math.floor(pi / 2) * 0.52, x = 5.7 + (pi % 2) * 3.6;
    d.addText(p[0], { x:x, y:y, w:0.4, h:0.32, fontFace:CN, fontSize:11.5, bold:true, color:STEEL, margin:0 });
    d.addText(p[1], { x:x + 0.42, y:y, w:3.1, h:0.34, fontFace:CN, fontSize:12, color:INK, margin:0, valign:'top' });
  });

  // 内容页
  ch[3].forEach(p => {
    const [no, name, lead, prep, how, tip, howTitle] = p;
    const s = pres.addSlide(); idx++;

    s.addShape(pres.ShapeType.rect, { x:M, y:0.42, w:0.74, h:0.74, fill:{ color:DEEP } });
    s.addText(no, { x:M, y:0.53, w:0.74, h:0.5, fontFace:CN, fontSize:26, bold:true, color:'FFFFFF', align:'center', margin:0 });
    s.addText(name, { x:M + 0.95, y:0.44, w:7.8, h:0.5, fontFace:CN, fontSize:25, bold:true, color:DEEP, margin:0 });
    s.addText('这页说清楚：' + lead, { x:M + 0.95, y:0.95, w:8.6, h:0.34, fontFace:CN, fontSize:14, color:GRAY, margin:0 });
    s.addShape(pres.ShapeType.rect, { x:W - M - 3.1, y:0.5, w:3.1, h:0.04, fill:{ color:MIST } });
    s.addText(ch[0] + '　' + ch[1], { x:W - M - 3.1, y:0.62, w:3.1, h:0.3, fontFace:CN, fontSize:12, color:MID, align:'right', margin:0 });

    s.addShape(pres.ShapeType.line, { x:M, y:1.5, w:CW, h:0, line:{ color:LINE, width:1.25 } });

    const cy = 1.78, chh = 4.32;
    if (prep.length === 0) {
      card(s, M, cy, CW, chh, howTitle, how);
    } else {
      card(s, M, cy, 4.5, chh, '先准备这些材料', prep);
      card(s, M + 4.78, cy, CW - 4.78, chh, howTitle, how);
    }

    s.addShape(pres.ShapeType.rect, { x:M, y:6.3, w:CW, h:0.7, fill:{ color:PAPER } });
    s.addShape(pres.ShapeType.rect, { x:M, y:6.3, w:0.14, h:0.7, fill:{ color:DEEP } });
    s.addText([{ text:'提醒　', options:{ bold:true, color:DEEP } }, { text:tip, options:{ color:INK } }],
      { x:M + 0.36, y:6.38, w:CW - 0.6, h:0.56, fontFace:CN, fontSize:12, margin:0, valign:'middle' });
    footer(s, `${ch[0]}　${String(idx).padStart(2, '0')} / ${String(total - 1).padStart(2, '0')}`);
    s.addNotes(tip);
  });
});

pres.writeFile({ fileName: 'output/BP框架/燕京中发融资BP框架（教学版）.pptx' }).then(f => console.log('saved', f));
