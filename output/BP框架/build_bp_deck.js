// 融资 BP 框架模板 —— 一个部分一页，字大、话白、说清楚准备什么和画什么
const fs = require('fs');
const pptxgen = require('pptxgenjs');

// 从 bp_content.py 取内容（由 dump_content.py 导出为 JSON，保证两份文件同源）
const C = JSON.parse(fs.readFileSync('output/BP框架/bp_content.json', 'utf8'));

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';                 // 13.3 x 7.5
const DEEP='123F63', MID='2E6C97', LIGHT='8FB6CE', PALE='EEF3F7', GRAY='5A6672', INK='2B333B';
const CN = '微软雅黑';
const M = 0.75;                              // 左右页边距

function head(s, no, name, pages) {
  s.addText(no, { x:M, y:0.34, w:1.2, h:0.62, fontFace:CN, fontSize:30, bold:true, color:LIGHT, margin:0 });
  s.addText(name, { x:M + 0.95, y:0.38, w:9.2, h:0.55, fontFace:CN, fontSize:28, bold:true, color:DEEP, margin:0 });
  s.addText(pages, { x:10.2, y:0.5, w:2.35, h:0.35, fontFace:CN, fontSize:13, color:GRAY, align:'right', margin:0 });
}

function colHead(s, x, w, t) {
  s.addShape(pres.ShapeType.rect, { x:x, y:1.86, w:0.14, h:0.28, fill:{ color:MID } });
  s.addText(t, { x:x + 0.28, y:1.82, w:w, h:0.36, fontFace:CN, fontSize:15, bold:true, color:DEEP, margin:0 });
}

function bullets(s, x, y, w, arr, size) {
  s.addText(arr.map((t, i) => ({ text:t, options:{ bullet:true, breakLine: i !== arr.length - 1 } })),
    { x:x, y:y, w:w, h:4.0, fontFace:CN, fontSize:size, color:INK,
      paraSpaceAfter:9, lineSpacingMultiple:1.15, margin:0, valign:'top' });
}

// ---------- 封面 ----------
(function () {
  const s = pres.addSlide();
  s.background = { color: DEEP };
  s.addText('融资 BP 框架', { x:1.1, y:2.15, w:11, h:0.95, fontFace:CN, fontSize:46, bold:true, color:'FFFFFF', margin:0 });
  s.addText('一页一页告诉你：每部分准备什么材料、写什么内容、画什么图',
    { x:1.1, y:3.2, w:11, h:0.5, fontFace:CN, fontSize:19, color:LIGHT, margin:0 });
  s.addShape(pres.ShapeType.line, { x:1.1, y:4.05, w:3.4, h:0, line:{ color:LIGHT, width:2 } });
  s.addText([
    { text:'两条通用规矩', options:{ bold:true, breakLine:true, color:'FFFFFF' } },
    { text:'一、每页标题写一句结论，不写名词。把"产品优势"改成"良率从 65% 提到 92%，2025 年 11 月起批量交付"。', options:{ breakLine:true } },
    { text:'二、能画图就别写字，能列表就别写段落，一页只讲一件事。', options:{ breakLine:false } },
  ], { x:1.1, y:4.45, w:10.5, h:1.5, fontFace:CN, fontSize:14, color:'C3D6E3', paraSpaceAfter:7, margin:0, valign:'top' });
  s.addText('正式版 15—25 页 ｜ 删成路演版 10—12 页 ｜ 再压成一页纸',
    { x:1.1, y:6.35, w:11, h:0.4, fontFace:CN, fontSize:13, color:MID, margin:0 });
  s.addNotes('这是骨架，不是范文。内容各家自己填。');
})();

// ---------- 17 个部分，一部分一页 ----------
C.PARTS.forEach(p => {
  const [no, name, pages, goal, prep, how, tip] = p;
  const s = pres.addSlide();
  head(s, no, name, '建议 ' + pages);
  s.addText(goal, { x:M, y:1.12, w:11.8, h:0.4, fontFace:CN, fontSize:15, color:GRAY, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.66, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });

  colHead(s, M, 4.0, '先准备这些材料');
  colHead(s, 5.5, 6.5, '这一页这样写');
  bullets(s, M + 0.05, 2.3, 4.35, prep, 14);
  bullets(s, 5.55, 2.3, 7.0, how, 14);

  s.addShape(pres.ShapeType.rect, { x:M, y:6.4, w:11.8, h:0.82, fill:{ color:PALE } });
  s.addText([
    { text:'提醒　', options:{ bold:true, color:DEEP } },
    { text:tip, options:{ color:INK } },
  ], { x:M + 0.25, y:6.5, w:11.3, h:0.62, fontFace:CN, fontSize:12.5, margin:0, valign:'top' });
  s.addNotes(tip);
});

