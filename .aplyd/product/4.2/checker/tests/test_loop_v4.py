"""Regression tests for durable, advisory owner/reviewer queues."""
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKER_DIR))
import quality_loop as loop


def document():
    return {"documentId": "fixture-loop", "mode": "real", "elements": [{"id": "story-1", "elementType": "user_story",
        "fields": {"user_story.scope": {"value": "Pending"}, "user_story.priority": {"value": "Pending"}},
        "decisionOwnerId": "fixture-owner"}], "scope": {"mode": "partial"}}


def result(check_id="scope", status="missing", mode="structural", reason="Missing field user_story.scope: establish the boundary.", resolution_kind="author_repair_or_owner_decision"):
    return {"id": "story-1:" + check_id, "checkId": check_id, "elementId": "story-1", "fieldId": "user_story.scope",
        "status": status, "mode": mode, "reason": reason, "blocking": True, "resolutionKind": resolution_kind,
        "questionGroup": "field:story-1:user_story.scope", "dimension": "completeness", "severity": "blocking",
        "passCriterion": "Explicit included/excluded scope agreed from retained evidence.", "evidenceRequirement": "Actual decision record.",
        "subjectFingerprint": "fixture-scoped-1"}


def report(*checks, status="needs_input", synthetic=False, fingerprint="fixture-report-1"):
    return {"checks": list(checks), "qualityState": {"status": status}, "subjectFingerprint": fingerprint,
        "reviewerAuthentication": {"advisoryOnly": True, "status": "synthetic_test_only" if synthetic else "not_authenticated_offline"},
        "assessmentCoverage": {"stage": "planning"}, "unresolvedCheckIds": [check["id"] for check in checks if check["status"] not in {"passed", "not_applicable"}]}


