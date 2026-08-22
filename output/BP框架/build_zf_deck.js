// 燕京中发融资 BP 框架（教学版）—— 一页 BP 一页说明
const fs = require('fs');
const pptxgen = require('pptxgenjs');
const C = JSON.parse(fs.readFileSync('output/BP框架/zf_content.json', 'utf8'));

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
const DEEP='123F63', MID='2E6C97', LIGHT='8FB6CE', PALE='EEF3F7', GRAY='5A6672', INK='2B333B';
const CN = '微软雅黑';
const M = 0.75;

function tipBar(s, t) {
  s.addShape(pres.ShapeType.rect, { x:M, y:6.4, w:11.8, h:0.82, fill:{ color:PALE } });
  s.addText([{ text:'提醒　', options:{ bold:true, color:DEEP } }, { text:t, options:{ color:INK } }],
    { x:M + 0.25, y:6.5, w:11.3, h:0.62, fontFace:CN, fontSize:12.5, margin:0, valign:'top' });
}
function bullets(s, x, y, w, arr, size) {
  s.addText(arr.map((t, i) => ({ text:t, options:{ bullet:true, breakLine: i !== arr.length - 1 } })),
    { x:x, y:y, w:w, h:4.0, fontFace:CN, fontSize:size, color:INK,
      paraSpaceAfter:9, lineSpacingMultiple:1.15, margin:0, valign:'top' });
}

// 封面
(function () {
  const s = pres.addSlide();
  s.background = { color: DEEP };
  s.addText('燕京中发　融资 BP 框架', { x:1.1, y:2.1, w:11, h:0.95, fontFace:CN, fontSize:42, bold:true, color:'FFFFFF', margin:0 });
  s.addText('混合所有制改革引入战略投资者 · 材料编写指引', { x:1.1, y:3.15, w:11, h:0.5, fontFace:CN, fontSize:19, color:LIGHT, margin:0 });
  s.addShape(pres.ShapeType.line, { x:1.1, y:3.95, w:3.4, h:0, line:{ color:LIGHT, width:2 } });
  s.addText('全篇 25 页，分五章：公司介绍 · 行业分析 · 发展规划 · 财务状况 · 融资方案',
    { x:1.1, y:4.3, w:11, h:0.4, fontFace:CN, fontSize:15, color:'C3D6E3', margin:0 });
  s.addText('每一页告诉你：先准备哪些材料、这一页怎么写、要注意什么',
    { x:1.1, y:4.8, w:11, h:0.4, fontFace:CN, fontSize:15, color:'C3D6E3', margin:0 });
  s.addText('国泰海通证券投资银行部', { x:1.1, y:6.4, w:11, h:0.4, fontFace:CN, fontSize:13, color:MID, margin:0 });
})();

// 说明页
(function () {
  const s = pres.addSlide();
  s.addText('动笔之前，先说清楚三件事', { x:M, y:0.45, w:11.8, h:0.6, fontFace:CN, fontSize:28, bold:true, color:DEEP, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.25, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });
  C.BRIEF.forEach((b, i) => {
    const y = 1.6 + i * 1.75;
    s.addShape(pres.ShapeType.rect, { x:M, y:y, w:0.08, h:1.4, fill:{ color:MID } });
    s.addText(b[0], { x:M + 0.3, y:y, w:11.2, h:0.4, fontFace:CN, fontSize:17, bold:true, color:DEEP, margin:0 });
    s.addText(b[1], { x:M + 0.3, y:y + 0.42, w:11.2, h:1.0, fontFace:CN, fontSize:14, color:INK, lineSpacingMultiple:1.25, margin:0, valign:'top' });
  });
})();

