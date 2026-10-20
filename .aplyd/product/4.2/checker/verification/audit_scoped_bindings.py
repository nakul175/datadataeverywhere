"""Independent scoped binding counterexamples using the actual supplied catalogue.

Generated positive verdicts are explicitly synthetic mechanics setup, never a
semantic product review. Production code and bundle files are read-only.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
spec = importlib.util.spec_from_file_location('audit_qc', BASE / 'quality_checker.py')
qc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qc)
c = qc.read_json(BASE / 'catalogue.json')
d = qc.read_json(BASE / 'examples' / 'synthetic-planning-pass.json')
d['catalogueHash'] = qc.digest(c)
d['documentId'] = 'SYNTHETIC-SCOPED-BINDING-AUDIT'
d['elements'] = copy.deepcopy(d['elements'])
mapping = {kind+'-001':kind+'-002' for kind in ('epic','user_story','acceptance_criterion','technical_task')}
for element in list(d['elements']):
    if element['id'] in mapping:
        new = copy.deepcopy(element)
        new['id'] = mapping[element['id']]
        new['parentId'] = mapping.get(element['parentId'],element['parentId'])
        if 'common.id' in new['fields']:
            new['fields']['common.id']['value'] = new['id']
        d['elements'].append(new)
for review in list(d['reviews']):
    if review['elementId'] in mapping:
        new = copy.deepcopy(review)
        new['id'] = new['id']+'-branch2'
        new['elementId'] = mapping[new['elementId']]
        d['reviews'].append(new)
d['evidence'] = []
for element in d['elements']:
    artifact = {'id':'synthetic-evidence-'+element['id'], 'kind':'independent_review_snapshot',
        'description':'SYNTHETIC mechanics evidence for scoped binding audit, not an actual product review.',
        'origin':'Independent local counterexample harness', 'syntheticFixture':True,
        'content':{'label':'SYNTHETIC TEST ONLY','target':element['id'],'method':'No semantic qualification or real approval.'},
        'bindings':[]}
    artifact['contentHash'] = qc.evidence_hash(artifact,'.')
    d['evidence'].append(artifact)
    for review in d['reviews']:
        if review['elementId'] == element['id']:
            review['evidenceIds'] = [artifact['id']]

def bind(doc):
    evidence = {x['id']:x for x in doc['evidence']}
    for item in doc['evidence']:
        item['contentHash'] = qc.evidence_hash(item,'.')
        item['bindings']=[]
    for review in doc['reviews']:
        target = {k:review.get(k) for k in ('elementId','fieldId','checkId')}
        fp = qc.check_subject_fingerprint(doc,c,target['elementId'],target['fieldId'],target['checkId'])
        review.update(bindingVersion='scoped-v1',subjectFingerprint=fp)
        for eid in review['evidenceIds']:
            evidence[eid]['bindings'].append(target | {'bindingVersion':'scoped-v1','subjectFingerprint':fp})
    return doc

def report(doc):
    return qc.Checker(c,doc).run()

def stale_targets(r):
    return sorted(x['id'] for x in r['checks'] if x['status']=='stale')

def element(doc,eid):
    return next(x for x in doc['elements'] if x['id']==eid)

bind(d)
baseline = report(d)
results = {'baseline':{'status':baseline['qualityState']['status'],'reviews':len(d['reviews']),'stale':baseline['qualityState']['counts']['stale']}}
if baseline['qualityState']['status'] not in qc.SUCCESS_STATES:
    results['baselineFailures'] = [{k:x[k] for k in ('id','status','reason')} for x in baseline['checks'] if x['status'] not in ('passed','not_applicable')]
    qc.write_json(OUT/'v4-independent-scoped-audit.json',results)
    print(json.dumps(results,indent=2));sys.exit(1)

changed=copy.deepcopy(d)
element(changed,'technical_task-002')['fields']['common.boundary']['value'] += ' Changed local fixture constraint.'
r=report(changed)
results['localTaskEdit']={'stale':len(stale_targets(r)),'targets':stale_targets(r),'branch1AllPreserved':not any('-001:' in x for x in stale_targets(r)), 'stagePassed':r['qualityState']['status'] in qc.SUCCESS_STATES}
changed=copy.deepcopy(d)
changed['revision']+=1
changed['changeReason']='SYNTHETIC audit metadata update'
changed['questionDecisionVersions']={'unrelated-question':91}
results['auditQuestionMetadataEdit']={'status':report(changed)['qualityState']['status'],'stale':report(changed)['qualityState']['counts']['stale']}
changed=copy.deepcopy(d)
element(changed,'user_story-002')['fields']['common.boundary']['value'] += ' Changed ancestor context.'
results['parentStoryEdit']={'stale':len(stale_targets(report(changed))), 'targets':stale_targets(report(changed))}
changed=copy.deepcopy(d)
element(changed,'technical_task-001')['dependencyIds']=['technical_task-002']
bind(changed)
element(changed,'technical_task-002')['fields']['common.boundary']['value'] += ' Changed referenced prerequisite.'
results['blockingPrerequisiteEdit']={'targets':stale_targets(report(changed)), 'dependentReopened':any('technical_task-001:' in x for x in stale_targets(report(changed)))}
changed=copy.deepcopy(d)
element(changed,'technical_task-001')['designDependencyIds']=['technical_task-002']
bind(changed)
element(changed,'technical_task-002')['fields']['common.boundary']['value'] += ' Changed design reference.'
results['designReferenceEdit']={'targets':stale_targets(report(changed)), 'dependentReopened':any('technical_task-001:' in x for x in stale_targets(report(changed)))}
changed=copy.deepcopy(d)
element(changed,'technical_task-001')['dependencyIds']=['technical_task-002']
bind(changed)
element(changed,'technical_task-001')['dependencyIds']=[]
results['deletedDependencyLink']={'targets':stale_targets(report(changed)), 'dependentReopened':any('technical_task-001:' in x for x in stale_targets(report(changed)))}
changed=copy.deepcopy(d)
changed['evidence'].append({'id':'unused-evidence','kind':'audit_note','description':'SYNTHETIC unused retained evidence.', 'origin':'Synthetic harness','syntheticFixture':True,'content':'Not cited by any review.'})
changed['authorities'].append({'id':'unused-reviewer','kind':'independent_ai','permissions':['quality_review'],'elementIds':['*'],'authoritySource':'Synthetic unused registry.'})
results['unusedEvidenceAuthorityAddition']={'status':report(changed)['qualityState']['status'],'stale':report(changed)['qualityState']['counts']['stale']}
changed=copy.deepcopy(d)
artifact=next(x for x in changed['evidence'] if x['id']=='synthetic-evidence-technical_task-002')
artifact['content']['note']='Revised proof snapshot'
results['citedEvidenceEdit']={'targets':stale_targets(report(changed)), 'onlyTargetAffected':all(x.startswith('technical_task-002:') for x in stale_targets(report(changed)))}
changed=copy.deepcopy(d)
changed['authorities'][0]['authoritySource']+=' Revised authority source.'
results['usedReviewerAuthorityEdit']={'stale':len(stale_targets(report(changed))),'reviews':len(changed['reviews'])}
changed=copy.deepcopy(d)
changed['evidence'][0]['bindings'].append(copy.deepcopy(changed['evidence'][0]['bindings'][0]))
rr=report(changed)
results['duplicateEvidenceBinding']={'status':rr['qualityState']['status'],'invalid':rr['qualityState']['counts']['invalid']}
changed=copy.deepcopy(d)
changed['reviews'][0].pop('bindingVersion')
rr=report(changed)
results['legacyBindingRefused']={'status':rr['qualityState']['status'],'stale':rr['qualityState']['counts']['stale']}

results['assertions']={
 'localTaskPreservesUnrelatedBranch':results['localTaskEdit']['branch1AllPreserved'],
 'localEditDoesNotPass':not results['localTaskEdit']['stagePassed'],
 'metadataDoesNotStale':results['auditQuestionMetadataEdit']['stale']==0,
 'blockingPrerequisiteReopensDependent':results['blockingPrerequisiteEdit']['dependentReopened'],
 'designReferenceReopensDependent':results['designReferenceEdit']['dependentReopened'],
 'deletedLinkReopensDependent':results['deletedDependencyLink']['dependentReopened'],
 'unusedEvidenceAuthorityDoNotStale':results['unusedEvidenceAuthorityAddition']['stale']==0,
 'citedEvidenceIsScoped':results['citedEvidenceEdit']['onlyTargetAffected'] and bool(results['citedEvidenceEdit']['targets']),
 'usedAuthorityReopensAllItsReviews':results['usedReviewerAuthorityEdit']['stale']==len(d['reviews']),
 'duplicateEvidenceBindingRefused':results['duplicateEvidenceBinding']['invalid']>0,
 'legacyBindingRefused':results['legacyBindingRefused']['stale']>0,
}
record={'checkerSha256':hashlib.sha256((BASE/'quality_checker.py').read_bytes()).hexdigest(),'catalogueSha256':hashlib.sha256((BASE/'catalogue.json').read_bytes()).hexdigest(),'syntheticOnly':True,'results':results,'allAssertionsPassed':all(results['assertions'].values())}
qc.write_json(OUT/'v4-independent-scoped-audit.json',record)
if __name__ == '__main__':
    print(json.dumps(results,indent=2))
    sys.exit(0 if record['allAssertionsPassed'] else 1)
