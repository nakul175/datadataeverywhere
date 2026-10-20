import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {mkdtemp,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {qualifyBrowser} from './qualify-browser.mjs';

// Actual compiled application + the disposable engine, never a production origin.
export async function qualifyWorkspace({password,tableId,baseId}){
 const temporary=await mkdtemp(join(tmpdir(),'dde-engine-app-'));
 const origin='http://localhost:3306';const checks=[];
 await writeFile(join(temporary,'access.json'),JSON.stringify({tables:[],users:{}}),{mode:0o600});
 const app=spawn(process.execPath,[resolve('sidecar/.next/standalone/server.js')],{cwd:resolve('sidecar/.next/standalone'),env:{...process.env,NODE_ENV:'production',PORT:'3306',HOSTNAME:'127.0.0.1',AUTH_MODE:'nocodb',APP_ORIGIN:origin,NOCODB_URL:'http://127.0.0.1:19080',ACCESS_FILE:join(temporary,'access.json'),SQLITE_BUDGET_FILE:join(temporary,'budget.sqlite'),OPENAI_API_KEY:'',ANTHROPIC_API_KEY:'',NEXT_TELEMETRY_DISABLED:'1'},stdio:'ignore'});
 let cookie='';
 async function request(path,body,status=200){
  const response=await fetch(origin+path,{method:body===undefined?'GET':'POST',redirect:'manual',signal:AbortSignal.timeout(15000),headers:{...(cookie?{cookie}:{}),...(body===undefined?{}:{origin,'content-type':'application/json'})},body:body===undefined?undefined:JSON.stringify(body)});
  assert.equal(response.status,status,`Compiled engine journey ${path.split('?')[0]} expected ${status}, observed ${response.status}`);return response;
 }
 try{
  let healthy=false;const deadline=Date.now()+15000;
  while(Date.now()<deadline){try{if((await fetch(origin+'/api/health',{signal:AbortSignal.timeout(Math.min(1000,deadline-Date.now()))})).ok){healthy=true;break;}}catch{}await new Promise(r=>setTimeout(r,100));}
  assert.ok(healthy,'Compiled application starts for actual-engine qualification');
  await request('/api/workspace',undefined,401);
  const login=await request('/api/auth/login',{email:'qa@example.test',password});
  const session=login.headers.get('set-cookie');assert.ok(session);cookie=session.split(';')[0];
  const bases=await(await request('/api/workspace')).json();assert.ok(bases.bases.some(b=>b.id===baseId));
  checks.push('Compiled app signs in to the actual isolated engine and lists its authorized base');
  const all=[];let columns;
  for(let offset=0;offset<300;offset+=50){const page=await(await request(`/api/workspace?action=records&tableId=${tableId}&offset=${offset}`)).json();columns=page.columns;all.push(...page.rows);if(page.page.isLast)break;}
  assert.equal(all.length,257);assert.equal(new Set(all.map(r=>r.Id)).size,257);
  const title=columns.find(c=>c.title==='Title');assert.ok(title);
  for(const [query,expected] of [['Needle','Needle beyond page one'],['Literal_under','Literal_under']]){
   const q=new URLSearchParams({action:'records',tableId,scope:'table',fieldId:title.id,query,sortId:title.id,direction:'desc'});
   const result=await(await request(`/api/workspace?${q}`)).json();assert.equal(result.rows.length,1);assert.equal(result.rows[0].Title,expected);assert.equal(result.page.total,null);
  }
  checks.push('Compiled app reconciles 257 actual rows and applies schema-based full-table and literal queries');
  const target=all.find(r=>r.Title==='Needle beyond page one');assert.ok(target);
  await request('/api/workspace',{action:'updateRecord',tableId,id:target.Id,values:{Notes:'Updated through compiled application'}});
  const updatedQuery=new URLSearchParams({action:'records',tableId,scope:'table',fieldId:title.id,query:'Needle'});
  const updated=await(await request(`/api/workspace?${updatedQuery}`)).json();assert.equal(updated.rows.find(r=>r.Id===target.Id).Notes,'Updated through compiled application');
  await request(`/api/workspace?action=records&tableId=${tableId}&scope=table&where=unsafe`,undefined,400);
  await request('/api/ai/context',{tableId},403);
  checks.push('Compiled app persists an actual edit and refuses raw filters and ungranted AI disclosure');
  checks.push(...await qualifyBrowser({origin,password,baseId}));
  return checks;
 }finally{
  if(app.exitCode===null&&app.signalCode===null){
   app.kill('SIGTERM');const timer=setTimeout(()=>app.kill('SIGKILL'),5000);
   await new Promise(resolve=>app.once('exit',resolve));clearTimeout(timer);
  }
  await rm(temporary,{recursive:true,force:true});
 }
}
