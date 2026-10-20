import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {mkdtemp,writeFile,cp,mkdir,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {fixtureEngine} from '../sidecar/tests/fixtures/engine.mjs';

const root=resolve('.');const temporary=await mkdtemp(join(tmpdir(),'dde-smoke-'));
const origin='http://localhost:3305';const checks=[];const startedAt=new Date().toISOString();
const engine=fixtureEngine();await new Promise((resolve,reject)=>{engine.once('error',reject);engine.listen(0,'127.0.0.1',resolve);});
await writeFile(join(temporary,'access.json'),JSON.stringify({tables:[],users:{}}),{mode:0o600});
await cp(join(root,'sidecar/public'),join(root,'sidecar/.next/standalone/public'),{recursive:true});
await cp(join(root,'sidecar/.next/static'),join(root,'sidecar/.next/standalone/.next/static'),{recursive:true});
const app=spawn(process.execPath,[join(root,'sidecar/.next/standalone/server.js')],{cwd:join(root,'sidecar/.next/standalone'),env:{...process.env,NODE_ENV:'production',PORT:'3305',HOSTNAME:'127.0.0.1',AUTH_MODE:'nocodb',APP_ORIGIN:origin,NOCODB_URL:`http://127.0.0.1:${engine.address().port}`,ACCESS_FILE:join(temporary,'access.json'),SQLITE_BUDGET_FILE:join(temporary,'budget.sqlite'),OPENAI_API_KEY:'',ANTHROPIC_API_KEY:'',NEXT_TELEMETRY_DISABLED:'1'},stdio:['ignore','ignore','ignore']});
let cookie='';
async function request(path,body,expected=200,selectedCookie=cookie){
 const res=await fetch(origin+path,{method:body===undefined?'GET':'POST',redirect:'manual',headers:{...(selectedCookie?{cookie:selectedCookie}:{}),...(body===undefined?{}:{origin,'content-type':'application/json'})},body:body===undefined?undefined:JSON.stringify(body),signal:AbortSignal.timeout(10000)});
 assert.equal(res.status,expected,`${path} expected ${expected}, observed ${res.status}`);return res;
}
async function login(email){const res=await request('/api/auth/login',{email,password:'local-fixture-only'},200,'');return res.headers.get('set-cookie').split(';')[0];}
try{
 let healthy=false;for(let i=0;i<100;i++){try{if((await fetch(origin+'/api/health')).ok){healthy=true;break;}}catch{}await new Promise(r=>setTimeout(r,100));}
 assert.ok(healthy,'Compiled standalone server must become responsive');
 await request('/api/workspace',undefined,401,'');checks.push('Protected workspace refuses missing session');
 await request('/api/auth/login',{email:'owner@example.test',password:'wrong-fixture-password'},401,'');
 cookie=await login('owner@example.test');checks.push('Actual sign-in route validates upstream fixture identity and issues a cookie');
 const bases=await (await request('/api/workspace')).json();assert.equal(bases.bases.length,2);assert.ok(!JSON.stringify(bases).includes('fixture-only-never-real'));checks.push('Workspace response projects titles/IDs without connection metadata');
 const home=await request('/');assert.match(await home.text(),/DataDataEverywhere/);
 const all=[];for(let offset=0;offset<300;offset+=50){const page=await(await request(`/api/workspace?action=records&tableId=t-fixture&offset=${offset}`)).json();all.push(...page.rows);if(page.page.isLast)break;}
 assert.equal(all.length,257);assert.equal(new Set(all.map(r=>r.Id)).size,257);checks.push('Custom route reconciles 257 fixture records over six pages');
 const global=await(await request('/api/workspace?action=records&tableId=t-fixture&scope=table&fieldId=title&query=Needle&sortId=title&direction=desc')).json();assert.equal(global.rows.length,1);assert.equal(global.rows[0].Id,201);assert.equal(global.page.scope,'table');assert.equal(global.page.total,null);checks.push('Full-table query finds a match outside page one and distinguishes scope/count');
 await request('/api/workspace?action=records&tableId=t-fixture&scope=table&where=unsafe',undefined,400);
 await request('/api/workspace',{action:'updateRecord',tableId:'t-fixture',id:201,values:{Calculated:900}},400);checks.push('Raw query syntax and calculated-field writes are refused');
 await request('/api/workspace',{action:'updateRecord',tableId:'t-fixture',id:201,values:{Notes:'Persisted fixture update'}});
 const updated=await(await request('/api/workspace?action=records&tableId=t-fixture&offset=200')).json();assert.equal(updated.rows[0].Notes,'Persisted fixture update');
 const base=await(await request('/api/workspace',{action:'createBase',title:'Smoke workspace'})).json();
 const table=await(await request('/api/workspace',{action:'createTable',baseId:base.id,title:'Smoke table'})).json();
 await request('/api/workspace',{action:'createRecord',tableId:table.id,values:{Title:'Created through compiled app',Notes:'Synthetic only'}});
 const created=await(await request(`/api/workspace?action=records&tableId=${table.id}`)).json();assert.equal(created.rows[0].Title,'Created through compiled app');checks.push('Compiled routes create a workspace/table/record and persist edits in the fixture');
 const reader=await login('reader@example.test');
 await request('/api/workspace?action=records&tableId=t-private',undefined,403,reader);
 await request('/api/workspace',{action:'createRecord',tableId:'t-fixture',values:{Title:'Not allowed'}},403,reader);checks.push('Reader direct requests cannot access a private table or mutate records');
 await request('/api/chat',{tableId:'t-fixture',messages:[{role:'user',parts:[{type:'text',text:'Synthetic only'}]}]},403);
 await request('/api/ai/context',{tableId:'t-fixture'},403);checks.push('Table use never implies an AI grant or provider call');
 const readiness=await(await request('/api/health/ready')).json();assert.equal(readiness.status,'ready');assert.equal(readiness.ai.configured,false);assert.equal(readiness.ai.providerConnectionVerified,false);checks.push('Authenticated dependency readiness separates AI configuration from provider verification');
 const logout=await request('/api/auth/logout',{});assert.match(logout.headers.get('set-cookie'),/Max-Age=0/);cookie='';await request('/api/workspace',undefined,401,'');checks.push('Local logout expires the application cookie; native token revocation is not implied');
 await mkdir('reports',{recursive:true});await writeFile('reports/workspace-smoke.json',JSON.stringify({status:'passed',startedAt,endedAt:new Date().toISOString(),checks,environment:'compiled standalone app plus local test-double engine',limits:'Manual HTTP cookie forwarding; not a real-engine permission, browser cookie, provider, restore or production acceptance run.'},null,2));
 console.log(JSON.stringify({status:'passed',checks:checks.length,records:257,providerCalls:0}));
}catch(e){
 await mkdir('reports',{recursive:true});await writeFile('reports/workspace-smoke.json',JSON.stringify({status:'failed',startedAt,endedAt:new Date().toISOString(),checks,error:e instanceof Error?e.message:'Failed'},null,2));process.exitCode=1;console.error('Workspace smoke failed; inspect the local report.');
}finally{
 if(app.exitCode===null){app.kill('SIGTERM');await new Promise(resolve=>app.once('exit',resolve));}await new Promise(resolve=>engine.close(resolve));await rm(temporary,{recursive:true,force:true});
}
