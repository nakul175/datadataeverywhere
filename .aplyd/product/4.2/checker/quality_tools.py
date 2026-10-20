"""Compact inspection and exact hashing helpers; never generate review verdicts."""
from pathlib import Path
import json

COMMANDS = {'summary', 'next', 'explain', 'review-hashes', 'trust-template', 'bind-evidence'}


def register_commands(commands):
    summary = commands.add_parser('summary', help='Read a compact report summary without dumping criteria.')
    summary.add_argument('--report', required=True)
    summary.add_argument('--state-dir')
    following = commands.add_parser('next', help='Inspect the retained batch and separate work queues.')
    following.add_argument('--state-dir', required=True)
    following.add_argument('--queue', choices=['owner', 'reviewer', 'repair', 'all'], default='all')
    following.add_argument('--limit', type=int, default=3)
    explain = commands.add_parser('explain', help='Inspect one exact criterion and its current finding.')
    explain.add_argument('check_id')
    explain.add_argument('--report', required=True)
    explain.add_argument('--element-id')
    explain.add_argument('--field-id')
    hashes = commands.add_parser('review-hashes', help='Compute existing review hashes without approving them.')
    hashes.add_argument('--document', required=True)
    hashes.add_argument('--output')
    skeleton = commands.add_parser('trust-template', help='Create an incomplete advisory registry intake.')
    skeleton.add_argument('--document', required=True)
    skeleton.add_argument('--output', required=True)
    bind = commands.add_parser('bind-evidence', help='Hash retained evidence and bind it to one current target.')
    bind.add_argument('--document', required=True)
    bind.add_argument('--evidence-id', required=True)
    bind.add_argument('--element-id')
    bind.add_argument('--field-id')
    bind.add_argument('--check-id', required=True)
    bind.add_argument('--output', required=True)
    bind.add_argument('--allow-synthetic', action='store_true')


def require_object(value, label):
    if not isinstance(value, dict):
        raise ValueError(label + ' must be a JSON object.')
    return value


def summary_report(report):
    require_object(report, 'Report')
    checks = report.get('checks', [])
    if not isinstance(checks, list) or any(not isinstance(row, dict) for row in checks):
        raise ValueError('Report checks must be a list of objects.')
    unresolved = [row for row in checks if row.get('blocking', True) and row.get('status') not in {'passed', 'not_applicable'}]
    by_kind = {}
    for row in unresolved:
        kind = row.get('resolutionKind', 'author_repair_or_owner_decision')
        by_kind[kind] = by_kind.get(kind, 0) + 1
    return {
        'documentId': report.get('documentId'), 'revision': report.get('revision'),
        'catalogueIdentity': report.get('catalogueIdentity'),
        'qualityState': report.get('qualityState'),
        'assessmentCoverage': report.get('assessmentCoverage'),
        'unresolvedByResolutionKind': by_kind,
        'unresolvedBlockingCount': len(unresolved),
        'advisorySamples': {
            'count': len(report.get('advisorySamples', [])),
            'unreviewed': sum(row.get('status') == 'unreviewed' for row in report.get('advisorySamples', [])),
            'failed': sum(row.get('status') == 'failed' for row in report.get('advisorySamples', [])),
        },
        'reviewerAuthentication': report.get('reviewerAuthentication'),
        'readinessState': report.get('readinessState'), 'deliveryState': report.get('deliveryState'),
        'assurance': report.get('assurance'), 'inspectionOnly': True,
    }


def inspect_next(packet, queue='all', limit=3):
    require_object(packet, 'Question packet')
    if not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValueError('limit must be between 1 and 100.')
    keys = {'owner': 'nextBatch', 'reviewer': 'reviewerQueue', 'repair': 'repairQueue'}
    result = {'loopStatus': packet.get('loopStatus'), 'currentBatchId': packet.get('currentBatchId'),
              'pendingQuestionCount': packet.get('pendingQuestionCount'),
              'awaitingAnswerIds': packet.get('awaitingAnswerIds', []), 'inspectionOnly': True}
    for name, key in keys.items():
        if queue not in {'all', name}:
            continue
        rows = packet.get(key, [])
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError(key + ' must be a list of objects.')
        fields = ['id', 'groupId', 'elementId', 'fieldId', 'checkId', 'question', 'reason',
                  'decisionOwnerId', 'ownerStatus', 'status', 'resolutionKind', 'occurrence', 'resumeCondition']
        result[name + 'Queue'] = [{key: row[key] for key in fields if key in row} for row in rows[:limit]]
        result[name + 'QueueTotal'] = len(rows)
        result[name + 'QueueTruncated'] = len(rows) > limit
    return result


def explain_check(report, check_id, element_id=None, field_id=None):
    require_object(report, 'Report')
    rows = [row for row in report.get('checks', []) if row.get('checkId') == check_id or row.get('id') == check_id]
    rows = [row for row in rows if (element_id is None or row.get('elementId') == element_id) and (field_id is None or row.get('fieldId') == field_id)]
    if len(rows) != 1:
        raise ValueError('Select exactly one result; supply its full result ID or --element-id and --field-id when ambiguous.')
    row = rows[0]
    keys = ['id', 'checkId', 'elementId', 'fieldId', 'status', 'blocking', 'resolutionKind',
            'reason', 'passCriterion', 'evidenceRequirement', 'evidenceIds', 'questionPrompt',
            'repairPrompt', 'subjectFingerprint', 'resultFingerprint', 'missingFieldIds', 'requiredFieldIds']
    return {key: row[key] for key in keys if key in row} | {'inspectionOnly': True}


