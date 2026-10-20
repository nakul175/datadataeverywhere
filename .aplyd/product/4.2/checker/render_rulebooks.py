#!/usr/bin/env python3
"""Render local generic stage gates and field components using explicit UTF-8."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent
NAMES={'common':'Shared fields and integrity/reference rules','vision':'Product vision','strategy':'Product strategy','roadmap':'Roadmap','release_goal':'Release goal','epic':'Epic','user_story':'User story','acceptance_criterion':'Acceptance criterion','technical_task':'Implementation or verification task'}

def rule(q):
    return '\n'.join(['**'+q['id']+'** · '+q['dimension']+' · '+q['mode']+' · '+q['severity'],'','- **Pass:** '+q['passCriterion'],'- **Evidence:** '+q['evidenceRequirement'],''])

def main():
    c=json.loads((ROOT/'catalogue.json').read_text(encoding='utf-8'))
    if c.get('status')!='complete_generic_catalogue_not_product_pass':
        raise SystemExit('Only a completed generic catalogue may be published.')
    out=ROOT/'publication';out.mkdir(exist_ok=True);summary=[]
    for typ,name in NAMES.items():
        fields=[f for f in c['fields'] if f['element']==typ]
        gates=[g for g in c.get('profileChecks',[]) if typ in g.get('applicable_types',[])]
        lines=['# Generic product management quality rules — '+name,'',
            'Catalogue '+c['catalogueVersion']+' · schema '+c['schemaVersion']+'. Generic framework, not certification of a particular product plan.','',
            'Default review uses seven unsampled must-pass gates per item for its current stage plus mandatory automatic integrity checks. Up to two deterministic noncritical field-rule targets per hierarchy level across all assessed items are advisory samples; PASS never claims unsampled detailed coverage. Exhaustive reference review is optional and its workload is disclosed.','',
            'Applicable AI, safety, security, privacy, access, accessibility, protected requirements and actual authority remain in mandatory gates and cannot be sampled away. Unknown necessary applicability, rights, evidence or authority is unresolved. No invented owner, target, size, approval, consent or observation clears a check.','',
            'Locally declared offline reviewers are advisory only; authoritative review requires an externally administered, verified reviewer registry. Quality, actual approval, readiness, acceptance, authorised publication, observed availability, user verification and outcome learning remain separate.','']
        if gates:
            lines+=['## Seven current-stage must-pass gates','']
            for stage,profile in c['review_profiles']['stages'].items():
                lines+=['### '+stage.title(),' ',profile['description'],'']
                for q in [g for g in gates if g['profile_stage']==stage]:
                    lines+=['#### '+q['title'],'',rule(q),'- **Required fields:** '+', '.join(q['requiredFieldIds'])+'.']
                    if q.get('conditionalFieldIds'):
                        lines+=['- **Conditional field branches:** '+json.dumps(q['conditionalFieldIds'],sort_keys=True)+'.']
                    lines+=['']
        lines+=['## Required field content components','',
                str(len(fields))+' owning fields. Listed components are content within their parent field, not independent checks or verdicts. Apply the selected stage requirements and factual exclusions. Shared fields also apply to each hierarchy level.','']
        for f in fields:
            source=f.get('source',{});req=f['requiredness']
            lines+=['### '+f['id']+' — '+f['label'],'','**Purpose:** '+f['purpose'],'',
                    '**Applicability:** '+req['policy']+' — '+req['condition'],'',
                    '**Source:** '+source.get('heading','')+' · source line '+str(source.get('line',''))+'.','',
                    '**Required components (one field assessment):**','']
            lines += ['- '+d['id']+' — '+d['label'] for d in f['details']]
            lines+=['']
        lines+=['## Detailed reference rules — advisory sampling or opt-in exhaustive inspection','',
                'These rules are available for deeper inspection and specific repairs. They are not extra default must-pass review verdicts. Passing the stage profile does not assert exhaustive reference-rule certification.','']
        for f in fields:
            lines+=['### '+f['id'],'']
            for q in f['checks']:lines+=[rule(q)]
        extra=[q for q in c.get('elementChecks',[]) if q.get('element',q.get('scopeElement'))==typ]
        if typ=='common':extra += c.get('hierarchyChecks',[])
        if extra:
            lines+=['## Whole-element and hierarchy reference criteria','']
            for q in extra:lines+=[rule(q)]
        data={'title':'Generic product management quality rules — '+name,'catalogueVersion':c['catalogueVersion'],'sourceSha256':c['source']['contentSha256'],'content':'\n'.join(lines)}
        path=out/(typ+'.json');path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        summary.append({'element':typ,'title':data['title'],'path':str(path.relative_to(ROOT)),'fields':len(fields),'requiredComponents':sum(len(f['details']) for f in fields),'independentComponentChecks':0,'mandatoryStageGateDefinitions':len(gates),'mandatoryGatesPerItemCurrentStage':7 if typ!='common' else 0,'referenceChecks':sum(len(f['checks']) for f in fields)+len(extra),'characters':len(data['content'])})
    (out/'index.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'documents':summary,'fieldCounts':dict(Counter(f['element'] for f in c['fields']))},indent=2))
if __name__=='__main__':main()
