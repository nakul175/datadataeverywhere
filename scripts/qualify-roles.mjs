import assert from 'node:assert/strict';
const engineOrigin='http://127.0.0.1:19080';

async function native(path,token,method='GET',body,allowed=[200]){
 const response=await fetch(engineOrigin+path,{method,redirect:'error',signal:AbortSignal.timeout(15000),headers:{...(token?{'xc-auth':token}:{}),...(body?{'content-type':'application/json'}:{})},body:body?JSON.stringify(body):undefined});
 assert.ok(allowed.includes(response.status),`Role fixture ${method} ${path} returned ${response.status}`);
 const text=await response.text();return text?JSON.parse(text):{};
}
export async function prepareRoleFixtures({password,adminToken,baseId,tableId,checks}){
 const privateBase=await native('/api/v2/meta/bases',adminToken,'POST',{title:'Private role qualification'});
 const privateTable=await native(`/api/v2/meta/bases/${privateBase.id}/tables`,adminToken,'POST',{title:'Private role records',table_name:'private_role_records',columns:[{title:'Id',column_name:'id',uidt:'ID',dt:'int4',pk:true,ai:true,rqd:true},{title:'Title',column_name:'title',uidt:'SingleLineText',dt:'text',pv:true},{title:'Notes',column_name:'notes',uidt:'LongText',dt:'text'}]});
 await native(`/api/v2/tables/${privateTable.id}/records`,adminToken,'POST',{Title:'Private role fixture',Notes:'Protected synthetic role value'});
 async function invite(email,base,role){
  const invitation=await native(`/api/v2/meta/bases/${base}/users`,adminToken,'POST',{email,roles:role});
  // With no SMTP configured, the documented native response supplies an offline invite token.
  assert.equal(typeof invitation.invite_token,'string','Isolated offline invitation must return its native token');
  const signup=await native('/api/v1/auth/user/signup',undefined,'POST',{email,password,firstname:'Qualification',lastname:role,token:invitation.invite_token,ignore_subscribe:1});
  assert.equal(typeof signup.token,'string');
  const user=await native('/api/v1/auth/user/me',signup.token);assert.equal(user.email,email);assert.equal(typeof user.id,'string');
  return {email,id:user.id,token:signup.token};
 }
 const viewer=await invite('viewer@example.test',baseId,'viewer');
 const editor=await invite('editor@example.test',privateBase.id,'editor');
 await native(`/api/v2/meta/tables/${tableId}`,viewer.token);
 await native(`/api/v2/tables/${tableId}/records?limit=1`,viewer.token);
 await native(`/api/v2/tables/${tableId}/records`,viewer.token,'POST',{Title:'Forbidden viewer write'},[403]);
 await native(`/api/v2/meta/tables/${privateTable.id}`,viewer.token,'GET',undefined,[403,404]);
 await native(`/api/v2/tables/${privateTable.id}/records?limit=1`,viewer.token,'GET',undefined,[403,404]);
 await native(`/api/v2/meta/tables/${tableId}`,editor.token,'GET',undefined,[403,404]);
 await native(`/api/v2/tables/${privateTable.id}/records`,editor.token,'POST',{Title:'Permitted editor write'});
 checks.push('Actual native offline invitation creates viewer/editor fixtures with base-specific read/write and cross-base denial');
 return {viewer,editor,password,tableId,privateTableId:privateTable.id,revokeViewer:()=>native(`/api/v2/meta/bases/${baseId}/users/${viewer.id}`,adminToken,'DELETE')};
}
export async function qualifyRoleWorkspace({origin,fixtures,checks}){
 async function request(path,cookie,body,allowed=[200]){
  const response=await fetch(origin+path,{method:body?'POST':'GET',redirect:'manual',signal:AbortSignal.timeout(15000),headers:{...(cookie?{cookie}:{}),...(body?{origin,'content-type':'application/json'}:{})},body:body?JSON.stringify(body):undefined});
  assert.ok(allowed.includes(response.status),`Compiled role request ${path.split('?')[0]} returned ${response.status}`);return response;
 }
 async function signin(email){const result=await request('/api/auth/login','',{email,password:fixtures.password});const cookie=result.headers.get('set-cookie');assert.ok(cookie);return cookie.split(';')[0];}
 const path=id=>`/api/workspace?action=records&tableId=${id}`;
 await request(path(fixtures.tableId),'',undefined,[401]);
 await request(path(fixtures.tableId),'dde_session=deliberately-forged-fixture-session',undefined,[401]);
 const viewer=await signin(fixtures.viewer.email);const editor=await signin(fixtures.editor.email);
 await request(path(fixtures.tableId),viewer);
 await request('/api/workspace',viewer,{action:'createRecord',tableId:fixtures.tableId,values:{Title:'Forbidden custom viewer write'}},[403]);
 await request(path(fixtures.privateTableId),viewer,undefined,[403,404]);
 await request(path(fixtures.tableId),editor,undefined,[403,404]);
 await request('/api/workspace',editor,{action:'createRecord',tableId:fixtures.privateTableId,values:{Title:'Permitted compiled editor write'}});
 await request('/api/ai/context',viewer,{tableId:fixtures.tableId},[403]);
 await fixtures.revokeViewer();
 await request(path(fixtures.tableId),viewer,undefined,[403,404]);
 await request('/api/workspace',viewer,{action:'createRecord',tableId:fixtures.tableId,values:{Title:'Forbidden revoked viewer write'}},[403,404]);
 checks.push('Compiled app enforces viewer/editor and cross-base boundaries, forged/missing sessions and separate AI grants');
 checks.push('Removing actual source membership immediately denies the old compiled-app session without cookie replacement');
}
