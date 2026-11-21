import os
import streamlit as st
import streamlit.components.v1 as components

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Put your Hugging Face key in a file named .env next to this app.py:
#   HF_TOKEN=hf_your_key_here
# It is optional. Without it, the dashboard shows rule-based insights.
# The key is used inside your browser page, so run this on your own computer only.
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2.5-72B-Instruct")

st.set_page_config(page_title="Competitor Analysis Agent", page_icon="📊", layout="wide")
st.markdown("<style>.block-container{padding:0!important;max-width:100%}header,footer,#MainMenu{visibility:hidden}.stApp{background:#07121a}</style>", unsafe_allow_html=True)

DASHBOARD_HTML = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Competitor Analysis Agent</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{--bg:#07121a;--p:#0c1c26;--p2:#102633;--ln:#17313a;--fg:#e6f1f3;--mut:#8aa4ad;--g:#10e0a0;--b:#2f8cff;--o:#f59e0b;--r:#ef4444;--pu:#a855f7;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:light){:root{--bg:#eef5f7;--p:#fff;--p2:#f1f7f8;--ln:#d5e3e7;--fg:#0b1d24;--mut:#587079;--g:#059669}}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(1000px 500px at 90% -10%,#0e3b4a55,transparent),var(--bg);color:var(--fg);font:14px/1.5 Inter,system-ui,sans-serif}
.wrap{max-width:1360px;margin:0 auto;padding:16px 20px 40px}
.top{display:flex;align-items:center;gap:20px;flex-wrap:wrap;border-bottom:1px solid var(--ln);padding-bottom:12px}
.lg{font-weight:700;font-size:19px;letter-spacing:.04em}.lg b{color:var(--g)}.lg span{color:var(--mut);font-weight:500;font-size:14px;margin-left:8px}
.tabs{display:flex;gap:4px;margin-left:auto;flex-wrap:wrap}.tabs button{background:none;border:0;color:var(--mut);font:600 14px Inter;padding:9px 14px;cursor:pointer;border-bottom:2px solid transparent}.tabs button.on{color:var(--g);border-color:var(--g)}
h1{font-size:28px;margin:16px 0 4px}h3{font-size:12px;letter-spacing:.07em;margin:0 0 10px;font-weight:700;text-transform:uppercase}
.sm{font-size:10px;border:1px solid var(--o);color:var(--o);border-radius:10px;padding:0 7px;margin-left:6px;letter-spacing:0}
.card{background:var(--p);border:1px solid var(--ln);border-radius:16px;padding:16px;min-width:0}
.form{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0;align-items:end}
label{font-size:11px;color:var(--mut);display:block;margin-bottom:3px}
input,select{width:100%;background:var(--p2);border:1px solid var(--ln);color:var(--fg);border-radius:10px;padding:9px 11px;font:14px Inter}
input:focus,select:focus{outline:2px solid var(--g)}
.btn{background:linear-gradient(90deg,var(--g),#059669);color:#04130d;border:0;border-radius:24px;padding:10px 20px;font:700 14px Inter;cursor:pointer;transition:.2s}.btn:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(16,224,160,.3)}
.btn.o{background:none;color:var(--g);border:1.5px solid var(--g)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:14px}
.kpi small{color:var(--mut);display:block}.kpi b{font-size:26px;display:block;margin-top:2px}.up{color:var(--g)}.dn{color:var(--r)}
.g{display:grid;gap:14px;margin-bottom:14px}.g3{grid-template-columns:1fr 1.5fr 1fr}.g2{grid-template-columns:1fr 1fr}
@media(max-width:900px){.g3,.g2{grid-template-columns:1fr}}
canvas{max-height:280px}
table{width:100%;border-collapse:collapse;font-size:13px}th{color:var(--mut);text-align:left;font-weight:600;padding:8px;border-bottom:1px solid var(--ln);cursor:pointer;white-space:nowrap}td{padding:8px;border-bottom:1px solid var(--ln)}tr:hover td{background:var(--p2)}
.tw{overflow-x:auto}.bar{height:7px;background:var(--ln);border-radius:4px;min-width:60px}.bar i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--g),#34d399)}
.th{padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600}.High{background:#7f1d1d;color:#fecaca}.Medium{background:#78350f;color:#fde68a}.Low{background:#064e3b;color:#a7f3d0}.You{background:#1e3a8a;color:#bfdbfe}
.sl{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px 18px}.sl div{font-size:12px}.sl input{padding:0;accent-color:var(--g)}
.hm{display:grid;gap:3px;font-size:12px}.hm div{padding:7px;border-radius:6px;text-align:center}
.chips{display:flex;flex-wrap:wrap;gap:7px}.chips span{background:var(--p2);border:1px solid var(--ln);border-radius:16px;padding:3px 11px;font-size:12px}
.ads{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}.ad{background:var(--p2);border:1px solid var(--ln);border-radius:14px;overflow:hidden}.ad .im{height:110px;display:grid;place-items:center;font-size:30px}.ad .tx{padding:10px;font-size:12.5px}.ad small{color:var(--mut)}
.ov{position:fixed;inset:0;background:#000a;z-index:50;display:none;place-items:center}.ov.on{display:grid}.ov .card{width:min(380px,90vw)}
.st{padding:5px 0;color:var(--mut)}.st.ok{color:var(--g)}.st.ok:before{content:"✓ "}
.sk{height:14px;border-radius:7px;background:linear-gradient(90deg,var(--p2),var(--ln),var(--p2));background-size:200% 100%;animation:sh 1.2s infinite;margin:8px 0}@keyframes sh{to{background-position:-200% 0}}
.rec{border-left:3px solid var(--g);padding:6px 12px;margin:8px 0;background:var(--p2);border-radius:0 10px 10px 0}
.pn{display:none}.pn.on{display:block}.note{color:var(--mut);font-size:12px}
svg text{fill:var(--fg);font-size:3px}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style></head><body><div class="wrap">
<div class="top"><div class="lg"><b>COMPETITOR</b>ANALYSIS<span>| AI Market Intelligence</span></div>
<div class="tabs" id="tabs"><button class="on" data-t="ov">Overview</button><button data-t="cp">Competitors</button><button data-t="kw">Keywords</button><button data-t="ad">Meta Ads</button><button data-t="in">Insights</button></div></div>
<h1>Competitor Analysis &amp; Brand Visibility</h1>
<div class="card"><div class="form">
<div><label>Company name</label><input id="co" value="Varadharaja Trading Company"></div>
<div><label>Location</label><input id="lo" value="Puducherry, India"></div>
<div><label>Industry</label><input id="ind" value="cooking oil store"></div>
<div><label>Competitors (5-15)</label><input id="nn" type="number" min="5" max="15" value="8"></div>
<div><label>Add competitor</label><input id="add" placeholder="Name, then press Add"></div>
<div style="display:flex;gap:8px"><button class="btn" id="run">Run analysis</button><button class="btn o" id="addb">Add</button></div></div>
<div class="note">Competitor data, keywords and ads here are generated sample data for this demo. Real Google and Meta data need API keys.</div></div>
<div class="card" style="margin:14px 0"><h3>Scoring weights (%)</h3><div class="form" style="margin-top:0"><div><label>Industry preset</label><select id="pre"></select></div></div><div class="sl" id="sl"></div></div>
<div id="app"><div class="sk"></div><div class="sk" style="width:70%"></div></div></div>
<div class="ov" id="ov"><div class="card"><h3>Agent running</h3><div id="steps"></div></div></div>
<script>
const $=id=>document.getElementById(id),CATS=["Search visibility","Reputation","Paid activity","Keyword strategy","Social presence","Website quality","Local presence"],W0=[25,20,15,15,10,10,5];
const PRE={"Default":W0,"Restaurant / retail":[15,30,10,10,10,5,20],"Online services":[30,15,20,20,5,10,0]};
const COL={High:"#ef4444",Medium:"#f59e0b",Low:"#10e0a0",You:"#2f8cff"},SUF=["Hub","Pro","Experts","Studio","Point","Works","Zone","Plus","Co","Solutions","Mart","Depot","House","Express","Traders"];
const HF={t:"__HF_TOKEN__",m:"__HF_MODEL__"};
async function askAI(msgs){if(HF.t&&HF.t.indexOf("__")<0){const r=await fetch("https://router.huggingface.co/v1/chat/completions",{method:"POST",headers:{"Authorization":"Bearer "+HF.t,"Content-Type":"application/json"},body:JSON.stringify({model:HF.m,messages:msgs,max_tokens:300})});if(!r.ok)throw 0;return{text:(await r.json()).choices[0].message.content}}
if(!Z)Z=await claude.use("sample");if(!Z)throw 0;return Z(msgs,{cache:false,modelTier:"quick"})}
let D=null,W=[...W0],SK="Score",SD=-1,CH={},TAB="ov",Z=null;
function rng(s){return()=>{s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function hash(s){let h=0;for(const c of s)h=Math.imul(31,h)+c.charCodeAt(0)|0;return h}
const cap=s=>s.replace(/\b\w/g,c=>c.toUpperCase());
PRE&&Object.keys(PRE).forEach(k=>$('pre').add(new Option(k,k)));
function sliders(){$('sl').innerHTML=CATS.map((c,i)=>`<div>${c}: <b>${W[i]}</b><input type="range" min="0" max="50" value="${W[i]}" data-i="${i}" aria-label="${c} weight"></div>`).join('')}
sliders();$('sl').oninput=e=>{W[+e.target.dataset.i]=+e.target.value;sliders();if(D)paint()};$('pre').onchange=e=>{W=[...PRE[e.target.value]];sliders();if(D)paint()};
function mk(r,name,type,R){const o={name,type,dist:type==="You"?0:+(0.5+r()*19.5).toFixed(1),ov:type==="You"?100:R(10,80),rating:+(3.4+r()*1.5).toFixed(1),reviews:R(20,900),ads:R(0,30),fol:R(300,20000),ppw:R(1,9),x:R(8,92),y:R(10,88),cat:CATS.map(()=>R(20,95))};
o.cat[1]=Math.round(o.rating/5*70+Math.min(o.reviews,500)/500*30);o.rv=[0,1,2,3,4,5].map(i=>Math.round(o.reviews*(.55+.09*i+r()*.03)));o.av=[0,1,2,3,4,5].map(()=>Math.max(0,o.ads+R(-8,8)));return o}
function gen(){const co=$('co').value.trim()||"My Business",lo=$('lo').value.trim()||"City",ind=$('ind').value.trim()||"business",n=Math.min(15,Math.max(5,+$('nn').value||8)),r=rng(hash(co+lo+ind)),R=(a,b)=>a+Math.floor(r()*(b-a+1)),city=lo.split(",")[0];
const rows=[mk(r,co+" (You)","You",R)];for(let i=0;i<n;i++)rows.push(mk(r,cap(`${city} ${ind} ${SUF[i]}`),r()<.7?"Direct":"Indirect",R));
const I=ind.toLowerCase(),kw=[["Branded",co.toLowerCase()],["Branded",co.toLowerCase()+" reviews"],["Service",I],["Service","best "+I],["Service","buy "+I+" online"],["Location",I+" near me"],["Location",I+" in "+city.toLowerCase()],["Informational","how to choose "+I],["Informational",I+" price guide"],["Informational","is "+I+" healthy"]].map(([c,k])=>({c,k,vol:R(50,9000),rk:rows.map(()=>r()<.25?null:R(1,30))}));
D={co,lo,ind,rows,kw,r,R}}
const mm=a=>{const lo=Math.min(...a),hi=Math.max(...a);return a.map(v=>hi===lo?50:(v-lo)/(hi-lo)*100)};
function score(){const rows=D.rows,N=CATS.map((_,j)=>mm(rows.map(o=>o.cat[j]))),pr=mm(rows.map(o=>o.dist)),tw=W.reduce((a,b)=>a+b,0)||1;
rows.forEach((o,i)=>{o.n=N.map(c=>c[i]);o.Score=+(o.n.reduce((a,v,j)=>a+v*W[j],0)/tw).toFixed(1);const t=.5*o.Score+.25*(100-pr[i])+.25*o.ov;o.Threat=o.type==="You"?"You":t>65?"High":t>40?"Medium":"Low"})}
function ch(id,cfg){if(CH[id])CH[id].destroy();Chart.defaults.color="#8aa4ad";Chart.defaults.borderColor="#17313a";CH[id]=new Chart($(id),cfg)}
const opt=(x={})=>({responsive:true,maintainAspectRatio:true,plugins:{legend:{labels:{boxWidth:10}}},...x});
function paint(){score();const rows=D.rows,me=rows[0],cp=rows.slice(1),avg=cp.reduce((a,o)=>a+o.Score,0)/cp.length,rank=rows.filter(o=>o.Score>me.Score).length+1,top=[...cp].sort((a,b)=>b.Score-a.Score),gap=me.Score-avg,tot=rows.reduce((a,o)=>a+o.cat[0],0);
const ov=`<div class="kpis"><div class="card kpi"><small>Competitors found</small><b>${cp.length}</b></div><div class="card kpi"><small>Your rank</small><b>${rank} <span class="note">of ${rows.length}</span></b></div><div class="card kpi"><small>Average market score</small><b>${avg.toFixed(1)}</b></div><div class="card kpi"><small>Top threat</small><b style="font-size:16px">${top[0].name}</b></div><div class="card kpi"><small>Gap vs average</small><b class="${gap>=0?"up":"dn"}">${gap>=0?"▲":"▼"} ${Math.abs(gap).toFixed(1)}</b></div></div>
<div class="g g3"><div class="card"><h3>Share of voice</h3><canvas id="c1"></canvas></div><div class="card"><h3>Review growth (6 months)<span class="sm">Sample</span></h3><canvas id="c2"></canvas></div><div class="card"><h3>You vs top rivals</h3><canvas id="c3"></canvas></div></div>
<div class="g g2"><div class="card"><h3>Positioning matrix</h3><canvas id="c4"></canvas><div class="note">Top-right = high visibility and reputation. Bubble size = score.</div></div><div class="card"><h3>Meta ad volume trend<span class="sm">Sample</span></h3><canvas id="c5"></canvas></div></div>`;
const rs=[...rows].sort((a,b)=>(typeof a[SK]==="string"?a[SK].localeCompare(b[SK]):a[SK]-b[SK])*SD),fl=$("fl")?$("fl").value:"All";
const cpn=`<div class="card"><h3>Leaderboard</h3><div style="margin-bottom:8px"><select id="fl" style="width:160px"><option>All</option><option>High</option><option>Medium</option><option>Low</option></select></div><div class="tw"><table><tr>${[["name","Competitor"],["Score","Score"],["Threat","Threat"],["rating","Rating"],["reviews","Reviews"],["ads","Meta ads"],["dist","Km"],["ov","Overlap %"]].map(([k,l])=>`<th data-k="${k}">${l}${SK===k?(SD>0?" ▲":" ▼"):""}</th>`).join("")}<th></th></tr>
${rs.filter(o=>fl==="All"||o.Threat===fl||o.type==="You").map(o=>`<tr><td>${o.name}</td><td><div class="bar"><i style="width:${o.Score}%"></i></div>${o.Score}</td><td><span class="th ${o.Threat}">${o.Threat}</span></td><td>${o.rating}</td><td>${o.reviews}</td><td>${o.ads}</td><td>${o.dist}</td><td>${o.ov}</td><td>${o.type==="You"?"":`<button class="btn o" style="padding:2px 10px" data-rm="${o.name}">Remove</button>`}</td></tr>`).join("")}</table></div><div class="note">Score = Σ(normalized category × weight). Hover a metric name in the radar for each category. Threat blends score, distance and keyword overlap.</div></div>
<div class="g g2" style="margin-top:14px"><div class="card"><h3>Competitor map<span class="sm">Sample</span></h3><svg viewBox="0 0 100 100" style="width:100%;background:var(--p2);border-radius:12px">${[20,40,60,80].map(v=>`<line x1="${v}" y1="0" x2="${v}" y2="100" stroke="#17313a" stroke-width=".3"/><line x1="0" y1="${v}" x2="100" y2="${v}" stroke="#17313a" stroke-width=".3"/>`).join("")}${rows.map(o=>`<circle cx="${o.x}" cy="${o.y}" r="${2+o.Score/14}" fill="${COL[o.Threat]}" fill-opacity=".75"><title>${o.name}: ${o.Score}</title></circle>`).join("")}</svg><div class="note">Pin size = score, color = threat (blue = you).</div></div><div class="card"><h3>Sentiment from reviews<span class="sm">Sample</span></h3><canvas id="c6"></canvas></div></div>`;
const cl=["Branded","Service","Location","Informational"],hm=`<div class="hm" style="grid-template-columns:150px repeat(4,1fr)"><div></div>${cl.map(c=>`<div><b>${c}</b></div>`).join("")}${rows.map((o,i)=>`<div style="text-align:left">${o.name.slice(0,22)}</div>${cl.map(c=>{const k=D.kw.filter(x=>x.c===c),n=k.filter(x=>x.rk[i]&&x.rk[i]<=10).length;return `<div style="background:rgba(16,224,160,${.12+n*.3})">${n}/${k.length}</div>`}).join("")}`).join("")}</div>`;
const gaps=D.kw.filter(k=>!(k.rk[0]&&k.rk[0]<=10)&&k.rk.slice(1).filter(v=>v&&v<=10).length>=2).sort((a,b)=>b.vol-a.vol);
const kw=`<div class="card"><h3>Keyword universe by intent<span class="sm">Sample</span></h3>${cl.map(c=>`<div style="margin-bottom:10px"><b>${c}</b><div class="chips">${D.kw.filter(k=>k.c===c).map(k=>`<span>${k.k} · ${k.vol.toLocaleString()}/mo</span>`).join("")}</div></div>`).join("")}</div>
<div class="g g2" style="margin-top:14px"><div class="card"><h3>Overlap heatmap (keywords in top 10)</h3><div class="tw">${hm}</div></div><div class="card"><h3>Keyword gaps</h3><div class="note">Keywords where 2+ rivals rank top 10 and you do not.</div><table><tr><th>Keyword</th><th>Intent</th><th>Volume</th></tr>${gaps.map(k=>`<tr><td>${k.k}</td><td>${k.c}</td><td>${k.vol.toLocaleString()}</td></tr>`).join("")||`<tr><td colspan="3">No major gaps.</td></tr>`}</table></div></div>`;
const th=["Offer: limited-time discount","New arrival","Trust: customer reviews","Free delivery"],fm=["Image","Video","Carousel"],ic=["🛒","🎬","🖼️","⭐","🚚"],gr=["#064e3b,#10e0a0","#1e3a8a,#2f8cff","#78350f,#f59e0b","#581c87,#a855f7"];
const ads=top.slice(0,6).flatMap((o,i)=>[0,1].map(j=>({o,t:th[(i+j)%4],f:fm[(i+j)%3],d:3+((i*7+j*11)%60),g:gr[(i+j)%4],ic:ic[(i+j)%5]}))).slice(0,10);
const ad=`<div class="card"><h3>Meta ads gallery<span class="sm">Sample</span></h3><div class="ads">${ads.map(a=>`<div class="ad"><div class="im" style="background:linear-gradient(135deg,${a.g})">${a.ic}</div><div class="tx"><b>${a.o.name.slice(0,24)}</b><br>${a.t}<br><small>${a.f} · running ${a.d} days</small></div></div>`).join("")}</div><div class="note">Real ads need the Meta Ad Library API. Creatives here are illustrations.</div></div>`;
const weak=CATS.map((c,j)=>({c,d:me.cat[j]-cp.reduce((a,o)=>a+o.cat[j],0)/cp.length})).sort((a,b)=>a.d-b.d).slice(0,3);
const ins=`<div class="card"><h3>AI insights</h3><div id="ai"><b>Summary.</b> ${D.co} scores ${me.Score} against a market average of ${avg.toFixed(1)} (rank ${rank} of ${rows.length}). Top threat: <b>${top[0].name}</b> (score ${top[0].Score}, threat ${top[0].Threat}).</div>
<div class="rec"><b>1.</b> Close the biggest gap: ${weak[0].c} is ${Math.abs(weak[0].d).toFixed(0)} points ${weak[0].d<0?"below":"above"} the competitor average.</div><div class="rec"><b>2.</b> Next gap: ${weak[1].c} (${weak[1].d.toFixed(0)} vs average).</div>
<div class="rec"><b>3.</b> Reputation: your rating is ${me.rating} from ${me.reviews} reviews; ${top[0].name} has ${top[0].rating} from ${top[0].reviews}.</div><div class="rec"><b>4.</b> Paid: ${top[0].name} runs ${top[0].ads} Meta ads vs your ${me.ads}.</div>
<div class="rec"><b>5.</b> Keywords: ${gaps.length} keyword gaps found${gaps[0]?`, biggest "${gaps[0].k}" (${gaps[0].vol.toLocaleString()}/mo)`:""}.</div>
<div style="margin-top:12px"><button class="btn" id="aib">Write AI summary</button> <button class="btn o" id="csv">Export CSV</button> <span id="cs" class="note"></span></div><div class="note">Every point cites a metric above. Data is sample data.</div></div>`;
$("app").innerHTML=`<div class="pn ${TAB==="ov"?"on":""}" id="p-ov">${ov}</div><div class="pn ${TAB==="cp"?"on":""}" id="p-cp">${cpn}</div><div class="pn ${TAB==="kw"?"on":""}" id="p-kw">${kw}</div><div class="pn ${TAB==="ad"?"on":""}" id="p-ad">${ad}</div><div class="pn ${TAB==="in"?"on":""}" id="p-in">${ins}</div>`;
if($("fl"))$("fl").value=fl;
const ys=[...top.slice(0,2),me],ml=["M1","M2","M3","M4","M5","M6"],pc=["#f59e0b","#a855f7","#10e0a0"];
ch("c1",{type:"doughnut",data:{labels:rows.map(o=>o.name.slice(0,16)),datasets:[{data:rows.map(o=>+(o.cat[0]/tot*100).toFixed(1)),backgroundColor:rows.map((o,i)=>i?["#2f8cff","#f59e0b","#a855f7","#94a3b8","#38bdf8","#f472b6","#a3e635","#fb7185","#22d3ee","#e879f9","#facc15","#4ade80","#60a5fa","#fb923c","#c084fc"][i-1]:"#10e0a0"),borderWidth:0}]},options:opt({cutout:"62%",plugins:{legend:{display:false}}})});
ch("c2",{type:"line",data:{labels:ml,datasets:ys.map((o,i)=>({label:o.name.slice(0,18),data:o.rv,borderColor:pc[i],backgroundColor:pc[i]+"22",fill:true,tension:.4}))},options:opt()});
ch("c3",{type:"radar",data:{labels:CATS,datasets:[me,...top.slice(0,2)].map((o,i)=>({label:o.name.slice(0,16),data:o.n.map(Math.round),borderColor:["#10e0a0","#f59e0b","#a855f7"][i],backgroundColor:["#10e0a0","#f59e0b","#a855f7"][i]+"22"}))},options:opt({scales:{r:{ticks:{display:false},pointLabels:{font:{size:9}}}}})});
ch("c4",{type:"bubble",data:{datasets:["You","High","Medium","Low"].map(t=>({label:t,data:rows.filter(o=>o.Threat===t).map(o=>({x:o.cat[0],y:o.cat[1],r:3+o.Score/9,n:o.name})),backgroundColor:COL[t]+"bb"}))},options:opt({scales:{x:{title:{display:true,text:"Search visibility"},min:0,max:100},y:{title:{display:true,text:"Reputation"},min:0,max:100}},plugins:{tooltip:{callbacks:{label:c=>c.raw.n}}}}),plugins:[{afterDraw(c){const{ctx,chartArea:a}=c;ctx.save();ctx.strokeStyle="#2c5560";ctx.setLineDash([4,4]);ctx.beginPath();ctx.moveTo((a.left+a.right)/2,a.top);ctx.lineTo((a.left+a.right)/2,a.bottom);ctx.moveTo(a.left,(a.top+a.bottom)/2);ctx.lineTo(a.right,(a.top+a.bottom)/2);ctx.stroke();ctx.restore()}}]});
ch("c5",{type:"bar",data:{labels:ml,datasets:ys.map((o,i)=>({label:o.name.slice(0,18),data:o.av,backgroundColor:pc[i]}))},options:opt()});
ch("c6",{type:"bar",data:{labels:[...top.slice(0,4),me].map(o=>o.name.slice(0,14)),datasets:[["Positive",d=>Math.round(40+d.rating*10)],["Neutral",()=>20],["Negative",d=>Math.round(60-d.rating*10)]].map(([l,f],i)=>({label:l,data:[...top.slice(0,4),me].map(f),backgroundColor:["#10e0a0","#94a3b8","#f59e0b"][i]}))},options:opt({scales:{x:{stacked:true},y:{stacked:true}}})})}
function run(){D=null;$("ov").classList.add("on");const S=["Resolving business profile...","Finding competitors...","Collecting keywords, ads and reputation signals...","Computing scores..."];$("steps").innerHTML=S.map(s=>`<div class="st">${s}</div>`).join("");
S.forEach((_,i)=>setTimeout(()=>{$("steps").children[i].classList.add("ok");if(i===3)setTimeout(()=>{gen();paint();$("ov").classList.remove("on")},350)},500*(i+1)))}
$("run").onclick=run;$("addb").onclick=()=>{const n=$("add").value.trim();if(!D||!n)return;D.rows.push(mk(D.r,cap(n),"Direct",D.R));D.kw.forEach(k=>k.rk.push(D.R(1,30)));$("add").value="";paint()};
$("tabs").onclick=e=>{const t=e.target.dataset.t;if(!t)return;TAB=t;document.querySelectorAll(".tabs button").forEach(b=>b.classList.toggle("on",b===e.target));document.querySelectorAll(".pn").forEach(p=>p.classList.toggle("on",p.id==="p-"+t))};
$("app").onclick=async e=>{const t=e.target;if(t.dataset.k){SD=SK===t.dataset.k?-SD:-1;SK=t.dataset.k;paint()}
if(t.dataset.rm){const i=D.rows.findIndex(o=>o.name===t.dataset.rm);D.rows.splice(i,1);D.kw.forEach(k=>k.rk.splice(i,1));paint()}
if(t.id==="csv"){const rows=D.rows,csv=["Competitor,Type,Score,Threat,Rating,Reviews,Meta ads,Distance km,Keyword overlap %,"+CATS.join(",")].concat(rows.map(o=>[`"${o.name}"`,o.type,o.Score,o.Threat,o.rating,o.reviews,o.ads,o.dist,o.ov,...o.cat].join(","))).join("\n");
try{const d=await claude.use("downloads");if(!d)throw 0;await d.save({filename:"competitor_analysis.csv",data:csv});$("cs").textContent="Saved."}catch(x){const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));a.download="competitor_analysis.csv";a.click();$("cs").textContent="Export started."}}
if(t.id==="aib"){try{$("ai").textContent="Writing...";const rows=D.rows,me=rows[0],tp=[...rows.slice(1)].sort((a,b)=>b.Score-a.Score).slice(0,3);const r=await askAI([{role:"user",content:`You are a competitor analyst. Using ONLY these sample-data metrics, write a 70-word summary citing metrics. ${D.co}: score ${me.Score}, rating ${me.rating}, reviews ${me.reviews}, ads ${me.ads}. Top rivals: ${tp.map(o=>`${o.name} score ${o.Score} rating ${o.rating} reviews ${o.reviews} ads ${o.ads} threat ${o.Threat}`).join("; ")}.`}]);$("ai").textContent=r.text}catch(x){$("ai").innerHTML+="<div class='note'>AI summary is not available here. The rule-based insights above are shown.</div>"}}};
$("app").onchange=e=>{if(e.target.id==="fl")paint()};
run();
</script></body></html>
'''

components.html(DASHBOARD_HTML.replace("__HF_TOKEN__", HF_TOKEN).replace("__HF_MODEL__", HF_MODEL), height=2400, scrolling=True)