def dispatch(args, catalogue, api):
    get = lambda name: api[name] if isinstance(api, dict) else getattr(api, name)
    read, write, digest = get('read_json'), get('write_json'), get('digest')
    if args.command == 'summary':
        result = summary_report(read(args.report))
        if args.state_dir:
            result['next'] = inspect_next(read(Path(args.state_dir) / 'questions.json'))
        return result
    if args.command == 'next':
        return inspect_next(read(Path(args.state_dir) / 'questions.json'), args.queue, args.limit)
    if args.command == 'explain':
        return explain_check(read(args.report), args.check_id, args.element_id, args.field_id)
    get('require_canonical_catalogue')(catalogue)
    document = require_object(read(args.document), 'Document')
    if args.command == 'review-hashes':
        if args.output and Path(args.output).resolve() == Path(args.document).resolve():
            raise ValueError('The hash output must not overwrite its source document.')
        reviews = document.get('reviews', [])
        if not isinstance(reviews, list) or any(not isinstance(row, dict) for row in reviews):
            raise ValueError('reviews must be a list of objects.')
        result = {'documentId': document.get('documentId'), 'reviewCount': len(reviews),
                  'bindingVersion': 'scoped-v1',
                  'reviewHashes': sorted(digest(row) for row in reviews),
                  'reviewSetFingerprint': get('review_set_fingerprint')(document, catalogue, Path(args.document).resolve().parent),
                  'meaning': 'Hashes of supplied existing reviews only; no review, identity verification or approval performed.'}
        if args.output:
            write(args.output, result)
        return result
    if args.command == 'trust-template':
        if Path(args.output).resolve() == Path(args.document).resolve():
            raise ValueError('The template must not overwrite its source document.')
        result = {'schemaVersion': '1.0', 'status': 'draft_needs_external_governance',
                  'catalogueHash': document.get('catalogueHash'), 'sourcePins': document.get('sourcePins', {}),
                  'bindingVersion': 'scoped-v1',
                  'reviewSetFingerprint': get('review_set_fingerprint')(document, catalogue, Path(args.document).resolve().parent),
                  'authorities': document.get('authorities', []), 'reviewVerifications': [],
                  'requiredExternalDecisions': ['Authenticate appointed reviewers and their actual scope outside the authoring agent.',
                      'Retain independently witnessed verification record and exact reviewed subject bindings.',
                      'Obtain the actual approving authority separately where required.'],
                  'certificationGranted': False, 'authorityCreatedByThisHelper': False,
                  'assurance': 'Incomplete advisory intake; copying declared profiles cannot authenticate them.'}
        write(args.output, result)
        return {'created': str(args.output), 'status': result['status'], 'reviewVerificationCount': 0,
                'certificationGranted': False, 'authorityCreatedByThisHelper': False}
    if args.command == 'bind-evidence':
        return bind_evidence(args, document, catalogue, api)
    raise ValueError('Unknown inspection helper command.')


def bind_evidence(args, document, catalogue, api):
    get = lambda name: api[name] if isinstance(api, dict) else getattr(api, name)
    get('require_canonical_catalogue')(catalogue)
    original, output = Path(args.document).resolve(), Path(args.output).resolve()
    if original == output:
        raise ValueError('Write a separate evidence-bound candidate; preserve the original document.')
    if original.parent != output.parent:
        raise ValueError('Keep the candidate beside its source so relative evidence assets retain their meaning.')
    if document.get('mode') == 'synthetic_fixture' and not args.allow_synthetic:
        raise ValueError('Synthetic input requires explicit --allow-synthetic and cannot certify a real product.')
    if document.get('catalogueHash') != get('digest')(catalogue):
        raise ValueError('The document must pin the current catalogue; this helper never silently repins it.')
    records = document.get('evidence', [])
    if not isinstance(records, list) or any(not isinstance(row, dict) for row in records):
        raise ValueError('evidence must be a list of objects.')
    matches = [row for row in records if row.get('id') == args.evidence_id]
    if len(matches) != 1:
        raise ValueError('Select exactly one existing retained evidence record.')
    target = {'elementId': args.element_id, 'fieldId': args.field_id, 'checkId': args.check_id}
    # The core rejects unknown targets. Actual content hashes are computed before
    # the subject hash; bindings are excluded from that hash to avoid a cycle.
    record = matches[0]
    record['contentHash'] = get('evidence_hash')(record, original.parent)
    fingerprint = get('check_subject_fingerprint')(document, catalogue, args.element_id,
                                                   args.field_id, args.check_id, original.parent)
    bindings = record.get('bindings', [])
    if not isinstance(bindings, list) or any(not isinstance(row, dict) for row in bindings):
        raise ValueError('Evidence bindings must be a list of objects.')
    record['bindings'] = [row for row in bindings if not all(row.get(key) == value for key, value in target.items())]
    record['bindings'].append({'bindingVersion': 'scoped-v1', **target, 'subjectFingerprint': fingerprint})
    get('write_json')(output, document)
    return {'created': str(output), 'evidenceId': record['id'], 'contentHash': record['contentHash'],
            'target': target, 'subjectFingerprint': fingerprint, 'bindingVersion': 'scoped-v1',
            'reviewsCreated': 0, 'reviewsApproved': 0, 'certificationGranted': False,
            'nextAction': 'Have the appointed reviewer inspect this exact target and retained evidence. Binding is not a review verdict.'}
