"""Independent hierarchy, approval, shape and synthetic CLI counterexamples."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

OUT=Path(__file__).resolve().parent;BASE=OUT.parent
spec=importlib.util.spec_from_file_location('setup_trust',OUT/'audit_scoped_bindings.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
qc=s.qc;c=s.c
exhaustive=qc.read_json(BASE/'examples'/'synthetic-exhaustive-pass.json');exhaustive['catalogueHash']=qc.digest(c);s.bind(exhaustive)
base=qc.Checker(c,exhaustive).run()
results={'exhaustiveBaseline':base['qualityState']['status']}
for case,as_author in [('storyAuthor',True),('narrowNonAuthor',False)]:
 d=copy.deepcopy(exhaustive);story=next(x for x in d['elements'] if x['elementType']=='user_story');reviewer='narrow-'+case
 if as_author:story['authorId']=reviewer
 d['authorities'].append({'id':reviewer,'kind':'independent_ai','permissions':['quality_review'],'elementIds':[story['id']], 'authoritySource':'SYNTHETIC one-item authority for negative test.'})
 for review in d['reviews']:
  if review['elementId'] is None:review['reviewerId']=reviewer
 s.bind(d);r=qc.Checker(c,d).run();hierarchy=[x for x in r['checks'] if x['elementId'] is None and x['checkId'].startswith('hierarchy.')]
 results[case+'Hierarchy']={'checks':len(hierarchy),'passed':sum(x['status']=='passed' for x in hierarchy),'invalid':sum(x['status']=='invalid' for x in hierarchy)}
d=copy.deepcopy(s.d);reviewer='ancestor-author';story=s.element(d,'user_story-002');story['authorId']=reviewer
d['authorities'].append({'id':reviewer,'kind':'independent_ai','permissions':['quality_review'],'elementIds':['*'],'authoritySource':'Synthetic all-scope record for ancestor-author refusal test.'})
next(x for x in d['reviews'] if x['elementId']=='technical_task-002')['reviewerId']=reviewer
s.bind(d);r=qc.Checker(c,d).run()
results['ancestorAuthorRefused']={'invalid':r['qualityState']['counts']['invalid'],'reasons':[x['reason'] for x in r['checks'] if x['status']=='invalid'][:2]}
before=copy.deepcopy(s.d);before['elements'][0]['approvalStatus']='approved';before['elements'][0]['approvalReference']='Retained authority decision reference'
after=copy.deepcopy(before);after['revision']+=1;after['changeReason']='Proposed changed approved scope';after['elements'][0]['fields']['common.boundary']['value']+=' Revised meaning.'
try:qc.protect_revision(before,after);protected=False
except ValueError:protected=True
results['approvedRewriteRefused']=protected
d=copy.deepcopy(s.d);d['elements'][0]['approvalStatus']='approved';d['elements'][0]['approvalReference']='TBD';s.bind(d);r=qc.Checker(c,d).run()
results['placeholderApproval']={'status':r['qualityState']['status'],'referenceStatus':[x['status'] for x in r['checks'] if x['checkId']=='approval_reference']}
results['placeholderPresence']={x:qc.resolved(x) for x in ('None — no external dependencies (confirmed with platform team)','TBD by product owner','Owner: TBD','Agreed owner: Morgan')}
cyclic=copy.deepcopy(s.d);s.element(cyclic,'technical_task-001')['dependencyIds']=['technical_task-002'];s.element(cyclic,'technical_task-002')['dependencyIds']=['technical_task-001'];s.bind(cyclic)
r=qc.Checker(c,cyclic).run();results['exactCyclePath']=[x['reason'] for x in r['checks'] if x['checkId']=='acyclic_dependencyIds']
design=copy.deepcopy(s.d);s.element(design,'technical_task-001')['designDependencyIds']=['technical_task-002'];s.element(design,'technical_task-002')['designDependencyIds']=['technical_task-001'];s.bind(design)
results['designReferenceCycleDoesNotBlock']=qc.Checker(c,design).run()['qualityState']['status']=='synthetic_checks_satisfied'
with tempfile.TemporaryDirectory(prefix='generic-cli-review-') as directory:
 p=Path(directory)
 def run_case(name,document,allow=False):
  path=p/(name+'.json');qc.write_json(path,document)
  command=[sys.executable,str(BASE/'quality_checker.py'),'check','--document',str(path),'--report',str(p/(name+'-report.json'))]
  if allow:command.append('--allow-synthetic')
  run=subprocess.run(command,capture_output=True,text=True)
  value={'exitCode':run.returncode,'traceback':'Traceback' in run.stderr}
  if run.returncode==0:value['qualityStatus']=json.loads(run.stdout)['qualityState']['status']
  else:
   try:value['error']=json.loads(run.stderr).get('error')
   except json.JSONDecodeError:value['error']=run.stderr[-1000:]
  return value
 malformed_scope=copy.deepcopy(s.d);malformed_scope['scope']='full_hierarchy'
 results['cliCases']={'syntheticWithoutFlag':run_case('synthetic-no-flag',s.d),'syntheticWithFlag':run_case('synthetic-flag',s.d,True),
  'malformedList':run_case('malformed-list',[]),'malformedScope':run_case('malformed-scope',malformed_scope,True)}
results['assertions']={'exhaustiveMechanicalBaselinePasses':results['exhaustiveBaseline']=='synthetic_checks_satisfied',
 'hierarchyAuthorExcluded':results['storyAuthorHierarchy']['invalid']==28 and results['storyAuthorHierarchy']['passed']==0,
 'wholeHierarchyRightsRequired':results['narrowNonAuthorHierarchy']['invalid']==28,
 'ancestorAuthorExcluded':results['ancestorAuthorRefused']['invalid']>0,
 'approvedOriginalPreserved':results['approvedRewriteRefused'],
 'approvalReferencePlaceholderBlocked':'missing' in results['placeholderApproval']['referenceStatus'],
 'confirmedAbsenceNotPlaceholder':results['placeholderPresence']['None — no external dependencies (confirmed with platform team)'],
 'unresolvedOwnersRefused':not results['placeholderPresence']['TBD by product owner'] and not results['placeholderPresence']['Owner: TBD'],
 'cyclePathPresent':bool(results['exactCyclePath']) and 'technical_task-001 -> technical_task-002 -> technical_task-001' in results['exactCyclePath'][0],
 'designCycleDistinct':results['designReferenceCycleDoesNotBlock'],
 'syntheticFlagRequired':results['cliCases']['syntheticWithoutFlag']['exitCode']==3,
 'syntheticStateDistinct':results['cliCases']['syntheticWithFlag'].get('qualityStatus')=='synthetic_checks_satisfied',
 'malformedControlled':all(results['cliCases'][key]['exitCode']==3 and not results['cliCases'][key]['traceback'] for key in ('malformedList','malformedScope'))}
record={'checkerSha256':hashlib.sha256((BASE/'quality_checker.py').read_bytes()).hexdigest(),'catalogueSha256':hashlib.sha256((BASE/'catalogue.json').read_bytes()).hexdigest(),
 'syntheticOnly':True,'results':results,'allAssertionsPassed':all(results['assertions'].values())}
qc.write_json(OUT/'v4-independent-trust-audit.json',record);print(json.dumps(results,indent=2));sys.exit(0 if record['allAssertionsPassed'] else 1)