class DurableLoopTests(unittest.TestCase):
    def test_batch_creation_is_not_acknowledgement_and_repeats(self):
        checks = [result(str(index)) | {"questionGroup": "decision-" + str(index)} for index in range(6)]
        first, state = loop.question_packet(report(*checks), document(), batch_size=3)
        second, state = loop.question_packet(report(*checks), document(), state, batch_size=3)
        self.assertEqual(first["currentBatchId"], second["currentBatchId"])
        self.assertEqual([item["id"] for item in first["nextBatch"]], [item["id"] for item in second["nextBatch"]])
        self.assertEqual(second["newQuestionCount"], 0)
        self.assertTrue(all(question["presentedCount"] == 0 for question in state["questions"].values()))

    def test_acknowledgement_advances_but_does_not_lose_unanswered(self):
        checks = [result(str(index)) | {"questionGroup": "decision-" + str(index)} for index in range(6)]
        first, state = loop.question_packet(report(*checks), document(), batch_size=3)
        with tempfile.TemporaryDirectory() as directory:
            loop.write_state(directory, state)
            ack = loop.acknowledge_batch(directory, first["currentBatchId"], "fixture-person")
            state = loop._read(Path(directory) / "loop-state.json")
            second, state = loop.question_packet(report(*checks), document(), state, batch_size=3)
            self.assertEqual(second["pendingQuestionCount"], 6)
            self.assertEqual(len(second["awaitingAnswerIds"]), 3)
            self.assertEqual(set(ack["questionIds"]), set(second["awaitingAnswerIds"]))
            self.assertTrue(set(second["awaitingAnswerIds"]).isdisjoint(item["id"] for item in second["nextBatch"]))
            self.assertEqual(second["loopStatus"], "needs_input")

    def test_all_acknowledged_still_show_awaiting_answers(self):
        packet, state = loop.question_packet(report(result()), document())
        with tempfile.TemporaryDirectory() as directory:
            loop.write_state(directory, state)
            loop.acknowledge_batch(directory, packet["currentBatchId"], "fixture-person")
            packet, state = loop.question_packet(report(result()), document(), loop._read(Path(directory) / "loop-state.json"))
        self.assertEqual(packet["nextBatch"], [])
        self.assertEqual(len(packet["awaitingAnswers"]), 1)
        self.assertEqual(packet["pendingQuestionCount"], 1)
        self.assertEqual(packet["loopStatus"], "needs_input")

    def test_partial_answer_keeps_remaining_batch(self):
        checks = [result(str(index)) | {"questionGroup": "decision-" + str(index)} for index in range(3)]
        packet, state = loop.question_packet(report(*checks), document())
        with tempfile.TemporaryDirectory() as directory:
            loop.write_state(directory, state)
            loop.record_answer(directory, packet["nextBatch"][0]["id"], "Retain scope boundary from the attached fixture workshop.", "fixture-owner")
            next_packet, _ = loop.question_packet(report(*checks), document(), loop._read(Path(directory) / "loop-state.json"))
        self.assertEqual(next_packet["currentBatchId"], packet["currentBatchId"])
        self.assertEqual(len(next_packet["nextBatch"]), 2)
        self.assertEqual(next_packet["answeredButUnresolvedCount"], 1)

    def test_resolved_question_reopens_on_regression_without_manual_version(self):
        failing = report(result())
        packet, state = loop.question_packet(failing, document())
        first = packet["nextBatch"][0]["id"]
        _, state = loop.question_packet(report(result(status="passed"), status="stage_checks_satisfied"), document(), state)
        self.assertEqual(state["questions"][first]["status"], "resolved")
        packet, state = loop.question_packet(failing, document(), state)
        reopened = packet["nextBatch"][0]
        self.assertNotEqual(reopened["id"], first)
        self.assertEqual(reopened["regressionOf"], first)
        self.assertEqual(reopened["occurrence"], 2)
        rerun, _ = loop.question_packet(failing, document(), state)
        self.assertEqual(rerun["newQuestionCount"], 0)
        self.assertEqual(rerun["nextBatch"][0]["id"], reopened["id"])

    def test_many_regression_cycles_reopen_each_real_occurrence(self):
        state = None
        ids = []
        for _ in range(20):
            packet, state = loop.question_packet(report(result()), document(), state)
            ids.append(packet["nextBatch"][0]["id"])
            _, state = loop.question_packet(report(result(status="passed"), status="stage_checks_satisfied"), document(), state)
        self.assertEqual(len(set(ids)), 20)

    def test_absent_and_stale_review_route_to_reviewer_without_owner_questions(self):
        for status in ("missing", "stale"):
            check = result(status=status, mode="review", reason="No exact current independent review.", resolution_kind="independent_review_task")
            packet, state = loop.question_packet(report(check), document())
            self.assertEqual(packet["nextBatch"], [])
            self.assertEqual(packet["pendingQuestionCount"], 0)
            self.assertEqual(packet["reviewerQueueCount"], 1)
            self.assertEqual(packet["loopStatus"], "needs_review")

    def test_missing_gate_content_stays_precise_owner_question(self):
        check = result(mode="review", reason="Required stage details unresolved: user_story.scope, user_story.priority. Deferred details remain deferred.") | {"fieldId": None}
        packet, _ = loop.question_packet(report(check), document())
        question = packet["nextBatch"][0]
        self.assertIn("user_story.scope", question["question"])
        self.assertIn("user_story.priority", question["question"])
        self.assertEqual(question["decisionOwnerId"], "fixture-owner")
        self.assertEqual(packet["reviewerQueueCount"], 0)

    def test_unknown_ai_applicability_is_owner_fact_not_missing_review(self):
        check = result(mode="review", reason="Resolve ai applicability from authoritative scope.") | {
            "id": "workspace:profile_decision_ai", "checkId": "profile_decision_ai", "elementId": None, "fieldId": None,
            "questionGroup": "check:workspace:profile_decision_ai"}
        doc = document() | {"productProfile": {"ai": {"applicability": "unknown", "decisionOwnerId": "fixture-context-owner"}}}
        packet, _ = loop.question_packet(report(check), doc)
        self.assertEqual(packet["reviewerQueueCount"], 0)
        self.assertIn("productProfile.ai", packet["nextBatch"][0]["question"])
        self.assertEqual(packet["nextBatch"][0]["decisionOwnerId"], "fixture-context-owner")

    def test_actual_owner_not_invented_from_author_or_reviewer(self):
        doc = document()
        doc["elements"][0].pop("decisionOwnerId")
        doc["elements"][0]["authorId"] = "author-not-owner"
        packet, _ = loop.question_packet(report(result()), doc)
        self.assertIsNone(packet["nextBatch"][0]["decisionOwnerId"])
        self.assertEqual(packet["nextBatch"][0]["decisionOwnerStatus"], "unresolved")

    def test_fixed_fact_waits_for_review_before_resolution(self):
        packet, state = loop.question_packet(report(result()), document())
        question_id = packet["nextBatch"][0]["id"]
        check = result(status="stale", mode="review", reason="Current exact review is stale.", resolution_kind="independent_review_task")
        packet, state = loop.question_packet(report(check), document(), state)
        self.assertEqual(state["questions"][question_id]["status"], "awaiting_review")
        self.assertEqual(packet["nextBatch"], [])
        self.assertEqual(packet["loopStatus"], "needs_review")
        _, state = loop.question_packet(report(result(status="passed"), status="stage_checks_satisfied"), document(), state)
        self.assertEqual(state["questions"][question_id]["status"], "resolved")

    def test_answers_never_grant_pass_and_followups_are_unlimited(self):
        packet, state = loop.question_packet(report(result()), document())
        current = packet["nextBatch"][0]["id"]
        with tempfile.TemporaryDirectory() as directory:
            for _ in range(12):
                loop.write_state(directory, state)
                loop.record_answer(directory, current, "This fixture still needs an excluded scope boundary.", "fixture-owner", "needs_clarification", "The exclusion is still missing.")
                packet, state = loop.question_packet(report(result()), document(), loop._read(Path(directory) / "loop-state.json"))
                self.assertEqual(packet["loopStatus"], "needs_input")
                self.assertEqual(packet["nextBatch"][0]["followUpTo"], current)
                current = packet["nextBatch"][0]["id"]
            self.assertEqual(state["answerCount"], 12)

    def test_long_followup_history_archives_answers_and_closed_packets(self):
        packet, state = loop.question_packet(report(result()), document())
        current = packet["nextBatch"][0]["id"]
        with tempfile.TemporaryDirectory() as directory:
            for _ in range(140):
                loop.write_state(directory, state)
                loop.record_answer(directory, current, "The workshop exclusion boundary still needs clarification.", "fixture-owner", "needs_clarification", "The exclusion remains unspecified.")
                packet, state = loop.question_packet(report(result()), document(), loop._read(Path(directory) / "loop-state.json"))
                self.assertEqual(packet["loopStatus"], "needs_input")
                current = packet["nextBatch"][0]["id"]
            loop.write_state(directory, state)
            self.assertEqual(state["answerCount"], 140)
            self.assertEqual(len(state["answers"]), loop.ANSWER_LIMIT)
            self.assertLessEqual(len(state["questions"]), loop.CLOSED_QUESTION_LIMIT + 1)
            archived_answers, archived_questions = 0, 0
            head = state["archiveHead"]
            while head:
                archived = loop._read(Path(directory) / head["path"])
                archived_answers += sum(record["kind"] == "answer" for record in archived["records"])
                archived_questions += sum(record["kind"] == "closed_question" for record in archived["records"])
                head = archived["previous"]
            self.assertEqual(archived_answers + len(state["answers"]), 140)
            self.assertGreater(archived_questions, 0)
            self.assertEqual(loop.verify_state(directory, state)["archiveIntegrity"], "verified_local_hash_chain")

    def test_unrelated_report_change_does_not_create_context_snapshot(self):
        packet, state = loop.question_packet(report(result()), document())
        question_id = packet["nextBatch"][0]["id"]
        for number in range(20):
            packet, state = loop.question_packet(report(result(), fingerprint="unrelated-" + str(number)), document(), state)
        self.assertEqual(packet["newQuestionCount"], 0)
        self.assertEqual(state["questions"][question_id]["contextHistory"], [])

    def test_context_history_is_compact_bounded_and_archived(self):
        packet, state = loop.question_packet(report(result()), document())
        with tempfile.TemporaryDirectory() as directory:
            for number in range(50):
                doc = document()
                doc["elements"][0]["fields"]["user_story.scope"]["value"] = "Unresolved specific fixture boundary " + str(number)
                check = result() | {"subjectFingerprint": "scope-" + str(number), "passCriterion": "X" * 10000}
                packet, state = loop.question_packet(report(check, fingerprint="report-" + str(number)), doc, state)
                loop.write_state(directory, state)
            question = state["questions"][packet["nextBatch"][0]["id"]]
            self.assertEqual(len(question["contextHistory"]), loop.CONTEXT_LIMIT)
            self.assertEqual(len(state["iterations"]), loop.ITERATION_LIMIT)
            self.assertLess((Path(directory) / "loop-state.json").stat().st_size, 25000)
            self.assertTrue(state.get("archiveHead"))
            head = state["archiveHead"]
            records = []
            while head:
                archived = loop._read(Path(directory) / head["path"])
                self.assertEqual(loop._digest(archived), head["contentHash"])
                records.extend(archived["records"])
                head = archived["previous"]
            self.assertTrue(any(record["kind"] == "question_context" for record in records))
            self.assertFalse(any("checksToResolve" in record for record in records if record["kind"] == "question_context"))

    def test_dismissal_keeps_failed_check_in_repair_queue(self):
        packet, state = loop.question_packet(report(result()), document())
        question_id = packet["nextBatch"][0]["id"]
        with tempfile.TemporaryDirectory() as directory:
            loop.write_state(directory, state)
            loop.dismiss_question(directory, question_id, "The author can extract the actual boundary from the pinned workshop; no owner question is required.", "fixture-person")
            packet, _ = loop.question_packet(report(result()), document(), loop._read(Path(directory) / "loop-state.json"))
        self.assertEqual(packet["qualityStatus"], "needs_input")
        self.assertEqual(packet["loopStatus"], "needs_revision")
        self.assertEqual(packet["dismissedQuestionIds"], [question_id])
        self.assertEqual(packet["repairQueue"][0]["lane"], "dismissed_but_unresolved")

    def test_real_and_synthetic_success_are_distinct_advisory_states(self):
        real, _ = loop.question_packet(report(result(status="passed"), status="stage_checks_satisfied"), document())
        synthetic, _ = loop.question_packet(report(result(status="passed"), status="synthetic_checks_satisfied", synthetic=True), document())
        self.assertEqual(real["loopStatus"], "advisory_complete")
        self.assertEqual(synthetic["loopStatus"], "synthetic_complete")
        self.assertNotEqual(real["loopStatus"], "complete")

    def test_shape_errors_are_value_errors(self):
        cases = [(report(result()), []), ([], document()), (report(result()) | {"checks": "bad"}, document()),
            (report(result()) | {"checks": [None]}, document()), (report(result()), document() | {"scope": "bad"}),
            (report(result()), document() | {"elements": ["bad"]}), (report(result()) | {"qualityState": []}, document())]
        for rep, doc in cases:
            with self.subTest(rep=rep, doc=doc), self.assertRaises(ValueError):
                loop.question_packet(rep, doc)
        for size in (0, -1, "3", True):
            with self.assertRaises(ValueError):
                loop.question_packet(report(result()), document(), batch_size=size)

    def test_bad_state_shapes_fail_deterministically(self):
        for state in ([], {"questions": []}, {"iterations": {}}, {"currentBatch": {"questionIds": "bad"}}, {"answerCount": "one"},
                      {"groups": {"a": "bad"}}, {"groups": {"a": {"occurrence": "one"}}},
                      {"currentBatch": {"id": "B-current", "questionIds": [None]}}, {"iterations": ["bad"]}):
            with self.assertRaises(ValueError):
                loop.question_packet(report(result()), document(), state)

    def test_changed_archived_history_refuses_mutation(self):
        _, state = loop.question_packet(report(result()), document())
        with tempfile.TemporaryDirectory() as directory:
            for number in range(12):
                state["_archivePending"].append({"kind": "fixture-audit", "number": number})
                loop.write_state(directory, state)
            check = loop.verify_state(directory, state)
            self.assertEqual(check["verifiedArchiveCount"], 12)
            self.assertEqual(check["verifiedArchivedRecordCount"], 12)
            head = state["archiveHead"]
            for _ in range(5):
                head = loop._read(Path(directory) / head["path"])["previous"]
            archive_path = Path(directory) / head["path"]
            archive = loop._read(archive_path)
            archive["records"][0]["number"] = "tampered"
            loop._write(archive_path, archive)
            before = (Path(directory) / "loop-state.json").read_bytes()
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                loop.write_state(directory, state)
            self.assertEqual(before, (Path(directory) / "loop-state.json").read_bytes())

    def test_archive_path_and_cumulative_count_are_checked(self):
        _, state = loop.question_packet(report(result()), document())
        with tempfile.TemporaryDirectory() as directory:
            state["_archivePending"].append({"kind": "fixture-audit"})
            loop.write_state(directory, state)
            wrong_path = copy.deepcopy(state)
            wrong_path["archiveHead"]["path"] = "../outside.json"
            with self.assertRaisesRegex(ValueError, "confined"):
                loop.verify_state(directory, wrong_path)
            wrong_count = copy.deepcopy(state)
            wrong_count["archiveHead"]["totalRecordCount"] += 1
            with self.assertRaisesRegex(ValueError, "cumulative record count"):
                loop.verify_state(directory, wrong_count)

    def test_invalid_answers_acknowledgement_and_stale_question_rejected(self):
        packet, state = loop.question_packet(report(result()), document())
        question_id = packet["nextBatch"][0]["id"]
        with tempfile.TemporaryDirectory() as directory:
            loop.write_state(directory, state)
            with self.assertRaises(ValueError):
                loop.acknowledge_batch(directory, "unknown-batch", "fixture-owner")
            with self.assertRaises(ValueError):
                loop.record_answer(directory, question_id, "TBD", "fixture-owner")
            with self.assertRaises(ValueError):
                loop.record_answer(directory, question_id, "A retained fixture answer.", "fixture-owner", "needs_clarification")
            _, state = loop.question_packet(report(result(status="passed"), status="stage_checks_satisfied"), document(), state)
            loop.write_state(directory, state)
            with self.assertRaises(ValueError):
                loop.record_answer(directory, question_id, "A retained fixture answer.", "fixture-owner")

    def test_all_legacy_presented_questions_reconsidered_without_false_ack(self):
        packet, state = loop.question_packet(report(result()), document())
        state.pop("loopSchemaVersion")
        state.pop("currentBatch")
        for question in state["questions"].values():
            question["presentedCount"] = 1
        packet, _ = loop.question_packet(report(result()), document(), state)
        self.assertEqual(len(packet["nextBatch"]), 1)
        self.assertIsNone(packet["nextBatch"][0]["acknowledgedAt"])

    def test_advisory_unreviewed_sample_never_creates_owner_question(self):
        check = result(status="unreviewed", mode="review") | {"blocking": False}
        packet, _ = loop.question_packet(report(check, status="stage_checks_satisfied"), document())
        self.assertEqual(packet["nextBatch"], [])
        self.assertEqual(packet["reviewerQueue"], [])

    def test_missing_actual_catalogue_reviews_route_only_to_reviewers(self):
        spec = importlib.util.spec_from_file_location("v4_current_checker", CHECKER_DIR / "quality_checker.py")
        qc = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(qc)
        catalogue = qc.read_json(CHECKER_DIR / "catalogue.json")
        doc = qc.read_json(CHECKER_DIR / "examples" / "synthetic-planning-pass.json")
        doc["reviews"] = []
        # A version migration alone retires old evidence bindings but does not
        # make its present facts into questions for a product owner.
        doc["catalogueHash"] = qc.digest(catalogue)
        current = qc.Checker(catalogue, doc).run()
        packet, _ = loop.question_packet(current, doc, api=qc)
        review_results = [check for check in current["checks"] if check.get("resolutionKind") == "independent_review_task"]
        self.assertGreater(len(review_results), 0)
        self.assertEqual(packet["reviewerQueueCount"], len(review_results))
        self.assertFalse(any(question["checkResultId"] in {check["id"] for check in review_results} for question in packet["nextBatch"]))


if __name__ == "__main__":
    unittest.main()
