import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {randomBytes,createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import {mkdtemp,writeFile,rm,mkdir} from 'node:fs/promises';
import {join,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {chromium} from '@playwright/test';
const require=createRequire(resolve('sidecar/package.json'));
const {Client}=require('pg');
const hash=v=>createHash('sha256').update(v).digest('hex');
const canonical=v=>Array.isArray(v)?`[${v.map(canonical).join(',')}]`:v!==null&&typeof v==='object'?`{${Object.entries(v).sort(([a],[b])=>a<b?-1:a>b?1:0).map(([k,val])=>`${JSON.stringify(k)}:${canonical(val)}`).join(',')}}`:JSON.stringify(v);
const quote=v=>`"${v.replaceAll('"','""')}"`;
// Only the explicitly-created synthetic stack is reachable; credentials stay in private files/memory.
export async function qualifyFeeds({settings,table,base,adminToken,checks}) {
 if(process.env.CI!=='true'||process.env.GITHUB_ACTIONS!=='true')throw new Error('Feed integration qualification requires the disposable CI stack.');
 const dir=await mkdtemp(join(tmpdir(),'dde-feeds-qa-'));
 const admin=new Client({host:'127.0.0.1',port:19081,user:'postgres',password:settings.QA_DB_PASSWORD,database:'postgres',connectionTimeoutMillis:5000,query_timeout:10000});
 const rolePassword=randomBytes(32).toString('hex');const origin='http://localhost:3307';
 let child;const summary=[];let apiToken;
 async function native(path,method='GET',body){const r=await fetch('http://127.0.0.1:19080'+path,{method,headers:{...(apiToken?{'xc-token':apiToken}:{'xc-auth':adminToken}),...(body?{'content-type':'application/json'}:{})},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(15000)});assert.equal(r.status,200,`Feed fixture native ${method} ${path} returned ${r.status}`);return r.json();}
 async function request(path,body,credential,status=200,cookie=''){
  const r=await fetch(origin+path,{method:body?'POST':'GET',headers:{...(body?{origin,'content-type':'application/json'}:{}),...(credential?{authorization:`Bearer ${credential}`}:{cookie})},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(60000)});
  assert.equal(r.status,status,`Feed compiled endpoint ${path.split('?')[0]} expected ${status}, observed ${r.status}`);return r.json();
 }
 try {
  await admin.connect();
  table=await native(`/api/v2/meta/bases/${base.id}/tables`,'POST',{title:'Governed feed fixture',table_name:'governed_feed_fixture',columns:[{title:'Id',column_name:'id',uidt:'ID',dt:'int4',pk:true,ai:true,rqd:true},{title:'Title',column_name:'title',uidt:'SingleLineText',dt:'text',pv:true},{title:'Notes',column_name:'notes',uidt:'LongText',dt:'text'},{title:'Secret',column_name:'secret',uidt:'LongText',dt:'text'}]});
  const fixtures=Array.from({length:270},(_,i)=>({Title:`Feed fixture ${i}`,Notes:i<257?'approved':'excluded',Secret:'Protected synthetic field'}));
  for(let i=0;i<fixtures.length;i+=50)await native(`/api/v2/tables/${table.id}/records`,'POST',fixtures.slice(i,i+50));
  const meta=await native(`/api/v2/meta/tables/${table.id}`);
  const title=meta.columns.find(c=>c.title==='Title'),notes=meta.columns.find(c=>c.title==='Notes'),key=meta.columns.find(c=>c.pk);
  assert.ok(title&&notes&&key);
  const matches=await admin.query('SELECT n.nspname,c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE c.relname=$1 AND c.relkind=$2',[meta.table_name,'r']);
  assert.equal(matches.rows.length,1,'Actual NocoDB physical table mapping must be unambiguous');
  const physical=`${quote(matches.rows[0].nspname)}.${quote(matches.rows[0].relname)}`;
  await admin.query(`CREATE SCHEMA dde_feed_fixture`);
  await admin.query(`CREATE VIEW dde_feed_fixture.approved AS SELECT ${quote(key.column_name)},${quote(title.column_name)},${quote(notes.column_name)} FROM ${physical}`);
  await admin.query(`CREATE ROLE dde_feed_reader LOGIN PASSWORD '${rolePassword}' NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE`);
  await admin.query('GRANT USAGE ON SCHEMA dde_feed_fixture TO dde_feed_reader');
  await admin.query('GRANT SELECT ON dde_feed_fixture.approved TO dde_feed_reader');
  const definition=await admin.query("SELECT pg_get_viewdef('dde_feed_fixture.approved'::regclass,true) AS value");
  const pgTypes=await admin.query("SELECT column_name,data_type FROM information_schema.columns WHERE table_schema='dde_feed_fixture' AND table_name='approved'");
  const source={id:'fixture',baseId:base.id,tableId:table.id,policyVersion:'fixture-v1',schema:'dde_feed_fixture',view:'approved',key:key.column_name,delegation:'verified-full-base-admin-only',reviewRef:'CI synthetic mapping to the actual physical NocoDB table',viewDefinitionHash:hash(definition.rows[0].value),fields:[title,notes].map(f=>({id:f.id,column:f.column_name,title:f.title,uidt:f.uidt,pgType:pgTypes.rows.find(p=>p.column_name===f.column_name).data_type}))};
  const tokenResult=await native(`/api/v2/meta/bases/${base.id}/api-tokens`,'POST',{description:'Disposable governed-feed metadata qualification'});apiToken=tokenResult.token;assert.equal(typeof apiToken,'string');
  await writeFile(join(dir,'sources.json'),JSON.stringify([source]),{mode:0o600});
  const dbUrl=new URL('postgresql://127.0.0.1:19081/postgres');dbUrl.username='dde_feed_reader';dbUrl.password=rolePassword;
  child=spawn(process.execPath,[resolve('sidecar/.next/standalone/server.js')],{cwd:resolve('sidecar/.next/standalone'),env:{...process.env,NODE_ENV:'production',PORT:'3307',HOSTNAME:'127.0.0.1',AUTH_MODE:'nocodb',APP_ORIGIN:origin,NOCODB_URL:'http://127.0.0.1:19080',SQLITE_BUDGET_FILE:join(dir,'budget.sqlite'),FEEDS_ENABLED:'true',FEEDS_SOURCES_FILE:join(dir,'sources.json'),FEEDS_STATE_FILE:join(dir,'feeds.sqlite'),FEEDS_DATABASE_URL:dbUrl.href,FEEDS_NOCODB_TOKEN:apiToken,OPENAI_API_KEY:'',ANTHROPIC_API_KEY:'',NEXT_TELEMETRY_DISABLED:'1'},stdio:'ignore'});
  let ready=false;for(let i=0;i<100;i++){try{if((await fetch(origin+'/api/health',{signal:AbortSignal.timeout(500)})).ok){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,100));}assert.ok(ready);
  const login=await fetch(origin+'/api/auth/login',{method:'POST',headers:{origin,'content-type':'application/json'},body:JSON.stringify({email:'qa@example.test',password:settings.QA_ADMIN_PASSWORD}),signal:AbortSignal.timeout(15000)});assert.equal(login.status,200,'Compiled feed fixture login requires its own persistent admission store');const cookie=login.headers.get('set-cookie').split(';')[0];
  const catalog=await request('/api/feeds',undefined,undefined,200,cookie);assert.equal(catalog.sources.length,1,'Actual source role and schema must be verified');
  const grant={source:'fixture',fields:[title.id,notes.id],scope:{kind:'equals',field:notes.id,values:['approved']},consumer:'Synthetic consumer',owner:catalog.owner,expiresAt:new Date(Date.now()+3600000).toISOString()};
  const created=await request('/api/feeds',{action:'create',grant},undefined,200,cookie);const feed=created.feed.id,secret=created.credential;
  const snapshot=await request('/api/feeds',{action:'snapshot',id:feed},undefined,200,cookie);assert.equal(snapshot.manifest.rowCount,257);assert.equal(snapshot.preview.length,10);
  await request('/api/feeds',{action:'resume',id:feed},undefined,200,cookie);
  const rows=[];let page=await request(`/api/feeds/export?feed=${feed}&snapshot=${snapshot.manifest.id}`,undefined,secret);const initialNext=page.next;rows.push(...page.records);
  while(page.next){const replay=await request(`/api/feeds/export?feed=${feed}&cursor=${encodeURIComponent(page.next)}`,undefined,secret);assert.deepEqual(await request(`/api/feeds/export?feed=${feed}&cursor=${encodeURIComponent(page.next)}`,undefined,secret),replay);page=replay;rows.push(...page.records);}
  assert.equal(rows.length,257);assert.equal(new Set(rows.map(r=>r.key)).size,257);assert.equal(hash(rows.map(r=>canonical(r)+'\n').join('')),page.completion.digest);assert.deepEqual(rows.slice(0,10),snapshot.preview);assert.ok(rows.every(r=>Object.keys(r.values).sort().join()===[title.id,notes.id].sort().join()&&r.values[notes.id]==='approved'));assert.ok(!JSON.stringify(rows).includes('Protected synthetic field'));
  summary.push('Actual NocoDB mapping/metadata token and restricted PostgreSQL view export exactly 257 records with matching preview, replay, digest and excluded-field projection');
  await request(`/api/feeds/export?feed=${feed}&snapshot=${snapshot.manifest.id}&fields=Notes`,undefined,secret,400);
  await request(`/api/feeds/export?feed=${feed}&snapshot=${snapshot.manifest.id}`,undefined,undefined,401,cookie);
  await request(`/api/feeds/export?feed=${feed}&cursor=${encodeURIComponent(initialNext+'x')}`,undefined,secret,400);
  await request('/api/feeds',{action:'pause',id:feed},undefined,200,cookie);await request(`/api/feeds/export?feed=${feed}&cursor=${encodeURIComponent(initialNext)}`,undefined,secret,403);await request('/api/feeds',{action:'resume',id:feed},undefined,200,cookie);
  summary.push('Actual compiled consumer route refuses UI-only credentials, excluded fields, cursor tampering and previously admitted cursors after pause');
  // All mutations are on the same native physical table through the supported NocoDB API.
  const original=(await native(`/api/v2/tables/${table.id}/records?limit=1`)).list[0];
  await native(`/api/v2/tables/${table.id}/records`,'PATCH',{[key.title]:original[key.title],[title.title]:'Synthetic feed changed'});
  const added=await native(`/api/v2/tables/${table.id}/records`,'POST',{[title.title]:'Synthetic feed added',[notes.title]:'approved'});
  let newer;
  try{
    newer=await request('/api/feeds',{action:'snapshot',id:feed},undefined,200,cookie);assert.equal(newer.manifest.rowCount,258);
    const diff=await request(`/api/feeds/export?feed=${feed}&snapshot=${newer.manifest.id}&before=${snapshot.manifest.id}`,undefined,secret);assert.equal(diff.records.filter(r=>r.kind==='upsert').length,2);assert.equal(diff.records.filter(r=>r.kind==='remove').length,0);
    assert.deepEqual(await request(`/api/feeds/export?feed=${feed}&snapshot=${newer.manifest.id}&before=${snapshot.manifest.id}`,undefined,secret),diff);
  }finally{await native(`/api/v2/tables/${table.id}/records`,'PATCH',{[key.title]:original[key.title],[title.title]:original[title.title]});await native(`/api/v2/tables/${table.id}/records`,'DELETE',{[key.title]:added[key.title]});}
  const removedSnapshot=await request('/api/feeds',{action:'snapshot',id:feed},undefined,200,cookie);const removals=await request(`/api/feeds/export?feed=${feed}&snapshot=${removedSnapshot.manifest.id}&before=${newer.manifest.id}`,undefined,secret);const removal=removals.records.find(r=>r.kind==='remove');assert.deepEqual(Object.keys(removal).sort(),['key','kind','version']);
  await request(`/api/feeds/export?feed=${feed}&snapshot=${snapshot.manifest.id}`,undefined,secret,409);
  summary.push('Native record writes produce deterministic snapshot upserts/removals; tombstones contain no row values and evicted checkpoints explicitly require restart');
  const rotated=await request('/api/feeds',{action:'rotate',id:feed},undefined,200,cookie);await request(`/api/feeds/export?feed=${feed}&cursor=${encodeURIComponent(initialNext)}`,undefined,secret,403);
  await request('/api/feeds',{action:'snapshot',id:feed},undefined,200,cookie);await request('/api/feeds',{action:'resume',id:feed},undefined,200,cookie);await request('/api/feeds',{action:'revoke',id:feed},undefined,200,cookie);await request('/api/feeds',{action:'resume',id:feed},undefined,409,cookie);
  await request(`/api/feeds/export?feed=${feed}&snapshot=${removedSnapshot.manifest.id}`,undefined,rotated.credential,403);
  const history=await request(`/api/feeds?action=history&id=${feed}`,undefined,undefined,200,cookie);const serialized=JSON.stringify(history);for(const forbidden of [secret,rotated.credential,'Synthetic feed changed',apiToken])assert.ok(!serialized.includes(forbidden));assert.ok(history.events.some(e=>e.action==='snapshot'&&e.evidence));
  summary.push('Rotation/revocation are permanent for old artifacts and protected history contains bounded digest/count evidence without credentials or row payloads');
  const reader=new Client({connectionString:dbUrl.href,connectionTimeoutMillis:5000});await reader.connect();try{await assert.rejects(reader.query(`SELECT * FROM ${physical} LIMIT 1`));await assert.rejects(reader.query('UPDATE dde_feed_fixture.approved SET '+quote(title.column_name)+"='blocked'"));}finally{await reader.end();}
  summary.push('Restricted connector role is denied direct base-table reads and view writes');
  // Slow synthetic view makes the concurrent commit deterministic without production test hooks.
  await admin.query(`CREATE VIEW dde_feed_fixture.slow AS SELECT native.${quote(key.column_name)},native.${quote(title.column_name)},native.${quote(notes.column_name)} FROM ${physical} native CROSS JOIN LATERAL (SELECT pg_sleep(0.004) WHERE native.${quote(key.column_name)} IS NOT NULL) delay`);
  await admin.query('GRANT SELECT ON dde_feed_fixture.slow TO dde_feed_reader');
  const slowDefinition=await admin.query("SELECT pg_get_viewdef('dde_feed_fixture.slow'::regclass,true) AS value");
  const slowSource={...source,id:'slow',view:'slow',viewDefinitionHash:hash(slowDefinition.rows[0].value)};
  await writeFile(join(dir,'sources.json'),JSON.stringify([source,slowSource]),{mode:0o600});
  const slowGrant=await request('/api/feeds',{action:'create',grant:{...grant,source:'slow'}},undefined,200,cookie);
  await admin.query(`CREATE TEMP TABLE dde_feed_titles AS SELECT ${quote(key.column_name)},${quote(title.column_name)} FROM ${physical}`);
  let slowSnapshot;
  try{
    const building=request('/api/feeds',{action:'snapshot',id:slowGrant.feed.id},undefined,200,cookie);
    let extracting=false;
    for(let i=0;i<200;i++){const activity=await admin.query("SELECT 1 FROM pg_stat_activity WHERE application_name='dde-readonly-feed' AND state='active' AND query LIKE 'FETCH FORWARD%' LIMIT 1");if(activity.rows.length){extracting=true;break;}await new Promise(r=>setTimeout(r,25));}
    // Always consume the build promise even if the synchronization precondition fails.
    if(!extracting){await building;throw new Error('Concurrent snapshot fixture did not observe active extraction');}
    await admin.query(`UPDATE ${physical} SET ${quote(title.column_name)}='Concurrent fixture epoch'`);
    slowSnapshot=await building;assert.equal(slowSnapshot.manifest.rowCount,257);
    await request('/api/feeds',{action:'resume',id:slowGrant.feed.id},undefined,200,cookie);
    let p=await request(`/api/feeds/export?feed=${slowGrant.feed.id}&snapshot=${slowSnapshot.manifest.id}`,undefined,slowGrant.credential);const stable=[...p.records];
    while(p.next){p=await request(`/api/feeds/export?feed=${slowGrant.feed.id}&cursor=${encodeURIComponent(p.next)}`,undefined,slowGrant.credential);stable.push(...p.records);}
    assert.equal(stable.length,257);assert.ok(stable.every(r=>r.values[title.id].startsWith('Feed fixture ')),'Concurrent commit must not mix source epochs into the snapshot');
  }finally{await admin.query(`UPDATE ${physical} n SET ${quote(title.column_name)}=o.${quote(title.column_name)} FROM dde_feed_titles o WHERE n.${quote(key.column_name)}=o.${quote(key.column_name)}`);}
  summary.push('Repeatable-read extraction remains one coherent 257-row epoch while a concurrent SQL transaction updates the actual native source table');
  // A definition drift denies an old immutable snapshot too; it cannot freeze authorization.
  await admin.query(`CREATE OR REPLACE VIEW dde_feed_fixture.slow AS SELECT native.${quote(key.column_name)},native.${quote(title.column_name)},native.${quote(notes.column_name)} FROM ${physical} native WHERE FALSE`);
  await request(`/api/feeds/export?feed=${slowGrant.feed.id}&snapshot=${slowSnapshot.manifest.id}`,undefined,slowGrant.credential,409);
  const paused=await request('/api/feeds',undefined,undefined,200,cookie);assert.equal(paused.feeds.find(f=>f.id===slowGrant.feed.id).status,'paused');
  summary.push('SQL-view policy drift pauses the grant and refuses previously valid snapshots');
  const schemaGrant=await request('/api/feeds',{action:'create',grant},undefined,200,cookie);
  const schemaSnapshot=await request('/api/feeds',{action:'snapshot',id:schemaGrant.feed.id},undefined,200,cookie);
  await request('/api/feeds',{action:'resume',id:schemaGrant.feed.id},undefined,200,cookie);
  try{
    await native(`/api/v2/meta/columns/${title.id}`,'PATCH',{title:'Renamed feed Title'});
    await request(`/api/feeds/export?feed=${schemaGrant.feed.id}&snapshot=${schemaSnapshot.manifest.id}`,undefined,schemaGrant.credential,409);
    const changed=await request('/api/feeds',undefined,undefined,200,cookie);const detail=changed.feeds.find(f=>f.id===schemaGrant.feed.id);assert.equal(detail.status,'paused');assert.deepEqual(detail.schemaChange.fields,[title.id]);assert.match(detail.schemaChange.version,/^[a-f0-9]{64}$/);
  }finally{await native(`/api/v2/meta/columns/${title.id}`,'PATCH',{title:title.title});}
  summary.push('Native field rename pauses consumers with a safe field identity, new observed schema fingerprint and explicit reapproval action');
  const browser=await chromium.launch({headless:true});
  try{
    const context=await browser.newContext();await context.addCookies([{name:'dde_session',value:cookie.slice('dde_session='.length),domain:'localhost',path:'/',httpOnly:true,secure:true,sameSite:'Lax'}]);
    const page=await context.newPage();page.setDefaultTimeout(20000);await page.goto(origin+'/feeds');
    await page.getByRole('heading',{name:'Governed data feeds',exact:true}).waitFor();
    await page.getByLabel('Reviewed workspace / table').selectOption('fixture');
    await page.getByLabel(title.title,{exact:true}).check();await page.getByLabel(notes.title,{exact:true}).check();
    await page.getByLabel('Row scope field').selectOption(notes.id);await page.getByLabel('equals',{exact:true}).fill('approved');
    await page.getByLabel('Named consumer').fill('Browser feed fixture');await page.getByLabel('Expiry (within 30 days)').fill(new Date(Date.now()+3600000).toISOString().slice(0,16));
    await page.getByRole('button',{name:'Create paused grant'}).click();await page.getByRole('heading',{name:'Credential shown once'}).waitFor();
    const article=page.locator('article').filter({has:page.getByRole('heading',{name:'Browser feed fixture · paused'})});
    await article.getByRole('button',{name:'Build snapshot & preview'}).click();
    await page.waitForFunction(()=>{const p=document.querySelector('pre');return p&&p.textContent.includes('"rowCount": 257');});
    const preview=JSON.parse(await page.locator('pre').innerText());assert.equal(preview.preview.length,10);assert.equal(preview.completePreview,false);
    await article.getByRole('button',{name:'resume',exact:true}).click();await page.getByRole('heading',{name:'Browser feed fixture · active'}).waitFor();
    const active=page.locator('article').filter({has:page.getByRole('heading',{name:'Browser feed fixture · active'})});await active.getByRole('button',{name:'pause',exact:true}).click();await page.getByRole('heading',{name:'Browser feed fixture · paused'}).waitFor();
    await context.close();
  }finally{await browser.close();}
  summary.push('Chromium administrator selects explicit fields/row scope/consumer/expiry, creates a paused grant, previews the complete snapshot and resumes/pauses sharing');
  checks.push(...summary);
  await mkdir('.quality/evidence',{recursive:true});await writeFile('.quality/evidence/feed-qualification.json',JSON.stringify({status:'scoped_feed_checks_passed',checks:summary,records:257,providerCalls:0,productionAccess:false,limits:'Synthetic same-table source mapping only; no production delegation attestation, 50-user SLA, release acceptance or feed-state recovery guarantee.'},null,2),{mode:0o600});
 }catch(e){await mkdir('.quality/evidence',{recursive:true});await writeFile('.quality/evidence/feed-qualification.json',JSON.stringify({status:'failed',checks:summary,error:(e instanceof Error?e.message:'Feed qualification failed').replaceAll(settings.QA_DB_PASSWORD,'[redacted]').replaceAll(rolePassword,'[redacted]').replaceAll(apiToken||'__absent__','[redacted]').replaceAll(adminToken,'[redacted]').replaceAll(settings.QA_ADMIN_PASSWORD,'[redacted]')},null,2),{mode:0o600});throw new Error('Isolated feed qualification failed; inspect the redacted report.');}
 finally{
  if(child&&child.exitCode===null&&child.signalCode===null){child.kill('SIGTERM');const timer=setTimeout(()=>child.kill('SIGKILL'),5000);await new Promise(r=>child.once('exit',r));clearTimeout(timer);}
  await admin.end().catch(()=>{});await rm(dir,{recursive:true,force:true});
 }
}