// 全篇总览
(function () {
  const s = pres.addSlide();
  s.addText('全篇 25 页长这样', { x:M, y:0.45, w:11.8, h:0.6, fontFace:CN, fontSize:28, bold:true, color:DEEP, margin:0 });
  s.addText('顺序不要动：先看公司，再看行业，最后看价格。',
    { x:M, y:1.08, w:11.8, h:0.35, fontFace:CN, fontSize:14, color:GRAY, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.5, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });
  const colW = 2.30, gap = 0.09;
  C.CHAPTERS.forEach((ch, ci) => {
    const x = M + ci * (colW + gap);
    s.addShape(pres.ShapeType.rect, { x:x, y:1.8, w:colW, h:0.92, fill:{ color:DEEP } });
    s.addText(ch[0], { x:x + 0.15, y:1.88, w:colW - 0.3, h:0.28, fontFace:CN, fontSize:11.5, color:LIGHT, margin:0 });
    s.addText(ch[1], { x:x + 0.15, y:2.14, w:colW - 0.3, h:0.42, fontFace:CN, fontSize:16, bold:true, color:'FFFFFF', margin:0 });
    ch[3].forEach((p, pi) => {
      const y = 2.86 + pi * 0.46;
      s.addShape(pres.ShapeType.rect, { x:x, y:y, w:colW, h:0.4, fill:{ color: pi % 2 ? 'FFFFFF' : PALE } });
      s.addText(p[0], { x:x + 0.12, y:y + 0.06, w:0.42, h:0.28, fontFace:CN, fontSize:11, bold:true, color:MID, margin:0 });
      s.addText(p[1], { x:x + 0.56, y:y + 0.05, w:colW - 0.68, h:0.32, fontFace:CN, fontSize:11.5, color:INK, margin:0, valign:'top' });
    });
    s.addText(ch[2], { x:x, y:7.0, w:colW, h:0.4, fontFace:CN, fontSize:9.5, color:GRAY, margin:0, valign:'top' });
  });
})();

// 各章
C.CHAPTERS.forEach(ch => {
  // 章封面
  const d = pres.addSlide();
  d.background = { color: PALE };
  d.addShape(pres.ShapeType.rect, { x:0, y:2.9, w:0.55, h:1.6, fill:{ color:MID } });
  d.addText(ch[0], { x:1.3, y:2.85, w:10, h:0.45, fontFace:CN, fontSize:16, color:MID, margin:0 });
  d.addText(ch[1], { x:1.3, y:3.25, w:10, h:0.8, fontFace:CN, fontSize:38, bold:true, color:DEEP, margin:0 });
  d.addText(ch[2], { x:1.3, y:4.15, w:10.5, h:0.4, fontFace:CN, fontSize:15, color:GRAY, margin:0 });
  d.addText(ch[3].map(p => p[0] + ' ' + p[1]).join('　｜　'),
    { x:1.3, y:4.9, w:10.8, h:0.6, fontFace:CN, fontSize:12, color:MID, margin:0, valign:'top' });

  ch[3].forEach(p => {
    const [no, name, goal, prep, how, tip] = p;
    const s = pres.addSlide();
    s.addText(no, { x:M, y:0.34, w:1.1, h:0.62, fontFace:CN, fontSize:30, bold:true, color:LIGHT, margin:0 });
    s.addText(name, { x:M + 0.9, y:0.38, w:8.4, h:0.55, fontFace:CN, fontSize:28, bold:true, color:DEEP, margin:0 });
    s.addText(ch[0] + '　' + ch[1], { x:9.6, y:0.5, w:2.95, h:0.35, fontFace:CN, fontSize:12, color:GRAY, align:'right', margin:0 });
    s.addText(goal, { x:M, y:1.12, w:11.8, h:0.4, fontFace:CN, fontSize:15, color:GRAY, margin:0 });
    s.addShape(pres.ShapeType.line, { x:M, y:1.66, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });
    [[M, '先准备这些材料'], [5.5, '这一页这样写']].forEach(([x, t]) => {
      s.addShape(pres.ShapeType.rect, { x:x, y:1.86, w:0.14, h:0.28, fill:{ color:MID } });
      s.addText(t, { x:x + 0.28, y:1.82, w:5.0, h:0.36, fontFace:CN, fontSize:15, bold:true, color:DEEP, margin:0 });
    });
    bullets(s, M + 0.05, 2.3, 4.35, prep, 14);
    bullets(s, 5.55, 2.3, 7.0, how, 14);
    tipBar(s, tip);
    s.addNotes(tip);
  });
});

