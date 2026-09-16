import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from app.schemas.investigation import RootCauseScore, EvidenceItem, AnomalyItem
from app.services.signal_normalizer import SignalNormalizer


class RootCauseEngine:
    """
    Evidence-Driven Multi-Signal Root Cause Analysis Engine.
    
    Combines continuous, non-saturating normalized physical signals, maintenance records,
    and historical failure cases into calibrated Root Cause Evidence Scores.
    """

    @staticmethod
    def analyze(
        machine_id: str,
        component_id: str,
        inspection_data: Dict[str, Any],
        machine_logs: pd.DataFrame,
        maintenance_history: pd.DataFrame,
        anomalies: List[AnomalyItem],
        historical_matches: List[Any],
        process_params: Optional[Dict[str, Any]] = None
    ) -> List[RootCauseScore]:
        # Extract telemetry context
        latest_log = machine_logs.iloc[-1] if not machine_logs.empty else {}
        vib_val = float(latest_log.get("vibration", 1.4))
        power_val = float(latest_log.get("power_consumption", 4.2))
        temp_val = float(latest_log.get("temperature", 38.0))
        cycle_count = int(latest_log.get("cycle_count", 0))
        tool_id = str(latest_log.get("tool_id", "T-14"))

        # Inspection deviation
        deviation = float(inspection_data.get("deviation", 0.0))
        tolerance = float(inspection_data.get("tolerance", 0.10))

        # 1. Evaluate Trend Signal: Check monotonic drift over previous records
        trend_drift_score = 0.0
        if len(machine_logs) >= 10:
            powers = machine_logs["power_consumption"].tail(15).values
            vibs = machine_logs["vibration"].tail(15).values
            if len(powers) > 1 and np.polyfit(range(len(powers)), powers, 1)[0] > 0.02:
                trend_drift_score += 0.25
            if len(vibs) > 1 and np.polyfit(range(len(vibs)), vibs, 1)[0] > 0.03:
                trend_drift_score += 0.20

        # 2. Check Maintenance Status for tool
        tool_maintenance_overdue = False
        if not maintenance_history.empty:
            tool_maint = maintenance_history[maintenance_history["tool_id"] == tool_id]
            if not tool_maint.empty:
                if any(tool_maint["status"] == "Overdue"):
                    tool_maintenance_overdue = True

        # Compute Continuous Normalized Signals using SignalNormalizer
        s_cycles = SignalNormalizer.normalize_tool_cycles(cycle_count, max_cycles=1500.0)
        s_power = SignalNormalizer.normalize_power_surge(power_val, baseline=4.20)
        s_vib = SignalNormalizer.normalize_vibration(vib_val, nominal_max=2.0)
        s_dim = SignalNormalizer.normalize_dimensional_deviation(deviation, tolerance=tolerance)
        s_maint = SignalNormalizer.normalize_maintenance_status(
            "Overdue" if tool_maintenance_overdue else "Completed",
            cycle_count,
            max_cycles=1500.0
        )

        feed_rate = float(process_params.get("feed_rate", 1200) if process_params else 1200)
        s_feed = SignalNormalizer.normalize_feed_rate_deviation(feed_rate, nominal=1200.0)

        coolant_temp = float(process_params.get("coolant_temperature", 21.5) if process_params else 21.5)
        s_coolant = SignalNormalizer.normalize_coolant_temperature(coolant_temp, target_min=19.0, target_max=23.0)

        s_calib = SignalNormalizer.normalize_calibration_drift(days=45.0, deviation=deviation, tolerance=tolerance)

        # -------------------------------------------------------------
        # CAUSE 1: TOOL WEAR
        # -------------------------------------------------------------
        tw_hist = SignalNormalizer.normalize_historical_similarity(historical_matches, "Tool Wear")
        raw_tw_score = (
            0.30 * s_cycles +
            0.25 * s_power +
            0.20 * s_dim +
            0.15 * s_maint +
            0.10 * tw_hist
        )

        tool_wear_evidence = [
            EvidenceItem(
                category="TOOL USAGE",
                title=f"Tool {tool_id} Cycle Accumulation",
                badge="Confirmed" if s_cycles > 0.70 else ("Strong Evidence" if s_cycles > 0.40 else "Context"),
                description=f"Tool {tool_id} reached {cycle_count} cycles (rated threshold: 1,500 cycles). Normalized wear evidence: {s_cycles:.3f}.",
                metrics={"current_cycles": cycle_count, "max_cycles": 1500, "tool_id": tool_id, "evidence_score": round(s_cycles, 3)}
            ),
            EvidenceItem(
                category="ANOMALY",
                title="Spindle Power Consumption Surge",
                badge="Strong Evidence" if s_power > 0.50 else "Context",
                description=f"Spindle cutting power measured at {power_val:.2f} kW (+{max(0.0, ((power_val-4.2)/4.2)*100):.1f}% over 4.20 kW baseline). Normalized cutting force evidence: {s_power:.3f}.",
                metrics={"actual_power": power_val, "baseline_power": 4.20, "evidence_score": round(s_power, 3)}
            ),
            EvidenceItem(
                category="TREND",
                title="Dimensional Tolerance Drift",
                badge="Strong Evidence" if s_dim > 0.50 else "Context",
                description=f"Measured deviation of {deviation:+.3f} mm relative to ±{tolerance:.2f} mm tolerance (ratio {abs(deviation)/tolerance:.1f}x). Normalized deviation evidence: {s_dim:.3f}.",
                metrics={"deviation_mm": deviation, "tolerance_mm": tolerance, "evidence_score": round(s_dim, 3)}
            ),
            EvidenceItem(
                category="MAINTENANCE",
                title="Tool Maintenance Ticket Status",
                badge="Confirmed" if tool_maintenance_overdue else "Context",
                description=f"Maintenance log for Tool {tool_id} is flagged as {'OVERDUE' if tool_maintenance_overdue else 'Completed'}. Evidence factor: {s_maint:.2f}.",
                metrics={"tool_id": tool_id, "status": "Overdue" if tool_maintenance_overdue else "Completed", "evidence_score": round(s_maint, 2)}
            )
        ]
        if tw_hist > 0.10:
            tool_wear_evidence.append(EvidenceItem(
                category="HISTORICAL",
                title="Historical Tool Failure Match",
                badge="Supporting Evidence",
                description=f"Corroborating historical tool wear incident profile matched with weighted similarity score of {tw_hist:.3f}.",
                metrics={"historical_similarity": round(tw_hist, 3)}
            ))

        # -------------------------------------------------------------
        # CAUSE 2: EXCESSIVE VIBRATION
        # -------------------------------------------------------------
        vib_hist = SignalNormalizer.normalize_historical_similarity(historical_matches, "Excessive Vibration")
        raw_vib_score = (
            0.50 * s_vib +
            0.20 * trend_drift_score +
            0.15 * s_dim +
            0.15 * vib_hist
        )

        vib_evidence = [
            EvidenceItem(
                category="ANOMALY",
                title="Spindle Dynamic Vibration",
                badge="Strong Evidence" if s_vib > 0.50 else "Context",
                description=f"Spindle vibration recorded at {vib_val:.2f} mm/s (nominal alert limit: 2.00 mm/s). Normalized vibration evidence: {s_vib:.3f}.",
                metrics={"vibration_mms": vib_val, "nominal_max": 2.0, "evidence_score": round(s_vib, 3)}
            ),
            EvidenceItem(
                category="PROCESS",
                title="Dynamic Harmonic Chatter",
                badge="Supporting Evidence" if trend_drift_score > 0.20 else "Context",
                description=f"Multi-cycle sensor telemetry demonstrates cutting force fluctuation and chatter drift (score: {trend_drift_score:.2f}).",
                metrics={"trend_score": round(trend_drift_score, 2)}
            )
        ]
        if vib_hist > 0.10:
            vib_evidence.append(EvidenceItem(
                category="HISTORICAL",
                title="Vibration Incident History",
                badge="Supporting Evidence",
                description=f"Past mechanical resonance incidents correlate with current vibration signature ({vib_hist:.3f}).",
                metrics={"historical_score": round(vib_hist, 3)}
            ))

        # -------------------------------------------------------------
        # CAUSE 3: INCORRECT FEED RATE
        # -------------------------------------------------------------
        feed_hist = SignalNormalizer.normalize_historical_similarity(historical_matches, "Incorrect Feed Rate")
        raw_feed_score = (
            0.55 * s_feed +
            0.15 * s_power +
            0.15 * s_dim +
            0.15 * feed_hist
        )

        feed_evidence = [
            EvidenceItem(
                category="PROCESS",
                title="Feed Rate Deviation",
                badge="Strong Evidence" if s_feed > 0.40 else "Context",
                description=f"Programmed feed rate is {feed_rate:.0f} mm/min (CAM baseline 1,200 mm/min, delta {abs(feed_rate-1200):.0f} mm/min). Normalized evidence: {s_feed:.3f}.",
                metrics={"feed_rate": feed_rate, "baseline": 1200, "evidence_score": round(s_feed, 3)}
            )
        ]

        # -------------------------------------------------------------
        # CAUSE 4: COOLANT TEMPERATURE VARIATION
        # -------------------------------------------------------------
        cool_hist = SignalNormalizer.normalize_historical_similarity(historical_matches, "Coolant Temperature Variation")
        raw_coolant_score = (
            0.55 * s_coolant +
            0.25 * s_dim +
            0.20 * cool_hist
        )

        coolant_evidence = [
            EvidenceItem(
                category="PROCESS",
                title="Coolant Delivery Temperature",
                badge="Supporting Evidence" if s_coolant > 0.30 else "Context",
                description=f"Coolant fluid temperature is {coolant_temp:.1f} °C (target range: 19.0 - 23.0 °C). Normalized thermal evidence: {s_coolant:.3f}.",
                metrics={"coolant_temp": coolant_temp, "evidence_score": round(s_coolant, 3)}
            )
        ]

        # -------------------------------------------------------------
        # CAUSE 5: MACHINE CALIBRATION DRIFT
        # -------------------------------------------------------------
        calib_hist = SignalNormalizer.normalize_historical_similarity(historical_matches, "Machine Calibration Drift")
        raw_calib_score = (
            0.80 * s_calib +
            0.20 * calib_hist
        )

        calib_evidence = [
            EvidenceItem(
                category="MAINTENANCE",
                title="Axis Backlash & Laser Calibration",
                badge="Context",
                description=f"Axis laser calibration age: 45 days. Calibration drift evidence score: {s_calib:.3f}.",
                metrics={"last_calib_days": 45, "evidence_score": round(s_calib, 3)}
            )
        ]

        # -------------------------------------------------------------
        # STRUCTURE CANDIDATES
        # -------------------------------------------------------------
        candidates = [
            {
                "root_cause": "Tool Wear",
                "raw_score": raw_tw_score,
                "evidence": tool_wear_evidence,
                "affected_parameters": ["Tool Cycle Life", "Spindle Power Draw", "Cutting Vibration", "Outer Diameter Dimension"],
                "recommended_actions": [
                    f"Immediate replacement of End Mill {tool_id} on {machine_id}",
                    "Optical tool setter length and diameter recalibration",
                    "Lower automatic tool cycle replacement warning threshold to 1400 cycles"
                ]
            },
            {
                "root_cause": "Excessive Vibration",
                "raw_score": raw_vib_score,
                "evidence": vib_evidence,
                "affected_parameters": ["Spindle Vibration RMS", "Surface Micro-Chatter"],
                "recommended_actions": [
                    f"Inspect toolholder collet tightness and runout (<3 µm) on {machine_id}",
                    "Perform dynamic spindle vibration FFT spectrum test",
                    "Verify hydraulic chuck clamping pressure"
                ]
            },
            {
                "root_cause": "Machine Calibration Drift",
                "raw_score": raw_calib_score,
                "evidence": calib_evidence,
                "affected_parameters": ["Axis Pitch Error", "Thermal Ball Screw Growth"],
                "recommended_actions": [
                    "Schedule Renishaw ballbar circularity verification test",
                    "Inspect linear guideway lubrication pressure"
                ]
            },
            {
                "root_cause": "Coolant Temperature Variation",
                "raw_score": raw_coolant_score,
                "evidence": coolant_evidence,
                "affected_parameters": ["Coolant Supply Temp", "Workpiece Thermal Expansion"],
                "recommended_actions": [
                    "Check coolant chiller heat exchanger fluid level",
                    "Inspect coolant nozzle delivery direction and flow rate"
                ]
            },
            {
                "root_cause": "Incorrect Feed Rate",
                "raw_score": raw_feed_score,
                "evidence": feed_evidence,
                "affected_parameters": ["Feed Rate (mm/min)", "Chip Load per Tooth"],
                "recommended_actions": [
                    "Verify G-code feed override lock in CNC controller",
                    "Cross-check CAM toolpath feed rate tables"
                ]
            }
        ]

        # -------------------------------------------------------------
        # FINAL ROOT CAUSE EVIDENCE SCORE CALCULATION
        # -------------------------------------------------------------
        results = []
        latest_log_id = f"LOG-{machine_id}-{latest_log.get('timestamp', 'NOW')}"
        maint_id = maintenance_history.iloc[0]["maintenance_id"] if not maintenance_history.empty else "MNT-GENERIC"

        for cand in candidates:
            raw_s = float(cand["raw_score"])
            # Map normalized composite score [0.0, 1.0] -> [0.0%, 100.0%] evidence score
            score_pct = round(max(5.0, min(99.0, raw_s * 100.0)), 1)

            if score_pct >= 80.0:
                conf_level = "HIGH CONFIDENCE"
                sev = "Critical"
            elif score_pct >= 60.0:
                conf_level = "MEDIUM-HIGH"
                sev = "Warning"
            elif score_pct >= 40.0:
                conf_level = "MEDIUM"
                sev = "Warning"
            else:
                conf_level = "LOW"
                sev = "Info"

            score_breakdown = {
                "anomaly_signal": round(raw_s * 0.40, 2),
                "trend_signal": round(trend_drift_score, 2),
                "maintenance_signal": round(s_maint * 0.30, 2),
                "historical_correlation": round(SignalNormalizer.normalize_historical_similarity(historical_matches, cand["root_cause"]), 2)
            }

            supporting_records = [
                {"source": "machine_logs", "record_id": latest_log_id, "value": f"P={power_val:.2f}kW, Vib={vib_val:.2f}mm/s, Cycles={cycle_count}"}
            ]
            if tool_maintenance_overdue or not maintenance_history.empty:
                supporting_records.append({
                    "source": "maintenance_history",
                    "record_id": maint_id,
                    "value": f"Tool {tool_id} status: {'Overdue' if tool_maintenance_overdue else 'Logged'}"
                })

            results.append(RootCauseScore(
                root_cause=cand["root_cause"],
                confidence=score_pct,
                root_cause_score=score_pct,
                evidence_score=score_pct,
                confidence_level=conf_level,
                severity=sev,
                score_breakdown=score_breakdown,
                evidence=cand["evidence"],
                affected_parameters=cand["affected_parameters"],
                supporting_records=supporting_records,
                recommended_actions=cand["recommended_actions"]
            ))

        # Sort dynamically by calculated evidence score descending
        results.sort(key=lambda x: x.confidence, reverse=True)
        return results
