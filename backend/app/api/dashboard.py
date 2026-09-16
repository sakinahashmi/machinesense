from fastapi import APIRouter
from app.services.data_service import DataService
from app.schemas.dashboard import DashboardOverviewResponse, DashboardMetrics, RecentInvestigationItem, FleetInsightItem

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/overview", response_model=DashboardOverviewResponse)
def get_dashboard_overview():
    # 1. Fetch live machine data & compute health metrics
    machines_summary = []
    machine_ids = [f"CNC-{i:02d}" for i in range(1, 9)]
    crit_count = 0
    warn_count = 0
    health_count = 0

    machine_models = {
        "CNC-01": ("DMG MORI NVX 5080", 3),
        "CNC-02": ("Haas VF-4SS", 3),
        "CNC-03": ("Mazak Variaxis i-600", 5),
        "CNC-04": ("Okuma Genos M560-V", 3),
        "CNC-05": ("Doosan DNM 5700", 3),
        "CNC-06": ("Makino PS105", 3),
        "CNC-07": ("Hermle C42 U", 5),
        "CNC-08": ("Chiron FZ 15W", 4)
    }

    for mid in machine_ids:
        latest = DataService.get_latest_machine_telemetry(mid)
        maint_df = DataService.get_maintenance_history(machine_id=mid)
        model, axes = machine_models.get(mid, ("CNC Machining Center", 3))

        vib = float(latest.get("vibration", 1.2))
        temp = float(latest.get("temperature", 38.0))
        power = float(latest.get("power_consumption", 4.1))
        tool = str(latest.get("tool_id", "T-01"))
        cycles = int(latest.get("cycle_count", 650))

        # Dynamic health & anomaly evaluation
        health_eval = DataService.calculate_machine_health(latest, maint_df)
        status = health_eval["status"]
        health_score = health_eval["health_score"]
        active_issues = health_eval["active_issues"]

        if status == "Critical":
            crit_count += 1
        elif status == "Warning":
            warn_count += 1
        else:
            health_count += 1

        last_maint = DataService.get_machine_last_maintenance_text(mid)

        machines_summary.append({
            "machine_id": mid,
            "model": model,
            "axes": axes,
            "status": status,
            "health_score": health_score,
            "current_tool": tool,
            "vibration": round(vib, 2),
            "temperature": round(temp, 1),
            "power_consumption": round(power, 2),
            "cycle_count": cycles,
            "last_maintenance": last_maint,
            "active_issues": active_issues
        })

    # 2. Get Dynamic Investigations from SQLite
    persisted_invs = DataService.get_investigations(limit=10)
    recent_invs = []
    if persisted_invs:
        for inv in persisted_invs:
            recent_invs.append(RecentInvestigationItem(
                investigation_id=inv["investigation_id"],
                component_id=inv["component_id"],
                machine_id=inv["machine_id"],
                failure_type=inv["failure_type"],
                primary_root_cause=inv["primary_root_cause"],
                confidence=inv["confidence"],
                severity=inv["severity"],
                status=inv["status"],
                created_at=inv["created_at"]
            ))
    else:
        # Default starter seed investigations
        recent_invs = [
            RecentInvestigationItem(
                investigation_id="INV-2026-001",
                component_id="CNC-2847",
                machine_id="CNC-07",
                failure_type="Dimensional Inspection Failure",
                primary_root_cause="Tool Wear",
                confidence=94.3,
                severity="Critical",
                status="Investigated",
                created_at="2026-09-15 14:02:11"
            ),
            RecentInvestigationItem(
                investigation_id="INV-2026-002",
                component_id="CNC-2790",
                machine_id="CNC-03",
                failure_type="Surface Roughness & Chattering",
                primary_root_cause="Excessive Vibration",
                confidence=74.2,
                severity="Warning",
                status="Closed",
                created_at="2026-09-14 11:24:00"
            ),
            RecentInvestigationItem(
                investigation_id="INV-2026-003",
                component_id="CNC-2680",
                machine_id="CNC-02",
                failure_type="Dimensional Undersize",
                primary_root_cause="Incorrect Feed Rate",
                confidence=81.0,
                severity="Resolved",
                status="Closed",
                created_at="2026-09-12 09:15:30"
            )
        ]

    # 3. Dynamic Fleet Insights based on live telemetry
    fleet_insights = []
    # Machine 7 insight
    m7_latest = DataService.get_latest_machine_telemetry("CNC-07")
    m7_cycles = int(m7_latest.get("cycle_count", 1832))
    m7_power = float(m7_latest.get("power_consumption", 5.31))
    m7_surge = round(((m7_power - 4.2) / 4.2) * 100.0, 1)

    fleet_insights.append(FleetInsightItem(
        id="INS-01",
        type="Critical",
        title="Tool Wear Anomaly on CNC-07",
        description=f"Tool T-14 has reached {m7_cycles:,} cycles (122.1% of 1,500 limit). Spindle cutting power is elevated +{m7_surge}%.",
        machine_id="CNC-07",
        tool_id="T-14",
        timestamp="10 mins ago",
        action_text="Investigate CNC-2847 Failure"
    ))

    # Machine 3 insight
    m3_latest = DataService.get_latest_machine_telemetry("CNC-03")
    m3_vib = round(float(m3_latest.get("vibration", 3.51)), 2)
    fleet_insights.append(FleetInsightItem(
        id="INS-02",
        type="Warning",
        title="Spindle Vibration Resonance on CNC-03",
        description=f"5-axis machine CNC-03 exhibits harmonic vibration peaks ({m3_vib} mm/s) during roughing cycles.",
        machine_id="CNC-03",
        tool_id=str(m3_latest.get("tool_id", "T-13")),
        timestamp="1 hour ago",
        action_text="Check Fixture Clamping"
    ))

    fleet_insights.append(FleetInsightItem(
        id="INS-03",
        type="Trend",
        title="Fleet Tool Cycle Pattern Correlation",
        description="Dimensional failures across recent batches correlate with tool cycle wear exceeding 1,500 cycles.",
        machine_id="Fleet-Wide",
        tool_id="All End Mills",
        timestamp="3 hours ago",
        action_text="Review Tooling Thresholds"
    ))

    # 4. Pass Rate Trend Data calculated from SQLite inspection_results
    pass_rate_trend = DataService.get_daily_pass_rate_trend(days=7)

    # 5. Dynamic Fleet KPIs from SQLite
    fpy_metrics = DataService.get_fleet_pass_rate_metrics()

    metrics = DashboardMetrics(
        first_pass_yield=fpy_metrics["first_pass_yield"],
        first_pass_yield_delta=fpy_metrics["delta"],
        active_investigations=len(recent_invs),
        critical_anomalies=crit_count,
        machines_monitored=len(machine_ids),
        healthy_machines_count=health_count,
        warning_machines_count=warn_count,
        critical_machines_count=crit_count
    )

    return DashboardOverviewResponse(
        metrics=metrics,
        machines=machines_summary,
        recent_investigations=recent_invs,
        fleet_insights=fleet_insights,
        inspection_pass_rate_trend=pass_rate_trend
    )