// 特别注意
(function () {
  const s = pres.addSlide();
  s.addText('中发这份 BP，特别注意这六件事', { x:M, y:0.45, w:11.8, h:0.6, fontFace:CN, fontSize:28, bold:true, color:DEEP, margin:0 });
  s.addText('这几条是这个项目独有的，普通融资 BP 上没有。', { x:M, y:1.08, w:11.8, h:0.35, fontFace:CN, fontSize:14, color:GRAY, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.5, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });
  C.SPECIALS.forEach((sp, i) => {
    const y = 1.85 + i * 0.85;
    s.addShape(pres.ShapeType.rect, { x:M, y:y, w:11.8, h:0.76, fill:{ color: i % 2 ? 'FFFFFF' : PALE } });
    s.addText(sp[0], { x:M + 0.25, y:y + 0.2, w:1.7, h:0.4, fontFace:CN, fontSize:15, bold:true, color:MID, margin:0 });
    s.addText(sp[1], { x:M + 2.1, y:y + 0.1, w:9.4, h:0.6, fontFace:CN, fontSize:14, color:INK, margin:0, valign:'top' });
  });
})();

// 备料清单
(function () {
  const s = pres.addSlide();
  s.addText('动手之前，先把料收齐', { x:M, y:0.45, w:11.8, h:0.6, fontFace:CN, fontSize:28, bold:true, color:DEEP, margin:0 });
  s.addText('料不齐就开始做页面，只能写形容词。', { x:M, y:1.08, w:11.8, h:0.35, fontFace:CN, fontSize:14, color:GRAY, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.5, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });
  ['类别', '要收的材料', '找谁要'].forEach((t, i) => {
    const x = [M + 0.2, 2.9, 10.6][i];
    s.addText(t, { x:x, y:1.72, w:3, h:0.3, fontFace:CN, fontSize:13, bold:true, color:DEEP, margin:0 });
  });
  C.MATERIALS.forEach((m, i) => {
    const y = 2.15 + i * 0.62;
    s.addShape(pres.ShapeType.rect, { x:M, y:y, w:11.8, h:0.56, fill:{ color: i % 2 ? 'FFFFFF' : PALE } });
    s.addText(m[0], { x:M + 0.2, y:y + 0.06, w:2.1, h:0.44, fontFace:CN, fontSize:14, bold:true, color:MID, margin:0, valign:'top' });
    s.addText(m[1], { x:2.9, y:y + 0.06, w:7.5, h:0.44, fontFace:CN, fontSize:13.5, color:INK, margin:0, valign:'top' });
    s.addText(m[2], { x:10.6, y:y + 0.06, w:1.9, h:0.44, fontFace:CN, fontSize:13, color:GRAY, margin:0, valign:'top' });
  });
  s.addText('六步做完：收料 → 用文字写全 → 做图做表 → 标题改成结论 → 四处对数 → 内部过合规口径',
    { x:M, y:6.75, w:11.8, h:0.4, fontFace:CN, fontSize:13, color:GRAY, margin:0 });
})();

// 检查清单
(function () {
  const s = pres.addSlide();
  s.addText('交之前对一遍', { x:M, y:0.45, w:11.8, h:0.6, fontFace:CN, fontSize:28, bold:true, color:DEEP, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.25, w:11.8, h:0, line:{ color:LIGHT, width:1.5 } });
  const L = C.CHECKS, half = Math.ceil(L.length / 2);
  [[M, L.slice(0, half)], [7.0, L.slice(half)]].forEach(([x, arr]) => {
    arr.forEach((t, i) => {
      const y = 1.75 + i * 0.72;
      s.addShape(pres.ShapeType.rect, { x:x, y:y + 0.05, w:0.24, h:0.24, fill:{ color:'FFFFFF' }, line:{ color:MID, width:1 } });
      s.addText(t, { x:x + 0.42, y:y, w:5.4, h:0.62, fontFace:CN, fontSize:13.5, color:INK, margin:0, valign:'top' });
    });
  });
})();

pres.writeFile({ fileName: 'output/BP框架/燕京中发融资BP框架（教学版）.pptx' }).then(f => console.log('saved', f));
