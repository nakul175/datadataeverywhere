"""Independent actual-catalogue queue delivery, regression and archive tests."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import sys

OUT=Path(__file__).resolve().parent
BASE=OUT.parent
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
s=load('scoped_setup',OUT/'audit_scoped_bindings.py');qc=s.qc;c=s.c;d=s.d
ql=load('independent_loop',BASE/'quality_loop.py')
pending=qc.read_json(BASE/'examples'/'synthetic-pending.json');pending['catalogueHash']=qc.digest(c)
rp=qc.Checker(c,pending).run()
p1,state=ql.question_packet(rp,pending,api=qc)
p2,state=ql.question_packet(rp,pending,state,api=qc)
results={'unansweredBatch':{'ownerQuestions':p1['pendingQuestionCount'],'firstBatchId':p1['currentBatchId'],'secondBatchId':p2['currentBatchId'],
 'sameQuestions':[x['id'] for x in p1['nextBatch']]==[x['id'] for x in p2['nextBatch']], 'generationAcknowledged':any(x.get('acknowledgedAt') for x in p2['nextBatch'])}}
changed=copy.deepcopy(d);s.element(changed,'technical_task-002')['fields']['common.boundary']['value']+=' Changed local required constraint.'
stale=qc.Checker(c,changed).run();packet,_=ql.question_packet(stale,changed,api=qc)
results['staleReviewerRouting']={'qualityStatus':stale['qualityState']['status'],'loopStatus':packet['loopStatus'],'ownerQuestions':packet['pendingQuestionCount'],'reviewerTasks':packet['reviewerQueueCount'],'staleChecks':stale['qualityState']['counts']['stale']}
missing=copy.deepcopy(d);missing['reviews'].pop()
packet,_=ql.question_packet(qc.Checker(c,missing).run(),missing,api=qc)
results['missingReviewerRouting']={'ownerQuestions':packet['pendingQuestionCount'],'reviewerTasks':packet['reviewerQueueCount'],'loopStatus':packet['loopStatus']}
failure=copy.deepcopy(d);failure['reviews'][0]['status']='failed'
pf,rs=ql.question_packet(qc.Checker(c,failure).run(),failure,api=qc);qid=pf['nextBatch'][0]['id']
_,rs=ql.question_packet(qc.Checker(c,d).run(),d,rs,api=qc)
failure['revision']+=1;s.bind(failure)
pr,rs=ql.question_packet(qc.Checker(c,failure).run(),failure,rs,api=qc)
results['resolvedRegression']={'oldStatus':rs['questions'][qid]['status'],'pending':pr['pendingQuestionCount'],'nextBatch':len(pr['nextBatch']),
 'newQuestionId':pr['nextBatch'][0]['id'] if pr['nextBatch'] else None,'regressionOf':pr['nextBatch'][0].get('regressionOf') if pr['nextBatch'] else None,
 'occurrence':pr['nextBatch'][0].get('occurrence') if pr['nextBatch'] else None}
with tempfile.TemporaryDirectory(prefix='generic-loop-review-') as directory:
 path=Path(directory)
 ql.write_state(path,state,api=qc)
 ql.acknowledge_batch(path,p2['currentBatchId'],'synthetic-respondent',api=qc)
 current=qc.read_json(path/'loop-state.json')
 p3,current=ql.question_packet(rp,pending,current,api=qc)
 results['acknowledgedBatch']={'newBatchId':p3['currentBatchId'],'previousQuestionsStillAwaiting':len(p3['awaitingAnswerIds']),
  'allPendingRetained':p3['pendingQuestionCount'],'qualityStatus':p3['qualityStatus']}
 ql.write_state(path,current,api=qc)
 answered=p1['nextBatch'][0]['id']
 ql.record_answer(path,answered,'A sourced decision is supplied as information and requires checked revision.','synthetic-respondent',api=qc)
 current=qc.read_json(path/'loop-state.json')
 pa,current=ql.question_packet(rp,pending,current,api=qc)
 results['answerDoesNotPass']={'qualityStatus':pa['qualityStatus'],'answerRetained':current['questions'][answered]['status']=='answered','loopStatus':pa['loopStatus']}
 sizes=[]
 for index in range(45):
  changedpending=copy.deepcopy(pending)
  changedpending['revision']+=index+1
  changedpending['questionDecisionVersions']={'unrelated-question':index+1}
  changedpending['elements'][0]['fields']['common.boundary']['value']='Pending: synthetic context update '+str(index)
  px,current=ql.question_packet(qc.Checker(c,changedpending).run(),changedpending,current,api=qc)
  ql.write_state(path,current,api=qc)
  if index in (15,31,44):sizes.append((index+1,(path/'loop-state.json').stat().st_size))
 archives=list((path/'loop-archive').glob('*.json'))
 head=current.get('archiveHead')
 verified=ql.verify_state(path,current,api=qc)
 results['boundedState']={'bytesAtRuns':sizes,'iterationCount':len(current['iterations']),'maxContextHistory':max(len(x['contextHistory']) for x in current['questions'].values()),
  'archiveFiles':len(archives),'archiveVerified':bool(verified),'headRecords':head.get('totalRecordCount') if head else None,
  'historicalCheckTextRepeated':any('checksToResolve' in x for question in current['questions'].values() for x in question['contextHistory'])}
 before=(path/'loop-state.json').read_bytes()
 archive=archives[0];body=qc.read_json(archive);body['createdAt']='tampered timestamp';qc.write_json(archive,body)
 try:ql.write_state(path,current,api=qc);tamper_refused=False
 except ValueError:tamper_refused=True
 results['archiveTamper']={'refused':tamper_refused,'stateBytesPreserved':before==(path/'loop-state.json').read_bytes()}
malformed=[[],{'questions':[]},{'loopSchemaVersion':'2.0','groups':{'bad':'not-object'}},{'loopSchemaVersion':'2.0','currentBatch':{'id':'batch','questionIds':[{}]}},
 {'loopSchemaVersion':'2.0','groups':{'bad':{'occurrence':'one'}}}]
statuses=[]
for bad in malformed:
 try:ql.question_packet(rp,pending,bad,api=qc);statuses.append('accepted')
 except ValueError:statuses.append('ValueError')
 except Exception as e:statuses.append(type(e).__name__)
results['malformedStates']=statuses
results['assertions']={
 'unansweredBatchRepeats':results['unansweredBatch']['sameQuestions'] and p1['currentBatchId']==p2['currentBatchId'],
 'generationNotAcknowledgement':not results['unansweredBatch']['generationAcknowledged'],
 'staleToReviewerOnly':results['staleReviewerRouting']['ownerQuestions']==0 and results['staleReviewerRouting']['reviewerTasks']==8,
 'missingToReviewerOnly':results['missingReviewerRouting']['ownerQuestions']==0 and results['missingReviewerRouting']['reviewerTasks']==1,
 'regressionReopens':results['resolvedRegression']['pending']==1 and results['resolvedRegression']['regressionOf']==qid,
 'ackStillUnanswered':results['acknowledgedBatch']['previousQuestionsStillAwaiting']==3 and results['acknowledgedBatch']['allPendingRetained']==59,
 'answerNotPass':results['answerDoesNotPass']['qualityStatus'] not in qc.SUCCESS_STATES,
 'historyBounded':results['boundedState']['iterationCount']<=32 and results['boundedState']['maxContextHistory']<=8,
 'noRepeatedHistoricCheckText':not results['boundedState']['historicalCheckTextRepeated'],
 'archiveTamperRefused':all(results['archiveTamper'].values()),
 'malformedStatesControlled':all(x=='ValueError' for x in statuses)}
record={'checkerSha256':hashlib.sha256((BASE/'quality_checker.py').read_bytes()).hexdigest(),'loopSha256':hashlib.sha256((BASE/'quality_loop.py').read_bytes()).hexdigest(),
 'catalogueSha256':hashlib.sha256((BASE/'catalogue.json').read_bytes()).hexdigest(),'syntheticOnly':True,'results':results,'allAssertionsPassed':all(results['assertions'].values())}
qc.write_json(OUT/'v4-independent-loop-audit.json',record);print(json.dumps(results,indent=2));sys.exit(0 if record['allAssertionsPassed'] else 1)
