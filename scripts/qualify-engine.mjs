import {readFile,writeFile,mkdir} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {qualifyWorkspace} from './qualify-workspace.mjs';
import {prepareRoleFixtures} from './qualify-roles.mjs';

const settings=Object.fromEntries((await readFile('.qualification/stack.env','utf8')).trim().split('\n').map(line=>line.split('=')));
const origin='http://127.0.0.1:19080';
const startedAt=new Date().toISOString();
const checks=[];
let token;
async function call(path,method='GET',body){
  const res=await fetch(new URL(path,origin),{method,redirect:'error',signal:AbortSignal.timeout(15000),headers:{...(token?{'xc-auth':token}:{}),...(body?{'content-type':'application/json'}:{})},body:body?JSON.stringify(body):undefined});
  if(!res.ok)throw new Error(`Qualification endpoint ${method} ${path.split('?')[0]} returned ${res.status}`);
  return res.json();
}
try {
  const login=await call('/api/v1/auth/user/signin','POST',{email:'qa@example.test',password:settings.QA_ADMIN_PASSWORD});
  assert.equal(typeof login.token,'string');token=login.token;
  const me=await call('/api/v1/auth/user/me');
  assert.equal(me.email,'qa@example.test');checks.push('Seeded isolated account signs in through v1 and validates /me');
  const base=await call('/api/v2/meta/bases','POST',{title:`Qualification ${Date.now()}`});
  assert.ok(base.id);
  const table=await call(`/api/v2/meta/bases/${base.id}/tables`,'POST',{title:'Qualification records',table_name:'qualification_records',columns:[{title:'Id',column_name:'id',uidt:'ID',dt:'int4',pk:true,ai:true,rqd:true},{title:'Title',column_name:'title',uidt:'SingleLineText',dt:'text',pv:true},{title:'Notes',column_name:'notes',uidt:'LongText',dt:'text'}]});
  assert.ok(table.id);checks.push('Actual engine creates the custom starter base/table schema');
  const schema=await call(`/api/v2/meta/tables/${table.id}`);
  assert.ok(schema.columns.some(c=>c.title==='Id'&&c.pk));
  const fixture=Array.from({length:257},(_,i)=>({Title:i===200?'Needle beyond page one':i===250?'Literal_under':i===251?'LiteralXunder':`Fixture ${String(i).padStart(3,'0')}`,Notes:'Synthetic qualification data only'}));
  for(let i=0;i<fixture.length;i+=50)await call(`/api/v2/tables/${table.id}/records`,'POST',fixture.slice(i,i+50));
  const rows=[];
  for(let offset=0;offset<300;offset+=50){
    const page=await call(`/api/v2/tables/${table.id}/records?limit=50&offset=${offset}&sort=Id`);
    assert.ok(page.list.length<=50);rows.push(...page.list);
    if(page.pageInfo?.isLastPage||page.list.length<50)break;
  }
  assert.equal(rows.length,257);assert.equal(new Set(rows.map(r=>r.Id)).size,257);
  checks.push('257 synthetic engine records reconcile across bounded pages without duplication in the quiescent fixture');
  const q=new URLSearchParams({limit:'50',offset:'0',where:'(Title,like,%Needle%)',sort:'-Title,Id'});
  const filtered=await call(`/api/v2/tables/${table.id}/records?${q}`);
  assert.equal(filtered.list.length,1);assert.equal(filtered.list[0].Title,'Needle beyond page one');
  checks.push('Actual v2 engine finds an authorized match beyond page one using the typed query grammar');
  const literalQuery=new URLSearchParams({limit:'50',where:'(Title,like,%Literal\\_under%)',sort:'Id'});
  const literal=await call(`/api/v2/tables/${table.id}/records?${literalQuery}`);
  assert.equal(literal.list.length,1);assert.equal(literal.list[0].Title,'Literal_under');
  checks.push('Escaped underscore matches the literal character rather than the LIKE wildcard');
  await call(`/api/v2/tables/${table.id}/records`,'PATCH',{Id:filtered.list[0].Id,Notes:'Qualification update'});
  const updated=await call(`/api/v2/tables/${table.id}/records?${q}`);
  assert.equal(updated.list[0].Notes,'Qualification update');checks.push('Single-primary-key PATCH persists on the actual isolated engine');
  await qualifyWorkspace({password:settings.QA_ADMIN_PASSWORD,tableId:table.id,baseId:base.id,checks,roleSetup:async()=>{const fresh=await call('/api/v1/auth/user/signin','POST',{email:'qa@example.test',password:settings.QA_ADMIN_PASSWORD});assert.equal(typeof fresh.token,'string');token=fresh.token;return prepareRoleFixtures({password:settings.QA_ADMIN_PASSWORD,adminToken:token,baseId:base.id,tableId:table.id,checks});}});
  await mkdir('.qualification',{recursive:true,mode:0o700});await writeFile('.qualification/fixture.json',JSON.stringify({baseId:base.id,tableId:table.id}),{mode:0o600});
  const report={status:'scoped_engine_checks_passed',startedAt,endedAt:new Date().toISOString(),environment:'isolated-loopback-dde-qualification',data:'257 synthetic fixture rows',checks,fixtureDigest:createHash('sha256').update(JSON.stringify(fixture)).digest('hex'),limits:'Not a restore, permission-matrix, provider, concurrent-snapshot, 50-user performance or product-acceptance result.'};
  await mkdir('.quality/evidence',{recursive:true});
  await writeFile('.quality/evidence/engine-qualification.json',JSON.stringify(report,null,2),{mode:0o600});
  console.log(JSON.stringify({status:report.status,checks:checks.length,records:257}));
} catch(e) {
  await mkdir('.quality/evidence',{recursive:true});
  await writeFile('.quality/evidence/engine-qualification.json',JSON.stringify({status:'failed',startedAt,endedAt:new Date().toISOString(),checks,error:(e instanceof Error?e.message:'Qualification failed').replaceAll(settings.QA_ADMIN_PASSWORD,'[redacted-fixture-secret]').replaceAll(token||'__no_token__','[redacted-fixture-token]'),networkCode:typeof e?.cause?.code==='string'?e.cause.code:null},null,2),{mode:0o600});
  console.error('Isolated engine qualification failed; inspect the private evidence report. No production data was used.');
  process.exitCode=1;
}
