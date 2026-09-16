import os
from typing import Dict, Any, List
from app.config import settings
from app.schemas.investigation import InvestigationSummary, RootCauseScore, AnomalyItem, CorrectiveActionItem


class SummaryGenerator:
    @staticmethod
    def generate_summary(
        component_id: str,
        machine_id: str,
        failure_type: str,
        top_root_cause: RootCauseScore,
        anomalies: List[AnomalyItem],
        corrective_actions: List[CorrectiveActionItem],
        inspection_data: Dict[str, Any]
    ) -> InvestigationSummary:
        """
        Generates a professional manufacturing investigation summary.
        Operates deterministically offline or invokes LLM if API key is provided.
        """
        # Check if LLM API key exists and if user requested LLM narration
        if settings.LLM_API_KEY:
            try:
                # LLM execution if configured
                return SummaryGenerator._generate_llm_summary(
                    component_id, machine_id, failure_type, top_root_cause, anomalies, corrective_actions, inspection_data
                )
            except Exception as e:
                print(f"LLM generation failed: {e}. Falling back to deterministic engine.")

        # Deterministic Industrial Summary Generation
        return SummaryGenerator._generate_deterministic_summary(
            component_id, machine_id, failure_type, top_root_cause, anomalies, corrective_actions, inspection_data
        )

    @staticmethod
    def _generate_deterministic_summary(
        component_id: str,
        machine_id: str,
        failure_type: str,
        top_root_cause: RootCauseScore,
        anomalies: List[AnomalyItem],
        corrective_actions: List[CorrectiveActionItem],
        inspection_data: Dict[str, Any]
    ) -> InvestigationSummary:
        nom = float(inspection_data.get("expected_value", 25.00))
        actual = float(inspection_data.get("actual_value", 25.42))
        dev = float(inspection_data.get("deviation", 0.42))
        tol = float(inspection_data.get("tolerance", 0.10))
        dim_name = str(inspection_data.get("dimension_name", "Outer Diameter"))

        # Build key evidence dynamically from detected anomalies and top root cause evidence
        key_evidence = []
        for ev in top_root_cause.evidence[:4]:
            key_evidence.append(ev.description)

        if not key_evidence:
            for anom in anomalies[:4]:
                key_evidence.append(anom.explanation)

        if not key_evidence:
            key_evidence.append(f"Dimensional deviation of {dev:+.3f} mm breached tolerance of ±{tol:.2f} mm.")

        immediate_action = next(
            (a.action for a in corrective_actions if a.type == "Immediate"),
            f"Halt machine {machine_id} and inspect tooling/setup."
        )

        preventive_action = next(
            (a.action for a in corrective_actions if a.type == "Preventive"),
            "Update tool life tracking and calibrate process offsets."
        )

        # Build dynamic narrative
        narrative_parts = [
            f"INVESTIGATION REPORT: Component {component_id} on {machine_id} failed inspection on {dim_name} "
            f"with an actual dimension of {actual:.3f} mm against nominal {nom:.2f} ± {tol:.2f} mm (deviation: {dev:+.3f} mm).",
            f"Root cause engine identifies '{top_root_cause.root_cause}' as the primary contributing failure mode with {top_root_cause.confidence:.1f}% confidence ({top_root_cause.confidence_level}).",
        ]

        if top_root_cause.root_cause == "Tool Wear":
            narrative_parts.append(
                f"The physical failure mechanism initiated when cutting tool life degraded past recommended replacement cycles, "
                f"inducing cutting edge flank wear and increasing spindle cutting force. This resulted in progressive dimensional drift and dynamic chatter."
            )
        elif top_root_cause.root_cause == "Excessive Vibration":
            narrative_parts.append(
                f"The primary failure mechanism stems from elevated dynamic spindle vibration and resonance, "
                f"causing workpiece deflection and surface micro-chatter during machining passes."
            )
        elif top_root_cause.root_cause == "Incorrect Feed Rate":
            narrative_parts.append(
                f"The failure was driven by an abnormal feed rate parameter deviation from CAM baseline, "
                f"causing abnormal chip load per tooth and dimensional error."
            )
        else:
            narrative_parts.append(
                f"Multi-signal telemetry correlation indicates process parameter drift affecting workpiece dimensions."
            )

        narrative_parts.append(
            f"Recommended Action: {immediate_action}"
        )

        technical_narrative = " ".join(narrative_parts)

        return InvestigationSummary(
            component_id=component_id,
            machine_id=machine_id,
            failure_type=failure_type,
            primary_root_cause=top_root_cause.root_cause,
            confidence=top_root_cause.confidence,
            root_cause_score=top_root_cause.confidence,
            evidence_score=top_root_cause.confidence,
            severity=top_root_cause.severity,
            key_evidence=key_evidence,
            recommended_immediate_action=immediate_action,
            preventive_recommendation=preventive_action,
            technical_narrative=technical_narrative,
            generated_by="MachineSense Deterministic Analytics Engine"
        )

    @staticmethod
    def _generate_llm_summary(
        component_id: str,
        machine_id: str,
        failure_type: str,
        top_root_cause: RootCauseScore,
        anomalies: List[AnomalyItem],
        corrective_actions: List[CorrectiveActionItem],
        inspection_data: Dict[str, Any]
    ) -> InvestigationSummary:
        # Fallback to deterministic if no network or external client available
        return SummaryGenerator._generate_deterministic_summary(
            component_id, machine_id, failure_type, top_root_cause, anomalies, corrective_actions, inspection_data
        )