// ---------- 加分页 ----------
(function () {
  const s = pres.addSlide();
  head(s, '＋', '有这些情况，再加几页', '按需选用');
  s.addText('不是每家都要写。有对应的事实就单独做一页，放正文里比塞进附录管用。',
    { x:M, y:1.12, w:11.8, h:0.4, fontFace:CN, fontSize:15, color:GRAY, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.66, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });
  s.addText('加什么页', { x:M + 0.2, y:1.9, w:2.1, h:0.3, fontFace:CN, fontSize:13, bold:true, color:DEEP, margin:0 });
  s.addText('什么情况下加', { x:3.0, y:1.9, w:2.6, h:0.3, fontFace:CN, fontSize:13, bold:true, color:DEEP, margin:0 });
  s.addText('这页怎么做', { x:5.9, y:1.9, w:6.6, h:0.3, fontFace:CN, fontSize:13, bold:true, color:DEEP, margin:0 });
  C.EXTRAS.forEach((e, i) => {
    const y = 2.35 + i * 0.68;
    s.addShape(pres.ShapeType.rect, { x:M, y:y, w:11.8, h:0.62, fill:{ color: i % 2 ? 'FFFFFF' : PALE } });
    s.addText(e[0], { x:M + 0.2, y:y + 0.06, w:2.1, h:0.5, fontFace:CN, fontSize:14, bold:true, color:MID, margin:0, valign:'top' });
    s.addText(e[1], { x:3.0, y:y + 0.06, w:2.7, h:0.5, fontFace:CN, fontSize:13, color:GRAY, margin:0, valign:'top' });
    s.addText(e[2], { x:5.9, y:y + 0.04, w:6.6, h:0.56, fontFace:CN, fontSize:13, color:INK, margin:0, valign:'top' });
  });
  s.addNotes('按客户自己的情况挑，没有对应事实的不要硬凑。');
})();

// ---------- 交之前对一遍 ----------
(function () {
  const s = pres.addSlide();
  head(s, '✓', '交之前对一遍', '');
  s.addShape(pres.ShapeType.line, { x:M, y:1.66, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });
  const L = C.CHECKS, half = Math.ceil(L.length / 2);
  [[M, L.slice(0, half)], [7.0, L.slice(half)]].forEach(([x, arr]) => {
    arr.forEach((t, i) => {
      const y = 2.0 + i * 0.62;
      s.addShape(pres.ShapeType.rect, { x:x, y:y + 0.05, w:0.24, h:0.24, fill:{ color:'FFFFFF' }, line:{ color:MID, width:1 } });
      s.addText(t, { x:x + 0.42, y:y, w:5.4, h:0.55, fontFace:CN, fontSize:13.5, color:INK, margin:0, valign:'top' });
    });
  });
  s.addNotes('这一页可以打印出来，定稿前逐条打勾。');
})();

// ---------- 对外发之前脱密 ----------
(function () {
  const s = pres.addSlide();
  head(s, '⊘', '发给外部之前，记得脱密', '');
  s.addText('还没签保密协议、或者要在多家机构之间流转的版本，按下面处理。',
    { x:M, y:1.12, w:11.8, h:0.4, fontFace:CN, fontSize:15, color:GRAY, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.66, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });
  C.DESENSITIZE.forEach((t, i) => {
    const y = 2.15 + i * 0.85;
    s.addShape(pres.ShapeType.rect, { x:M, y:y, w:0.5, h:0.5, fill:{ color:PALE } });
    s.addText(String(i + 1), { x:M, y:y + 0.06, w:0.5, h:0.38, fontFace:CN, fontSize:15, bold:true, color:MID, align:'center', margin:0 });
    s.addText(t, { x:M + 0.8, y:y + 0.02, w:11.0, h:0.5, fontFace:CN, fontSize:15, color:INK, margin:0, valign:'top' });
  });
  s.addShape(pres.ShapeType.rect, { x:M, y:6.4, w:11.8, h:0.82, fill:{ color:PALE } });
  s.addText([
    { text:'提醒　', options:{ bold:true, color:DEEP } },
    { text:'脱密只做遮盖，不改数字。脱密版和完整版的数字必须一样。', options:{ color:INK } },
  ], { x:M + 0.25, y:6.6, w:11.3, h:0.45, fontFace:CN, fontSize:12.5, margin:0 });
  s.addNotes('这一条是投行的标准做法，客户团队往往没意识到。');
})();

pres.writeFile({ fileName: 'output/BP框架/融资BP框架模板.pptx' }).then(f => console.log('saved', f));
