from typing import List
from fastapi import APIRouter, HTTPException
from app.services.data_service import DataService
from app.schemas.machine import MachineSummary, MachineDetail, MachineTelemetryPoint

router = APIRouter(prefix="/api/machines", tags=["Machines"])

MACHINE_SPECS = {
    "CNC-01": {"model": "DMG MORI NVX 5080", "axes": 3, "nominal_power": 4.5, "nominal_vib": 1.2, "nominal_temp": 38.0},
    "CNC-02": {"model": "Haas VF-4SS", "axes": 3, "nominal_power": 4.2, "nominal_vib": 1.4, "nominal_temp": 39.5},
    "CNC-03": {"model": "Mazak Variaxis i-600", "axes": 5, "nominal_power": 5.0, "nominal_vib": 2.8, "nominal_temp": 42.0},
    "CNC-04": {"model": "Okuma Genos M560-V", "axes": 3, "nominal_power": 4.1, "nominal_vib": 1.3, "nominal_temp": 37.5},
    "CNC-05": {"model": "Doosan DNM 5700", "axes": 3, "nominal_power": 4.0, "nominal_vib": 1.1, "nominal_temp": 36.8},
    "CNC-06": {"model": "Makino PS105", "axes": 3, "nominal_power": 4.8, "nominal_vib": 1.5, "nominal_temp": 41.0},
    "CNC-07": {"model": "Hermle C42 U", "axes": 5, "nominal_power": 4.3, "nominal_vib": 1.3, "nominal_temp": 38.2},
    "CNC-08": {"model": "Chiron FZ 15W", "axes": 4, "nominal_power": 3.8, "nominal_vib": 1.2, "nominal_temp": 37.0},
}


@router.get("", response_model=List[MachineSummary])
def list_machines():
    results = []
    for mid, spec in MACHINE_SPECS.items():
        latest = DataService.get_latest_machine_telemetry(mid)
        maint_df = DataService.get_maintenance_history(machine_id=mid)

        vib = float(latest.get("vibration", spec["nominal_vib"]))
        temp = float(latest.get("temperature", spec["nominal_temp"]))
        power = float(latest.get("power_consumption", spec["nominal_power"]))
        tool = str(latest.get("tool_id", "T-01"))
        cycles = int(latest.get("cycle_count", 0))

        health_eval = DataService.calculate_machine_health(latest, maint_df)
        status = health_eval["status"]
        health = health_eval["health_score"]
        issues = health_eval["active_issues"]
        last_maint = DataService.get_machine_last_maintenance_text(mid)

        # Realistic cycle utilization percentage based on current cycle count / 1500
        cycle_util = round(min(100.0, (cycles / 1500.0) * 100.0), 1)

        results.append(MachineSummary(
            machine_id=mid,
            model=spec["model"],
            axes=spec["axes"],
            status=status,
            health_score=health,
            current_tool=tool,
            vibration=round(vib, 2),
            temperature=round(temp, 1),
            power_consumption=round(power, 2),
            last_maintenance=last_maint,
            active_issues=issues,
            cycle_utilization_pct=cycle_util
        ))
    return results


@router.get("/{machine_id}", response_model=MachineDetail)
def get_machine_detail(machine_id: str):
    if machine_id not in MACHINE_SPECS:
        raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")

    spec = MACHINE_SPECS[machine_id]
    logs_df = DataService.get_machine_logs(machine_id=machine_id)
    maint_df = DataService.get_maintenance_history(machine_id=machine_id)
    insp_df = DataService.get_inspection_records(machine_id=machine_id)

    recent_telemetry = []
    if not logs_df.empty:
        for _, row in logs_df.tail(40).iterrows():
            recent_telemetry.append(MachineTelemetryPoint(
                timestamp=str(row["timestamp"]),
                vibration=float(row["vibration"]),
                temperature=float(row["temperature"]),
                power_consumption=float(row["power_consumption"]),
                spindle_speed=int(row["spindle_speed"]),
                feed_rate=int(row["feed_rate"]),
                cycle_count=int(row["cycle_count"]),
                status=str(row.get("machine_status", "Running"))
            ))

    latest = DataService.get_latest_machine_telemetry(machine_id)
    latest_point = recent_telemetry[-1] if recent_telemetry else MachineTelemetryPoint(
        timestamp="2026-09-15 14:00:00",
        vibration=spec["nominal_vib"],
        temperature=spec["nominal_temp"],
        power_consumption=spec["nominal_power"],
        spindle_speed=6000,
        feed_rate=1200,
        cycle_count=800,
        status="Running"
    )

    health_eval = DataService.calculate_machine_health(latest, maint_df)
    status = health_eval["status"]
    health = health_eval["health_score"]
    alerts = health_eval["active_issues"]

    recent_inspections = insp_df.tail(10).to_dict(orient="records") if not insp_df.empty else []
    recent_maint = maint_df.head(10).to_dict(orient="records") if not maint_df.empty else []
    curr_tool = str(latest.get("tool_id", "T-01"))

    return MachineDetail(
        machine_id=machine_id,
        model=spec["model"],
        axes=spec["axes"],
        status=status,
        health_score=health,
        current_tool=curr_tool,
        nominal_power=spec["nominal_power"],
        nominal_vib=spec["nominal_vib"],
        nominal_temp=spec["nominal_temp"],
        latest_telemetry=latest_point,
        recent_telemetry=recent_telemetry,
        recent_inspections=recent_inspections,
        recent_maintenance=recent_maint,
        active_alerts=alerts
    )

