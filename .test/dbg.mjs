import fs from "node:fs"; import path from "node:path";
import jsdomPkg from "jsdom"; const { JSDOM, VirtualConsole, requestInterceptor } = jsdomPkg;
const ROOT = path.resolve("..");
const vc = new VirtualConsole();
vc.on("jsdomError", e => console.log("JSDOM-ERR:", e.message));
vc.on("log", (...a) => console.log("console.log:", ...a));
const dom = new JSDOM(fs.readFileSync(path.join(ROOT,"index.html"),"utf8"), {
  url:"http://localhost:8000/", runScripts:"dangerously", virtualConsole: vc, pretendToBeVisual:true,
  resources:{ interceptors:[requestInterceptor(r=>{ const rel=new URL(r.url).pathname.replace(/^\//,""); const f=path.join(ROOT,rel);
    return fs.existsSync(f)&&!fs.statSync(f).isDirectory() ? new Response(fs.readFileSync(f),{status:200,headers:{"Access-Control-Allow-Origin":"*"}}) : new Response("x",{status:404}); })] }});
await new Promise(r=>setTimeout(r,800));
const d=dom.window.document;
console.log("TITLE:", JSON.stringify(d.getElementById("course-title").textContent));
d.querySelector('[data-mode="cards"]').click();
console.log("VIEW HTML:\n", d.getElementById("view").innerHTML.slice(0,1400));
