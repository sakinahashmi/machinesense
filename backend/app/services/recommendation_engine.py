from typing import List, Dict, Any
from app.schemas.investigation import CorrectiveActionItem, RootCauseScore


class RecommendationEngine:
    @staticmethod
    def generate_recommendations(
        primary_root_cause: str,
        machine_id: str,
        tool_id: str = "T-14",
        deviation: float = 0.42
    ) -> List[CorrectiveActionItem]:
        actions: List[CorrectiveActionItem] = []

        if primary_root_cause == "Tool Wear":
            actions.append(CorrectiveActionItem(
                type="Immediate",
                priority="High",
                action=f"Lock out machine {machine_id} and replace cutting tool {tool_id} (Carbide End Mill).",
                reason=f"Tool {tool_id} has exceeded maximum safe cycle threshold (1842 cycles vs 1500 limit) exhibiting severe flank wear and cutting edge dulling.",
                expected_impact="Immediately eliminates cutting force overload and restores nominal dimensional geometry.",
                target_component_or_tool=f"{machine_id} / Tool {tool_id}"
            ))
            actions.append(CorrectiveActionItem(
                type="Immediate",
                priority="High",
                action=f"Perform optical tool setter length and diameter recalibration for {tool_id}.",
                reason="Ensure newly mounted tool offset register in CNC controller is zeroed against reference datum.",
                expected_impact="Prevents step errors and maintains ±0.02 mm machining accuracy.",
                target_component_or_tool=f"{machine_id} Tool Offset Register"
            ))
            actions.append(CorrectiveActionItem(
                type="Immediate",
                priority="Medium",
                action="Quarantine preceding 15 components machined on CNC-07 for 100% CMM dimensional inspection.",
                reason="Dimensional drift trend indicates prior components may be borderline out-of-tolerance.",
                expected_impact="Prevents non-conforming parts from reaching downstream assembly.",
                target_component_or_tool="WIP Batch CNC-2833 to CNC-2847"
            ))

            # Preventive Actions
            actions.append(CorrectiveActionItem(
                type="Preventive",
                priority="High",
                action="Lower automatic tool-cycle replacement warning threshold from 1500 to 1400 cycles.",
                reason="Statistical analysis shows tool degradation steepens sharply beyond 1450 cycles on tough alloy materials.",
                expected_impact="Eliminates unexpected tool wear dimensional blowouts before tolerance breach.",
                target_component_or_tool="CNC Tool Life Management System"
            ))
            actions.append(CorrectiveActionItem(
                type="Preventive",
                priority="Medium",
                action="Enable real-time spindle power surge and vibration threshold interlock on CNC controller.",
                reason="Automatically pause cycle or prompt operator if spindle power spikes >15% over nominal baseline.",
                expected_impact="Zero-latency early detection of tool chipping or edge wear.",
                target_component_or_tool=f"{machine_id} Telemetry Monitor"
            ))
            actions.append(CorrectiveActionItem(
                type="Preventive",
                priority="Standard",
                action="Schedule weekly automated maintenance review for overdue tool replacement flags.",
                reason="Prevent tool maintenance tickets from staying in 'Overdue' state across shifts.",
                expected_impact="Increases Overall Equipment Effectiveness (OEE) and standardizes shift handovers.",
                target_component_or_tool="Plant Maintenance ERP"
            ))

        elif primary_root_cause == "Excessive Vibration":
            actions.append(CorrectiveActionItem(
                type="Immediate",
                priority="High",
                action=f"Inspect tool holder collet tightness, chuck jaw pressure, and runout (<3 µm) on {machine_id}.",
                reason="Spindle vibration telemetry is elevated at 3.75 mm/s, causing harmonic surface chattering.",
                expected_impact="Restores spindle dynamic stability and surface finish quality.",
                target_component_or_tool=f"{machine_id} Spindle Collet"
            ))
            actions.append(CorrectiveActionItem(
                type="Preventive",
                priority="High",
                action="Perform scheduled dynamic spindle balancing and bearing acoustic vibration inspection.",
                reason="Detect early mechanical bearing race fatigue before catastrophic spindle seizure.",
                expected_impact="Prevents unscheduled spindle rebuild downtime.",
                target_component_or_tool=f"{machine_id} Spindle Cartridge"
            ))
        else:
            actions.append(CorrectiveActionItem(
                type="Immediate",
                priority="High",
                action=f"Verify G-code cutting parameters and reset tool offset on {machine_id}.",
                reason="Cross-check programmed parameters against CAM post-processor verification.",
                expected_impact="Restores nominal process control.",
                target_component_or_tool=machine_id
            ))
            actions.append(CorrectiveActionItem(
                type="Preventive",
                priority="Medium",
                action="Audit operator parameter override permissions and calibration schedules.",
                reason="Standardize operating procedures across shifts.",
                expected_impact="Prevents accidental parameter drift.",
                target_component_or_tool="Quality SOP"
            ))

        return actions
