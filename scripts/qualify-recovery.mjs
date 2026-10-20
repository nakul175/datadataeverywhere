import assert from 'node:assert/strict';
import {execFileSync,spawn} from 'node:child_process';
import {readFile,writeFile,mkdir,mkdtemp,cp,rm,symlink,unlink,access} from 'node:fs/promises';
import {homedir,userInfo} from 'node:os';
import {resolve,join} from 'node:path';
import {createHash,randomUUID} from 'node:crypto';
import {DatabaseSync} from 'node:sqlite';

// Destructive fixture operations are intentionally limited to disposable GitHub runners.
assert.equal(process.env.CI,'true');assert.equal(process.env.GITHUB_ACTIONS,'true');process.umask(0o077);
const origin='http://127.0.0.1:19080';const appOrigin='http://localhost:3306';
const settings=Object.fromEntries((await readFile('.qualification/stack.env','utf8')).trim().split('\n').map(l=>l.split('=')));
const fixture=JSON.parse(await readFile('.qualification/fixture.json','utf8'));
const output=resolve('.qualification/recovery');await mkdir(output,{mode:0o700});
const report={status:'running',startedAt:new Date().toISOString(),checks:[],limits:'Synthetic stopped-write fixture only. No agreed RTO/RPO, SMTP delivery, Redis/legacy dashboard, host Caddy/TLS, actual systemd activation, neighboring-service or production recovery acceptance.'};
const hash=value=>createHash('sha256').update(value).digest('hex');
const marker=randomUUID();let root,unit,unitHash,app,token;let managedUnit=false;
const compose=(project,args)=>['compose','--env-file','.qualification/stack.env','-f','docker-compose.qualification.yml','-p',project,...args];
function run(label,command,args,options={}){
 try{return execFileSync(command,args,{timeout:420000,maxBuffer:64*1024*1024,...options});}
 catch(error){try{execFileSync('python3',['-c','import sys; from pathlib import Path; p=Path(sys.argv[1]); p.write_bytes(sys.stdin.buffer.read()); p.chmod(0o600)',join(output,'operation-failure.log')],{input:error.stderr||Buffer.from(label)});}catch{}throw new Error(`Isolated recovery operation failed: ${label}`);}
}
const dc=(project,label,args,options)=>run(label,'docker',compose(project,args),options);
async function api(path,method='GET',body){
 const res=await fetch(origin+path,{method,redirect:'error',signal:AbortSignal.timeout(15000),headers:{...(token?{'xc-auth':token}:{}),...(body&&!(body instanceof FormData)?{'content-type':'application/json'}:{})},body:body?(body instanceof FormData?body:JSON.stringify(body)):undefined});
 assert.ok(res.ok,`Recovery fixture API ${method} ${path.split('?')[0]} returned ${res.status}`);return res.json();
}
async function signin(){const result=await api('/api/v1/auth/user/signin','POST',{email:'qa@example.test',password:settings.QA_ADMIN_PASSWORD});assert.equal(typeof result.token,'string');token=result.token;}
async function rows(id){const result=[];for(let offset=0;offset<1000;offset+=50){const page=await api(`/api/v2/tables/${id}/records?limit=50&offset=${offset}&sort=Id`);assert.ok(Array.isArray(page.list)&&page.list.length<=50);result.push(...page.list);if(page.list.length<50)return result;}throw new Error('Recovery fixture pagination bound exceeded');}
function budget(path){const db=new DatabaseSync(path,{readOnly:true});try{return{usage:db.prepare('SELECT * FROM usage ORDER BY key').all(),leases:db.prepare('SELECT * FROM leases ORDER BY id').all()};}finally{db.close();}}
async function download(item){const href=item.signedPath||item.signedUrl||item.url;assert.equal(typeof href,'string','Native attachment must expose a documented signed path or URL');const url=new URL(href,origin);assert.equal(url.origin,origin,'Fixture attachment must stay on the isolated origin');const result=await fetch(url,{headers:{'xc-auth':token},redirect:'error',signal:AbortSignal.timeout(15000)});assert.ok(result.ok,`Fixture attachment download returned ${result.status}`);return Buffer.from(await result.arrayBuffer());}
async function removeMarkedRoot(){if(!root)return;let value;try{value=await readFile(join(root,'.qualification-marker'),'utf8');}catch{return;}if(value===marker&&root.startsWith(join(homedir(),'.dde-recovery-fixture-')))await rm(root,{recursive:true});}
try{
 const names=run('inspect clean target','docker',['volume','ls','--format','{{.Name}}']).toString().trim().split('\n');
 for(const name of ['dde-recovery-qualification_qa_pg','dde-recovery-qualification_qa_nc'])assert.ok(!names.includes(name),'Refusing an existing recovery data volume');
 unit=join(homedir(),'.config/systemd/user/datadataeverywhere.service');
 try{await access(unit);throw new Error('Recovery fixture refuses an existing service unit');}catch(error){if(error.code!=='ENOENT')throw error;}
 await signin();const before=await rows(fixture.tableId);assert.equal(before.length,257);
 const base=await api('/api/v2/meta/bases','POST',{title:'Recovery attachment fixture'});
 const table=await api(`/api/v2/meta/bases/${base.id}/tables`,'POST',{title:'Recovery files',table_name:'recovery_files',columns:[{title:'Id',column_name:'id',uidt:'ID',dt:'int4',pk:true,ai:true,rqd:true},{title:'Title',column_name:'title',uidt:'SingleLineText',dt:'text',pv:true},{title:'Files',column_name:'files',uidt:'Attachment'}]});
 const attachmentBytes=Buffer.from('DataDataEverywhere synthetic recovery attachment\n');const multipart=new FormData();multipart.append('files',new Blob([attachmentBytes],{type:'text/plain'}),'recovery-fixture.txt');
 const uploaded=await api('/api/v2/storage/upload','POST',multipart);assert.ok(Array.isArray(uploaded)&&uploaded.length===1);
 await api(`/api/v2/tables/${table.id}/records`,'POST',{Title:'Recover this native attachment',Files:uploaded});
 assert.equal(hash(await download((await rows(table.id))[0].Files[0])),hash(attachmentBytes));
 root=await mkdtemp(join(homedir(),'.dde-recovery-fixture-'));await writeFile(join(root,'.qualification-marker'),marker,{mode:0o600});
 const shared=join(root,'shared');await mkdir(shared,{mode:0o700});await mkdir(join(shared,'data'),{mode:0o700});
 await cp('.qualification/unified-runtime/budget.sqlite',join(shared,'data/budget.sqlite'));
 for(const suffix of ['-wal','-shm']){try{await cp('.qualification/unified-runtime/budget.sqlite'+suffix,join(shared,'data/budget.sqlite'+suffix));}catch(error){if(error.code!=='ENOENT')throw error;}}
 await cp('.qualification/unified-runtime/access.json',join(shared,'access.json'));
 const beforeBudget=budget(join(shared,'data/budget.sqlite'));assert.ok(beforeBudget.usage.some(r=>r.key.startsWith('day:')&&r.key.endsWith(':global')&&r.amount===32000));
 await writeFile(join(shared,'runtime.env'),`AUTH_MODE=nocodb\nAPP_ORIGIN=${appOrigin}\nNOCODB_URL=${origin}\nACCESS_FILE=${join(shared,'access.json')}\nSQLITE_BUDGET_FILE=${join(shared,'data/budget.sqlite')}\n`,{mode:0o600});
 const release=join(root,'release');await mkdir(join(release,'.next'),{recursive:true,mode:0o700});await cp('sidecar/.next/standalone',join(release,'.next/standalone'),{recursive:true});await symlink(release,join(root,'current'),'dir');
 const service=`[Unit]\nDescription=Disposable DataDataEverywhere recovery fixture\n[Service]\nWorkingDirectory=${root}/current/.next/standalone\nEnvironmentFile=${shared}/runtime.env\nExecStart=${process.execPath} ${root}/current/.next/standalone/server.js\n`;
 await mkdir(join(homedir(),'.config/systemd/user'),{recursive:true,mode:0o700});await writeFile(unit,service,{flag:'wx',mode:0o600});managedUnit=true;unitHash=hash(service);
 run('archive stopped unified fixture','python3',['scripts/unified-state.py','backup','--root',root,'--user',userInfo().username,'--output',output]);
 dc('dde-qualification','stop source writes',['stop','nocodb']);
 await writeFile(join(output,'postgres.sql'),dc('dde-qualification','dump source PostgreSQL',['exec','-T','postgres','pg_dumpall','-U','postgres']),{mode:0o600});
 await writeFile(join(output,'nocodb.tgz'),dc('dde-qualification','archive source files',['run','--rm','--no-deps','-T','--user','root','--entrypoint','tar','nocodb','-C','/usr/app/data','-czf','-','.']),{mode:0o600});
 const artifacts={};for(const name of ['postgres.sql','nocodb.tgz'])artifacts[name]=hash(await readFile(join(output,name)));await writeFile(join(output,'engine-manifest.json'),JSON.stringify(artifacts),{mode:0o600});
 report.checks.push('Stopped-write PostgreSQL/files plus compiled interface/config/unit and actual SQLite reservation are checksummed privately');
 const restoreStarted=Date.now();
 for(const [name,digest] of Object.entries(artifacts))assert.equal(hash(await readFile(join(output,name))),digest);
 await writeFile('.qualification/recovery-target-created','dde-recovery-qualification',{flag:'wx',mode:0o600});
 dc('dde-recovery-qualification','start clean PostgreSQL',['up','-d','--wait','--wait-timeout','120','postgres']);
 const sql=(await readFile(join(output,'postgres.sql'),'utf8')).replace(/^CREATE ROLE postgres;\r?\n/m,'');
 dc('dde-recovery-qualification','restore PostgreSQL',['exec','-T','postgres','psql','-U','postgres','-v','ON_ERROR_STOP=1','postgres'],{input:sql});
 dc('dde-recovery-qualification','restore native files',['run','--rm','--no-deps','-T','--user','root','--entrypoint','tar','nocodb','-C','/usr/app/data','-xzf','-'],{input:await readFile(join(output,'nocodb.tgz'))});
 await removeMarkedRoot();assert.equal(hash(await readFile(unit)),unitHash);await unlink(unit);
 run('restore unified fixture','python3',['scripts/unified-state.py','restore','--backup',output]);await writeFile(join(root,'.qualification-marker'),marker,{flag:'wx',mode:0o600});
 assert.deepEqual(budget(join(shared,'data/budget.sqlite')),beforeBudget);assert.equal(hash(await readFile(unit)),unitHash);
 dc('dde-recovery-qualification','start recovered engine',['up','-d','--wait','--wait-timeout','360','nocodb']);
 token=undefined;await signin();assert.equal(hash(JSON.stringify(await rows(fixture.tableId))),hash(JSON.stringify(before)));
 const restoredAttachment=(await rows(table.id))[0];assert.equal(hash(await download(restoredAttachment.Files[0])),hash(attachmentBytes));
 report.checks.push('Clean target restores the actual account, 257 exact rows and the native attachment bytes/access');
 const runtime=Object.fromEntries((await readFile(join(shared,'runtime.env'),'utf8')).trim().split('\n').map(l=>{const i=l.indexOf('=');return[l.slice(0,i),l.slice(i+1)];}));
 app=spawn(process.execPath,[join(root,'current/.next/standalone/server.js')],{cwd:join(root,'current/.next/standalone'),env:{...process.env,...runtime,NODE_ENV:'production',PORT:'3306',HOSTNAME:'127.0.0.1',OPENAI_API_KEY:'',ANTHROPIC_API_KEY:''},stdio:'ignore'});
 let healthy=false;const deadline=Date.now()+15000;while(Date.now()<deadline){try{if((await fetch(appOrigin+'/api/health',{signal:AbortSignal.timeout(1000)})).ok){healthy=true;break;}}catch{}await new Promise(r=>setTimeout(r,100));}assert.ok(healthy,'Restored compiled interface starts');
 const login=await fetch(appOrigin+'/api/auth/login',{method:'POST',headers:{origin:appOrigin,'content-type':'application/json'},body:JSON.stringify({email:'qa@example.test',password:settings.QA_ADMIN_PASSWORD}),signal:AbortSignal.timeout(15000)});assert.equal(login.status,200);const cookie=login.headers.get('set-cookie').split(';')[0];
 const page=await fetch(`${appOrigin}/api/workspace?action=records&tableId=${fixture.tableId}`,{headers:{cookie},signal:AbortSignal.timeout(15000)});assert.equal(page.status,200);assert.equal((await page.json()).rows.length,50);
 const viewerLogin=await fetch(appOrigin+'/api/auth/login',{method:'POST',headers:{origin:appOrigin,'content-type':'application/json'},body:JSON.stringify({email:'viewer@example.test',password:settings.QA_ADMIN_PASSWORD}),signal:AbortSignal.timeout(15000)});assert.equal(viewerLogin.status,200);const viewerCookie=viewerLogin.headers.get('set-cookie').split(';')[0];
 const removed=await fetch(`${appOrigin}/api/workspace?action=records&tableId=${fixture.tableId}`,{headers:{cookie:viewerCookie},signal:AbortSignal.timeout(15000)});assert.ok([403,404].includes(removed.status),'Restored removed membership must remain denied');
 assert.ok(budget(join(shared,'data/budget.sqlite')).usage.some(r=>r.key.startsWith('day:')&&r.key.endsWith(':global')&&r.amount===32000));
 report.checks.push('Restored compiled interface authenticates/reads, retains removed-member denial and preserves prior budget/config/unit state');
 report.status='scoped_recovery_checks_passed';report.observedRestoreSeconds=Number(((Date.now()-restoreStarted)/1000).toFixed(3));report.fixtureRows=257;report.providerCalls=0;report.fixtureDataLossObserved=0;
}catch(error){report.status='failed';report.error=(error instanceof Error?error.message:'Recovery failed').replaceAll(settings.QA_ADMIN_PASSWORD,'[redacted-fixture-secret]').replaceAll(token||'__no_token__','[redacted-fixture-token]');process.exitCode=1;}
finally{
 if(app&&app.exitCode===null&&app.signalCode===null){app.kill('SIGTERM');const timer=setTimeout(()=>app.kill('SIGKILL'),5000);await new Promise(r=>app.once('exit',r));clearTimeout(timer);}
 if(managedUnit){try{if(hash(await readFile(unit))===unitHash)await unlink(unit);}catch(error){if(error.code!=='ENOENT'){report.cleanupIssue=true;process.exitCode=1;}}}
 try{await removeMarkedRoot();}catch{report.cleanupIssue=true;process.exitCode=1;}
 report.endedAt=new Date().toISOString();await mkdir('.quality/evidence',{recursive:true});await writeFile('.quality/evidence/recovery-qualification.json',JSON.stringify(report,null,2),{mode:0o600});console.log(JSON.stringify({status:report.status,checks:report.checks.length,providerCalls:0}));
}
