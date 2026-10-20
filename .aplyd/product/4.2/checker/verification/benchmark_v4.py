"""302-item synthetic scale and real-advisory metadata-binding counterexamples."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

OUT=Path(__file__).resolve().parent
BASE=OUT.parent
spec=importlib.util.spec_from_file_location('bench_qc',BASE/'quality_checker.py')
qc=importlib.util.module_from_spec(spec);spec.loader.exec_module(qc)
c=qc.read_json(BASE/'catalogue.json')
original=qc.read_json(BASE/'examples'/'synthetic-planning-pass.json')
d=copy.deepcopy(original)
d.update(documentId='SYNTHETIC-302-ITEM-SCALE-AUDIT',catalogueHash=qc.digest(c),elements=[],reviews=[],evidence=[])
templates={item['elementType']:item for item in original['elements']}
counts={'vision':1,'strategy':1,'roadmap':1,'release_goal':1,'epic':8,'user_story':40,'acceptance_criterion':150,'technical_task':100}
def eid(kind,index):return kind+'-%03d'%index
for kind,count in counts.items():
 for index in range(1,count+1):
  element=copy.deepcopy(templates[kind]);element['id']=eid(kind,index)
  if kind=='vision':parent=None
  elif kind=='strategy':parent=eid('vision',1)
  elif kind=='roadmap':parent=eid('strategy',1)
  elif kind=='release_goal':parent=eid('roadmap',1)
  elif kind=='epic':parent=eid('release_goal',1)
  elif kind=='user_story':parent=eid('epic',(index-1)//5+1)
  else:parent=eid('user_story',(index-1)%40+1)
  element['parentId']=parent
  if 'common.id' in element['fields']:element['fields']['common.id']['value']=element['id']
  d['elements'].append(element)
selection=qc.assessment_selection(c,d)
for element in d['elements']:
 artifact={'id':'synthetic-proof-'+element['id'],'kind':'mechanics_fixture','description':'SYNTHETIC scale fixture only: generated verdicts measure mechanics, not quality.',
  'origin':'Independent local scale harness','syntheticFixture':True,'content':{'label':'SYNTHETIC TEST ONLY','item':element['id']},'bindings':[]}
 artifact['contentHash']=qc.evidence_hash(artifact,'.');d['evidence'].append(artifact)
 for gate in selection['checks'][element['elementType']]:
  d['reviews'].append({'id':'synthetic-review-%04d'%len(d['reviews']),'elementId':element['id'],'fieldId':None,'checkId':gate['id'],'status':'passed','reviewerId':'fixture-reviewer',
   'independent':True,'evidenceIds':[artifact['id']],'rationale':'SYNTHETIC GENERATED VERDICT: mechanics fixture setup, not independent product assessment.'})

def bind(doc):
 evidence={x['id']:x for x in doc['evidence']}
 for item in doc['evidence']:item['contentHash']=qc.evidence_hash(item,'.');item['bindings']=[]
 for review in doc['reviews']:
  target={k:review.get(k) for k in ('elementId','fieldId','checkId')}
  fp=qc.check_subject_fingerprint(doc,c,*target.values())
  review.update(bindingVersion='scoped-v1',subjectFingerprint=fp)
  for item in review['evidenceIds']:evidence[item]['bindings'].append(target|{'bindingVersion':'scoped-v1','subjectFingerprint':fp})
 return doc

t0=time.perf_counter();bind(d);bind_seconds=time.perf_counter()-t0
t0=time.perf_counter();r=qc.Checker(c,d).run();check_seconds=time.perf_counter()-t0
changed=copy.deepcopy(d)
next(x for x in changed['elements'] if x['id']=='technical_task-100')['fields']['common.boundary']['value']+=' Changed local synthetic leaf requirement.'
t0=time.perf_counter();rr=qc.Checker(c,changed).run();edit_seconds=time.perf_counter()-t0
stale=[x for x in rr['checks'] if x['status']=='stale']
related={x['elementId'] for x in stale}
results={'scale':{'syntheticOnly':True,'elements':len(d['elements']),'countsByLevel':counts,'reviewVerdicts':len(d['reviews']),'blockingChecks':len(r['checks']),
 'baselineStatus':r['qualityState']['status'],'bindingSeconds':round(bind_seconds,3),'checkingSeconds':round(check_seconds,3),'leafEditCheckingSeconds':round(edit_seconds,3),
 'reportCanonicalBytes':len(qc.canonical(r).encode('utf-8')),'leafEditStaleReviews':len(stale),'leafEditAffectedElements':sorted(related),
 'unchangedReviewsPreserved':len(d['reviews'])-len(stale),'wholeUnrelatedBranchPreserved':not any(x['elementId'] in {eid('epic',1),*[eid('user_story',i) for i in range(1,6)]} for x in stale)}}
# Real advisory mode with supplied synthetic-shaped registry/evidence. This
# measures receipt consistency, not genuine authority or evidence authenticity.
small=copy.deepcopy(original);small['catalogueHash']=qc.digest(c)
small['mode']='real'
for artifact in small['evidence']:artifact['syntheticFixture']=False
bind(small)
trust={'catalogueHash':qc.digest(c),'sourcePins':copy.deepcopy(small['sourcePins']),'authorities':copy.deepcopy(small['authorities']),
 'reviewVerifications':[{'bindingVersion':'scoped-v1','subjectFingerprint':qc.review_set_fingerprint(small,c),'verificationMethod':'independent_agent_review','independent':True,
  'verifierId':'fixture-reviewer','reviewHashes':sorted(qc.digest(x) for x in small['reviews']),
  'verificationRecord':'SYNTHETIC supplied offline record for receipt-consistency mechanics, not actual authority.'}]}
before=qc.Checker(c,small,trust_store=trust).run()
meta=copy.deepcopy(small);meta['revision']+=1;meta['changeReason']='Synthetic queue-only audit edit';meta['questionDecisionVersions']={'unrelated-question':47}
after=qc.Checker(c,meta,trust_store=trust).run()
sourcechange=copy.deepcopy(small);sourcechange['sources'][0]['text']+=' Altered source requirement.';sourcechange['sourcePins'][sourcechange['sources'][0]['id']]=qc.source_hash(sourcechange['sources'][0])
invalid=qc.Checker(c,sourcechange,trust_store=trust).run()
results['realAdvisoryReceipt']={'baselineStatus':before['qualityState']['status'],'metadataOnlyStatus':after['qualityState']['status'],'metadataOnlyStale':after['qualityState']['counts']['stale'],
 'identityAuthenticated':after['reviewerAuthentication']['status'],'advisoryOnly':after['reviewerAuthentication']['advisoryOnly'],'certificationGranted':after['qualityState']['certificationGranted'],
 'sourceChangeStatus':invalid['qualityState']['status'],'sourceChangeStale':invalid['qualityState']['counts']['stale'],
 'metadataReceiptCurrent':next(x['status'] for x in after['checks'] if x['checkId']=='external_review_verification'),
 'sourceBaselineRefused':any(x['checkId']=='external_source_baseline' and x['status']=='stale' for x in invalid['checks'])}
results['assertions']={'302ItemsAnd2114Verdicts':len(d['elements'])==302 and len(d['reviews'])==2114,
 'baselineSyntheticMechanicsSatisfied':r['qualityState']['status']=='synthetic_checks_satisfied',
 'leafEditOnly8Reviews':len(stale)==8,'unrelatedBranchPreserved':results['scale']['wholeUnrelatedBranchPreserved'],
 'realMetadataDoesNotStale':after['qualityState']['counts']['stale']==0 and results['realAdvisoryReceipt']['metadataReceiptCurrent']=='passed',
 'realStillAdvisory':after['reviewerAuthentication']['advisoryOnly'] and not after['qualityState']['certificationGranted'],
 'sourceChangeRefused':invalid['qualityState']['status'] not in qc.SUCCESS_STATES and results['realAdvisoryReceipt']['sourceBaselineRefused']}
record={'checkerSha256':hashlib.sha256((BASE/'quality_checker.py').read_bytes()).hexdigest(),'catalogueSha256':hashlib.sha256((BASE/'catalogue.json').read_bytes()).hexdigest(),
 'results':results,'allAssertionsPassed':all(results['assertions'].values())}
qc.write_json(OUT/'v4-independent-scale-audit.json',record);print(json.dumps(results,indent=2));sys.exit(0 if record['allAssertionsPassed'] else 1)
