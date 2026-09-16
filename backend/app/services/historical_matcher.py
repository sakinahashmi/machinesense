import json
import numpy as np
from typing import List, Dict, Any
from app.schemas.investigation import HistoricalMatch
from app.services.data_service import DataService


class HistoricalMatcher:
    @staticmethod
    def match_cases(
        target_features: Dict[str, float],
        machine_id: str = "CNC-07",
        limit: int = 5
    ) -> List[HistoricalMatch]:
        """
        Matches current failure telemetry against historical failure database
        using multi-feature weighted Euclidean distance / Cosine similarity.
        """
        cases = DataService.get_historical_cases()
        if not cases:
            return []

        # Target vector: [vib_ratio, power_pct_inc, cycle_ratio, dim_dev, temp_c]
        # Feature normalization weights
        weights = np.array([0.25, 0.25, 0.25, 0.15, 0.10])
        scales = np.array([4.0, 30.0, 1.5, 0.6, 55.0])

        t_vec = np.array([
            target_features.get("vib_ratio", 2.5),
            target_features.get("power_pct_inc", 18.4),
            target_features.get("cycle_ratio", 1.22),
            target_features.get("dim_dev", 0.42),
            target_features.get("temp_c", 44.0)
        ]) / scales

        scored_matches = []

        for case in cases:
            raw_sim = case.get("similarity_features")
            if not raw_sim:
                continue

            try:
                feat = json.loads(raw_sim) if isinstance(raw_sim, str) else raw_sim
                c_vec = np.array([
                    feat.get("vib_ratio", 1.0),
                    feat.get("power_pct_inc", 0.0),
                    feat.get("cycle_ratio", 0.8),
                    feat.get("dim_dev", 0.05),
                    feat.get("temp_c", 38.0)
                ]) / scales

                # Weighted Euclidean distance
                diff = (t_vec - c_vec) * weights
                dist = np.linalg.norm(diff)

                # Machine affinity boost (if same machine model/type)
                machine_bonus = 0.05 if case.get("machine_id") == machine_id else 0.0

                # Similarity percentage calculation (0 to 100)
                sim_pct = max(10.0, min(98.5, (1.0 - dist * 1.8 + machine_bonus) * 100.0))
                sim_pct = round(sim_pct, 1)

                scored_matches.append({
                    "case_id": case["case_id"],
                    "machine_id": case["machine_id"],
                    "failure_type": case["failure_type"],
                    "root_cause": case["root_cause"],
                    "similarity_score": sim_pct,
                    "evidence": case["evidence"],
                    "corrective_action": case["corrective_action"],
                    "resolution_time": float(case.get("resolution_time", 2.0))
                })
            except Exception:
                continue

        # Sort by similarity descending
        scored_matches.sort(key=lambda x: x["similarity_score"], reverse=True)

        return [HistoricalMatch(**m) for m in scored_matches[:limit]]
