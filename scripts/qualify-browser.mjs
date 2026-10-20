import assert from 'node:assert/strict';
import {chromium,expect} from '@playwright/test';
import {mkdir} from 'node:fs/promises';

// No traces, videos, storage-state exports or credential output.
export async function qualifyBrowser({origin,password,baseId,email='qa@example.test',checks=[]}){
 const browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage();page.setDefaultTimeout(15000);
 const ready=()=>expect(page.locator('.grid-scroll')).toHaveAttribute('aria-busy','false');
 let releaseSave;
 try{
  await page.goto(origin+'/signin');
  await page.getByLabel('Email address').fill(email);
  await page.getByLabel('Password',{exact:true}).fill('deliberately-wrong-fixture-password');
  await page.getByRole('button',{name:/make sense/}).click();
  await expect(page.locator('.error[role=alert]')).toContainText('not accepted');
  await page.getByLabel('Password',{exact:true}).fill(password);
  await page.getByRole('button',{name:/make sense/}).click();
  await expect(page.getByRole('button',{name:'Sign out',exact:true})).toBeVisible();
  const cookie=(await context.cookies()).find(c=>c.name==='dde_session');assert.ok(cookie?.httpOnly&&cookie?.secure&&cookie?.sameSite==='Lax');
  await page.getByLabel('Workspace',{exact:true}).selectOption(baseId);await ready();
  checks.push('Chromium signs in after an invalid attempt using the actual Secure/HttpOnly/SameSite cookie');
  await expect(page.locator('.data-grid tbody tr')).toHaveCount(50);
  await page.getByLabel('Search this page',{exact:true}).fill('Needle');await expect(page.locator('.data-grid tbody tr')).toHaveCount(0);await expect(page.getByText('No matches on this page.',{exact:true})).toBeVisible();
  await page.getByLabel('Search this page',{exact:true}).fill('');await expect(page.locator('.data-grid tbody tr')).toHaveCount(50);
  await page.getByLabel('Sort this page by',{exact:true}).selectOption('Title');await page.getByRole('button',{name:'Sort descending',exact:true}).click();
  await expect(page.locator('.data-grid tbody tr').first().locator('td').nth(2)).toHaveText('Fixture 049');await page.getByLabel('Sort this page by',{exact:true}).selectOption('');
  const ids=[];
  for(let n=1;n<=6;n++){
   await ready();await expect(page.locator('.grid-footer')).toContainText(`Page ${n}`);
   ids.push(...await page.locator('.data-grid tbody tr').evaluateAll(rows=>rows.map(r=>r.children[1].textContent.trim())));
   if(n<6)await Promise.all([page.waitForResponse(response=>{const q=new URL(response.url());return q.pathname==='/api/workspace'&&q.searchParams.get('action')==='records'&&q.searchParams.get('offset')===String(n*50);}),page.getByRole('button',{name:'Next →',exact:true}).click()]);
  }
  assert.equal(ids.length,257);assert.equal(new Set(ids).size,257);await expect(page.getByRole('button',{name:'Next →',exact:true})).toBeDisabled();
  await expect(page.getByLabel('Search this page',{exact:true})).toBeVisible();await expect(page.getByLabel('Sort this page by',{exact:true})).toBeVisible();
  await page.getByText('Search or sort the entire table',{exact:true}).click();
  await page.getByLabel('Full-table search field').selectOption({label:'Title'});
  await page.getByLabel('Full-table search text').fill('Needle');
  await page.getByRole('button',{name:'Apply table query',exact:true}).click();await ready();
  await expect(page.locator('.data-grid tbody tr')).toHaveCount(1);await expect(page.locator('.data-grid')).toContainText('Needle beyond page one');
  checks.push('Browser reconciles all 257 rows over six pages and distinguishes full-table from page-local queries');
  const trigger=page.getByRole('button',{name:/New workspace/});await trigger.click();
  const dialog=page.getByRole('dialog');await expect(dialog.getByLabel('Workspace name')).toBeFocused();
  await dialog.getByRole('button',{name:'Create',exact:true}).focus();await page.keyboard.press('Tab');await expect(dialog.getByRole('button',{name:'Close dialog'})).toBeFocused();
  await page.keyboard.press('Shift+Tab');await expect(dialog.getByRole('button',{name:'Create',exact:true})).toBeFocused();
  await page.keyboard.press('Escape');await expect(dialog).toHaveCount(0);await expect(trigger).toBeFocused();
  checks.push('Dialog Tab/Shift+Tab wraps, Escape cancels and focus returns to its trigger');
  await trigger.click();await dialog.getByLabel('Workspace name').fill('Browser qualification');await dialog.getByRole('button',{name:'Create',exact:true}).click();await expect(dialog).toHaveCount(0);
  await page.getByRole('button',{name:'Create table',exact:true}).click();await dialog.getByLabel('Table name').fill('Browser records');await dialog.getByRole('button',{name:'Create',exact:true}).click();await expect(dialog).toHaveCount(0);await ready();
  await page.getByRole('button',{name:/Add record/}).click();await dialog.getByLabel('Title',{exact:true}).fill('Browser created record');await dialog.getByLabel('Notes',{exact:true}).fill('Created in Chromium');
  let saveStarted;const started=new Promise(resolve=>saveStarted=resolve);const blocked=new Promise(resolve=>releaseSave=resolve);
  await page.route('**/api/workspace',async route=>{
   if(route.request().method()==='POST'&&route.request().postDataJSON()?.action==='createRecord'){saveStarted();await blocked;}
   await route.continue();
  });
  await dialog.getByRole('button',{name:'Save record'}).click();
  let startTimer;try{await Promise.race([started,new Promise((_,reject)=>{startTimer=setTimeout(()=>reject(new Error('Browser save did not issue a create request within 15 seconds')),15000);})]);}finally{clearTimeout(startTimer);}
  await expect(dialog.getByRole('button',{name:'Close dialog'})).toBeDisabled();await expect(dialog.getByRole('button',{name:'Cancel',exact:true})).toBeDisabled();await page.keyboard.press('Escape');await expect(dialog).toBeVisible();await page.locator('.modal-shade').click({position:{x:5,y:5}});await expect(dialog).toBeVisible();
  releaseSave();await expect(dialog).toHaveCount(0);await page.unroute('**/api/workspace');await ready();await expect(page.locator('.data-grid')).toContainText('Browser created record');
  checks.push('Browser creates workspace/table/record; pending save prevents dismissal and persists through the configured engine');
  await page.getByRole('button',{name:'Edit record 1',exact:true}).click();await dialog.getByRole('button',{name:'Save record'}).click();await expect(dialog.getByRole('alert')).toContainText('No changed fields');
  await dialog.getByLabel('Notes',{exact:true}).fill('Browser persisted edit');await dialog.getByRole('button',{name:'Save record'}).click();await expect(dialog).toHaveCount(0);await page.reload();await page.getByLabel('Workspace',{exact:true}).selectOption({label:'Browser qualification'});await expect(page.getByRole('heading',{name:'Browser records',exact:true})).toBeVisible();await ready();await expect(page.locator('.data-grid')).toContainText('Browser persisted edit');
  await page.getByRole('button',{name:'Edit record 1',exact:true}).click();await dialog.getByLabel('Notes',{exact:true}).fill('Unsaved after refusal');
  await page.route('**/api/workspace',route=>route.request().method()==='POST'?route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({error:'Controlled fixture save refusal'})}):route.continue());
  await dialog.getByRole('button',{name:'Save record'}).click();await expect(dialog.getByRole('alert')).toContainText('Controlled fixture save refusal');await expect(dialog.getByLabel('Notes',{exact:true})).toHaveValue('Unsaved after refusal');await page.unroute('**/api/workspace');await dialog.getByRole('button',{name:'Cancel',exact:true}).click();
  checks.push('Reload retains edits; empty and upstream-rejected saves remain correctable without false success');
  await page.setViewportSize({width:390,height:844});
  await page.getByRole('button',{name:'Toggle navigation'}).click();await expect(page.getByLabel('Workspace',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:/Browser records/}).click();await expect(page.getByLabel('Workspace',{exact:true})).not.toBeVisible();
  if(await page.getByRole('button',{name:'Close AI panel'}).isVisible())await page.getByRole('button',{name:'Close AI panel'}).click();
  await page.getByRole('button',{name:/Ask your data/}).click();await expect(page.getByRole('button',{name:'Close AI panel'})).toBeVisible();await page.getByRole('button',{name:'Close AI panel'}).click();
  checks.push('Narrow viewport navigation opens/selects/closes and the AI panel has a usable close control');
  await page.goto(origin+'/?browser-history=1');await ready();
  await page.route('**/api/auth/logout',route=>route.fulfill({status:503,contentType:'application/json',body:'{}'}));await page.getByRole('button',{name:'Sign out',exact:true}).click();await expect(page.locator('.error[role=alert]')).toContainText('Unable to sign out');await page.unroute('**/api/auth/logout');
  await page.route('**/api/auth/logout',route=>route.abort('failed'));await page.getByRole('button',{name:'Sign out',exact:true}).click();await expect(page.locator('.error[role=alert]')).toContainText('Unable to sign out');await page.unroute('**/api/auth/logout');
  await page.getByRole('button',{name:'Sign out',exact:true}).click();await expect(page).toHaveURL(origin+'/signin');assert.ok(!(await context.cookies()).some(c=>c.name==='dde_session'));
  await page.goBack();await expect(page).toHaveURL(origin+'/signin');
  const denied=await context.request.get(origin+'/api/workspace');assert.equal(denied.status(),401);
  await page.setViewportSize({width:1440,height:1000});
  await page.getByLabel('Email address').fill(email);await page.getByLabel('Password',{exact:true}).fill(password);await page.getByRole('button',{name:/make sense/}).click();await expect(page.getByRole('button',{name:'Sign out',exact:true})).toBeVisible();await page.getByLabel('Workspace',{exact:true}).selectOption({label:'Browser qualification'});await expect(page.getByRole('heading',{name:'Browser records',exact:true})).toBeVisible();await ready();await expect(page.locator('.data-grid')).toContainText('Browser persisted edit');
  checks.push('Logout failure is retryable, successful logout expires cookies/browser-back access, and re-login retains data');
  return checks;
 }catch(error){
  try{await mkdir('.quality/evidence',{recursive:true});await page.screenshot({path:'.quality/evidence/browser-failure.png',timeout:3000,mask:[page.locator('input[type=password]')]});}catch{}
  throw error;
 }finally{releaseSave?.();await context.close();await browser.close();}
}
