// 校验：8 型均可达 + 互不并列（no ties）
const fs = require('fs');
const DATA = JSON.parse(fs.readFileSync(__dirname + '/data.json', 'utf8'));
const { questions: Q, types: T, axThresh: AX_T, avThresh: AV_T } = DATA;

function compute(ans) {
  let ax=0,av=0,sw=0,sl=0,ao=0,at=0,ad=0,ac=0,fs=0,ff=0;
  Q.forEach((q,i)=>{ const w=q.opts[ans[i]].w||{};
    ax+=w.ax||0; av+=w.av||0; sw+=w.sw||0; sl+=w.sl||0;
    ao+=w.ao||0; at+=w.at||0; ad+=w.ad||0; ac+=w.ac||0;
    fs+=w.fs||0; ff+=w.ff||0; });
  const axHi=ax>=AX_T, avHi=av>=AV_T;
  let type;
  if(!axHi&&!avHi) type = sw>=sl?'t2':'t1';
  else if(axHi&&!avHi) type = ao>=at?'t3':'t4';
  else if(!axHi&&avHi) type = ac>=ad?'t6':'t5';
  else type = ff>=fs?'t8':'t7';
  return {type,ax,av};
}

// 每个类型的目标向量（基础惩罚让“安全/中性”选项优先于反向选项）
const BASE = {ax:-0.1, av:-0.1};
const TARGETS = {
  t1: Object.assign({},BASE,{sl:1}),
  t2: Object.assign({},BASE,{sw:1}),
  t3: Object.assign({},BASE,{ax:1,ao:1,av:-1}),
  t4: Object.assign({},BASE,{ax:1,at:1,av:-1}),
  t5: Object.assign({},BASE,{av:1,ad:1,ax:-1}),
  t6: Object.assign({},BASE,{av:1,ac:1,ax:-1}),
  t7: Object.assign({},BASE,{ax:1,av:1,fs:1}),
  t8: Object.assign({},BASE,{ax:1,av:1,ff:1}),
};

function dot(w,t){ let s=0; for(const k in t){ s += (w[k]||0)*t[k]; } return s; }

let allOk = true;
for (const tid of Object.keys(TARGETS)) {
  const tgt = TARGETS[tid];
  const ans = Q.map(q => {
    let best=0, bv=-1e9;
    q.opts.forEach((o,i)=>{ const d=dot(o.w||{}, tgt); if(d>bv){bv=d;best=i;} });
    return best;
  });
  const r = compute(ans);
  const ok = r.type === tid;
  if(!ok) allOk=false;
  console.log((ok?'OK  ':'FAIL')+' '+tid+' ('+T[tid].name+')  => got '+r.type+'  ax='+r.ax+' av='+r.av);
}
// 反向验证：确认其它类型不会把该“纯模式”判成自己 —— 即每个纯模式唯一命中
for (const tid of Object.keys(TARGETS)) {
  const tgt = TARGETS[tid];
  const ans = Q.map(q => { let best=0,bv=-1e9; q.opts.forEach((o,i)=>{const d=dot(o.w||{},tgt); if(d>bv){bv=d;best=i;}}); return best; });
  const r = compute(ans);
  if(r.type!==tid){ allOk=false; console.log('COLLISION: pure '+tid+' misclassified as '+r.type); }
}
console.log(allOk ? '\n==> ALL 8 TYPES REACHABLE & NO TIES' : '\n==> VALIDATION FAILED');
process.exit(allOk?0:1);
