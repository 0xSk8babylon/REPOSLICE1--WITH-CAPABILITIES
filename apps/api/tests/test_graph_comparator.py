import unittest

from app.engines.graph_comparator import (
    CandidateConfiguration,
    GraphEdge,
    GraphNode,
    compare_configurations,
    graph_confidence,
    score_smart_panel,
)


class GraphComparatorTests(unittest.TestCase):
    def test_compare_configurations_scores_tradeoffs_without_selecting_winner(self):
        candidates = (
            CandidateConfiguration(
                id="pw3",
                name="Powerwall 3 AC coupled",
                nodes=(GraphNode("service", "service", "known"),),
                edges=(GraphEdge("service", "battery", "power", "derived"),),
                annual_bill_delta=1200,
                backup_coverage_hours=18,
                headroom_kw=2,
                complexity_score=4,
                compliance_blockers=0,
                confidence="derived",
            ),
            CandidateConfiguration(
                id="eg4",
                name="EG4 hybrid",
                nodes=(GraphNode("service", "service", "known"),),
                edges=(GraphEdge("service", "inverter", "power", "assumed"),),
                annual_bill_delta=900,
                backup_coverage_hours=24,
                headroom_kw=-1,
                complexity_score=8,
                compliance_blockers=1,
                confidence="assumed",
            ),
        )

        scores = compare_configurations(candidates)

        self.assertEqual(("pw3", "eg4"), tuple(score.candidate_id for score in scores))
        self.assertGreater(scores[0].economics_score, scores[1].economics_score)
        self.assertGreater(scores[1].backup_score, scores[0].backup_score)
        self.assertIn("Headroom is negative", scores[1].tradeoffs[2])

    def test_smart_panel_scoring_reflects_load_management_and_backfeed_constraints(self):
        score = score_smart_panel("SPAN", controllable_load_kw=4, critical_load_kw=8, backfeed_headroom_amps=10, confidence="derived")

        self.assertEqual(50.0, score.load_management_value_score)
        self.assertEqual(80.0, score.backfeed_constraint_value_score)
        self.assertEqual(60.5, score.total_score)
        self.assertIn("load management", score.reasons[0])

    def test_graph_confidence_counts_nodes_and_edges(self):
        counts = graph_confidence(
            [GraphNode("service", "service", "known"), GraphNode("battery", "storage", "derived")],
            [GraphEdge("service", "battery", "power", "assumed")],
        )

        self.assertEqual({"known": 1, "derived": 1, "assumed": 1, "missing": 0}, counts)


if __name__ == "__main__":
    unittest.main()
