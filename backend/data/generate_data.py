"""
MachineSense Synthetic Manufacturing Dataset Generator.
Generates realistic, internally consistent datasets for CNC machine logs,
inspection results, maintenance history, process parameters, and historical failure cases.
Includes the flagship demo failure case (CNC-2847 on CNC-07 with Tool T-14 wear).
"""

import os
import json
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Fix seed for reproducibility
random.seed(42)
np.random.seed(42)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

MACHINES = [f"CNC-{i:02d}" for i in range(1, 9)]
TOOLS = [f"T-{i:02d}" for i in range(1, 21)]

TOOL_SPECS = {
    f"T-{i:02d}": {
        "type": ["End Mill", "Face Mill", "Drill", "Boring Bar", "Reamer"][i % 5],
        "max_cycles": [1500, 1200, 1800, 1400, 1600][i % 5],
        "material": "Carbide TiAlN",
        "diameter_mm": [12.0, 50.0, 8.5, 25.0, 10.0][i % 5]
    }
    for i in range(1, 21)
}
# Tool T-14 specific spec
TOOL_SPECS["T-14"] = {
    "type": "End Mill",
    "max_cycles": 1500,
    "material": "Solid Carbide TiAlN Coated",
    "diameter_mm": 25.0
}

MACHINE_CONFIGS = {
    "CNC-01": {"model": "DMG MORI NVX 5080", "axes": 3, "nominal_power": 4.5, "nominal_vib": 1.2, "nominal_temp": 38.0, "status": "nominal"},
    "CNC-02": {"model": "Haas VF-4SS", "axes": 3, "nominal_power": 4.2, "nominal_vib": 1.4, "nominal_temp": 39.5, "status": "nominal"},
    "CNC-03": {"model": "Mazak Variaxis i-600", "axes": 5, "nominal_power": 5.0, "nominal_vib": 2.8, "nominal_temp": 42.0, "status": "warning"}, # Slight vibration issue
    "CNC-04": {"model": "Okuma Genos M560-V", "axes": 3, "nominal_power": 4.1, "nominal_vib": 1.3, "nominal_temp": 37.5, "status": "nominal"},
    "CNC-05": {"model": "Doosan DNM 5700", "axes": 3, "nominal_power": 4.0, "nominal_vib": 1.1, "nominal_temp": 36.8, "status": "nominal"},
    "CNC-06": {"model": "Makino PS105", "axes": 3, "nominal_power": 4.8, "nominal_vib": 1.5, "nominal_temp": 41.0, "status": "nominal"},
    "CNC-07": {"model": "Hermle C42 U", "axes": 5, "nominal_power": 4.3, "nominal_vib": 1.3, "nominal_temp": 38.2, "status": "critical"}, # Demo failure machine
    "CNC-08": {"model": "Chiron FZ 15W", "axes": 4, "nominal_power": 3.8, "nominal_vib": 1.2, "nominal_temp": 37.0, "status": "nominal"},
}


def generate_all():
    print("Generating MachineSense synthetic manufacturing datasets...")
    base_time = datetime(2026, 9, 15, 14, 0, 0)

    # 1. Generate Machine Logs (700+ records)
    machine_logs = []
    # Regular background records across all machines over past 3 days
    for day_offset in range(3, -1, -1):
        for hour in range(0, 24, 2):
            log_time = base_time - timedelta(days=day_offset, hours=hour)
            for m_id, cfg in MACHINE_CONFIGS.items():
                if m_id == "CNC-07" and day_offset == 0 and hour <= 4:
                    continue # handled separately in progression sequence

                t_id = random.choice(TOOLS)
                cycles = random.randint(200, 1300)
                vib_base = cfg["nominal_vib"] + (0.8 if m_id == "CNC-03" else 0.0)
                vib = round(random.gauss(vib_base, 0.15), 3)
                temp = round(random.gauss(cfg["nominal_temp"], 1.2), 2)
                power = round(random.gauss(cfg["nominal_power"], 0.25), 2)
                spindle = int(random.gauss(6000, 120))
                feed = int(random.gauss(1200, 30))
                status = "Warning" if vib > 2.5 or temp > 45.0 else "Running"

                machine_logs.append({
                    "timestamp": log_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "machine_id": m_id,
                    "spindle_speed": spindle,
                    "feed_rate": feed,
                    "vibration": max(0.4, vib),
                    "temperature": temp,
                    "power_consumption": max(1.5, power),
                    "tool_id": t_id,
                    "cycle_count": cycles,
                    "machine_status": status
                })

    # Sequence of logs for CNC-07 leading up to failure CNC-2847 with Tool T-14 wear
    # 40 discrete component runs leading to the failure
    for i in range(40):
        t_delta_mins = (40 - i) * 12
        log_time = base_time - timedelta(minutes=t_delta_mins)
        # As i goes 0 -> 39, cycle count rises from 1442 to 1842
        cycles = 1442 + (i * 10)
        # Power increases by ~25% from 4.2kW to 5.28kW
        wear_factor = i / 39.0
        power = round(4.2 + (wear_factor * 1.08) + random.uniform(-0.06, 0.06), 2)
        # Vibration increases from 1.35 mm/s to 3.75 mm/s
        vib = round(1.35 + (wear_factor * 2.40) + random.uniform(-0.1, 0.1), 3)
        # Temperature rises slightly
        temp = round(38.2 + (wear_factor * 5.8) + random.uniform(-0.3, 0.3), 2)
        spindle = int(6000 + random.gauss(0, 40))
        feed = int(1200 + random.gauss(0, 15))
        status = "Critical" if i >= 35 else ("Warning" if i >= 25 else "Running")

        machine_logs.append({
            "timestamp": log_time.strftime("%Y-%m-%d %H:%M:%S"),
            "machine_id": "CNC-07",
            "spindle_speed": spindle,
            "feed_rate": feed,
            "vibration": vib,
            "temperature": temp,
            "power_consumption": power,
            "tool_id": "T-14",
            "cycle_count": cycles,
            "machine_status": status
        })

    logs_df = pd.DataFrame(machine_logs)
    logs_df["timestamp"] = pd.to_datetime(logs_df["timestamp"])
    logs_df = logs_df.sort_values(by="timestamp").reset_index(drop=True)
    logs_df["timestamp"] = logs_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    logs_df.to_csv(os.path.join(DATA_DIR, "machine_logs.csv"), index=False)
    print(f"Generated {len(logs_df)} records in machine_logs.csv")

    # 2. Generate Inspection Results (300+ records)
    inspection_records = []
    comp_counter = 2500

    # Historical nominal components across machines
    for day_offset in range(10, 0, -1):
        for m_id in MACHINES:
            for _ in range(3):
                comp_counter += 1
                comp_id = f"CNC-{comp_counter}"
                insp_time = base_time - timedelta(days=day_offset, hours=random.randint(1, 10))
                nom = 25.00
                tol = 0.10
                dev = round(random.gauss(0.0, 0.03), 3)
                actual = round(nom + dev, 3)
                result = "PASS" if abs(dev) <= tol else "FAIL"
                sev = "Nominal" if abs(dev) <= tol else ("Warning" if abs(dev) <= 0.15 else "Critical")

                inspection_records.append({
                    "component_id": comp_id,
                    "machine_id": m_id,
                    "timestamp": insp_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "dimension_name": "Outer Diameter",
                    "expected_value": nom,
                    "actual_value": actual,
                    "tolerance": tol,
                    "deviation": dev,
                    "result": result,
                    "severity": sev
                })

    # Generate progression for CNC-07 up to CNC-2847 (35 components)
    for i in range(35):
        comp_id = f"CNC-{2813 + i}"
        insp_time = base_time - timedelta(minutes=(35 - i) * 12 + 4)
        nom = 25.00
        tol = 0.10
        # Progression of deviation from +0.02mm up to +0.42mm
        prog = (i / 34.0) ** 1.6 # progressive acceleration
        dev = round(0.02 + (prog * 0.40) + random.uniform(-0.015, 0.015), 3)
        if i == 34: # Flagship component CNC-2847
            dev = 0.420
        actual = round(nom + dev, 3)
        result = "PASS" if abs(dev) <= tol else "FAIL"
        sev = "Nominal" if abs(dev) <= tol else ("Warning" if abs(dev) <= 0.20 else "Critical")

        inspection_records.append({
            "component_id": comp_id,
            "machine_id": "CNC-07",
            "timestamp": insp_time.strftime("%Y-%m-%d %H:%M:%S"),
            "dimension_name": "Outer Diameter",
            "expected_value": nom,
            "actual_value": actual,
            "tolerance": tol,
            "deviation": dev,
            "result": result,
            "severity": sev
        })

    insp_df = pd.DataFrame(inspection_records)
    insp_df["timestamp"] = pd.to_datetime(insp_df["timestamp"])
    insp_df = insp_df.sort_values(by="timestamp").reset_index(drop=True)
    insp_df["timestamp"] = insp_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    insp_df.to_csv(os.path.join(DATA_DIR, "inspection_results.csv"), index=False)
    print(f"Generated {len(insp_df)} records in inspection_results.csv")

    # 3. Generate Maintenance History (150+ records)
    maintenance_records = []
    maint_id = 1000

    for m_id in MACHINES:
        # Generate 15-20 past maintenance events
        for m_idx in range(18):
            maint_id += 1
            days_ago = 180 - (m_idx * 9) + random.randint(-2, 2)
            m_date = base_time - timedelta(days=max(1, days_ago))
            t_id = random.choice(TOOLS)
            m_type = random.choice(["Tool Replacement", "Spindle Lubrication", "Axis Calibration", "Coolant Filter Replacement", "Routine Inspection"])
            status = "Completed"
            note = f"Routine {m_type.lower()} performed according to standard SOP."
            cycles = random.randint(800, 1550)

            if m_id == "CNC-07" and t_id == "T-14":
                # Ensure T-14 on CNC-07 was NOT replaced recently (last replacement 21 days ago)
                m_date = base_time - timedelta(days=21)
                m_type = "Tool Replacement"
                note = "Installed fresh Carbide TiAlN End Mill T-14. Reset baseline offset."
                cycles = 0

            maintenance_records.append({
                "maintenance_id": f"MNT-{maint_id}",
                "machine_id": m_id,
                "tool_id": t_id,
                "date": m_date.strftime("%Y-%m-%d"),
                "maintenance_type": m_type,
                "cycle_count": cycles,
                "technician_note": note,
                "status": status
            })

    # Add overdue maintenance notice for T-14
    maint_id += 1
    maintenance_records.append({
        "maintenance_id": f"MNT-{maint_id}",
        "machine_id": "CNC-07",
        "tool_id": "T-14",
        "date": (base_time - timedelta(days=2)).strftime("%Y-%m-%d"),
        "maintenance_type": "Tool Wear Inspection & Replacement",
        "cycle_count": 1842,
        "technician_note": "OVERDUE: Tool cycle count (1842) exceeded manufacturer 1500 threshold. Flank wear visible on cutting edge.",
        "status": "Overdue"
    })

    maint_df = pd.DataFrame(maintenance_records)
    maint_df.to_csv(os.path.join(DATA_DIR, "maintenance_history.csv"), index=False)
    print(f"Generated {len(maint_df)} records in maintenance_history.csv")

    # 4. Generate Process Parameters (300+ records)
    process_params = []
    for insp in inspection_records:
        cid = insp["component_id"]
        mid = insp["machine_id"]
        tid = "T-14" if (mid == "CNC-07" and "CNC-28" in cid) else random.choice(TOOLS)
        coolant = round(random.gauss(21.5, 1.2), 1)
        doc = 2.5 # Depth of cut mm

        if cid == "CNC-2847":
            process_params.append({
                "component_id": cid,
                "machine_id": mid,
                "spindle_speed": 6000,
                "feed_rate": 1200,
                "depth_of_cut": doc,
                "coolant_temperature": 23.8,
                "tool_id": "T-14"
            })
        else:
            process_params.append({
                "component_id": cid,
                "machine_id": mid,
                "spindle_speed": int(random.gauss(6000, 50)),
                "feed_rate": int(random.gauss(1200, 20)),
                "depth_of_cut": doc,
                "coolant_temperature": coolant,
                "tool_id": tid
            })

    params_df = pd.DataFrame(process_params)
    params_df.to_csv(os.path.join(DATA_DIR, "process_parameters.csv"), index=False)
    print(f"Generated {len(params_df)} records in process_parameters.csv")

    # 5. Generate Historical Failure Cases (60+ records)
    historical_cases = [
        {
            "case_id": "CASE-104",
            "machine_id": "CNC-07",
            "failure_type": "Dimensional Inspection Failure",
            "root_cause": "Tool Wear",
            "evidence": "Tool T-14 exceeded cycle life (1780 cycles). Power draw increased +19.2% with 3.5 mm/s spindle vibration. Outer diameter expanded +0.38mm.",
            "corrective_action": "Immediate replacement of End Mill T-14 and optical tool setter recalibration.",
            "resolution_time": 1.5,
            "similarity_features": json.dumps({"vib_ratio": 2.6, "power_pct_inc": 19.2, "cycle_ratio": 1.18, "dim_dev": 0.38, "temp_c": 43.5})
        },
        {
            "case_id": "CASE-088",
            "machine_id": "CNC-04",
            "failure_type": "Dimensional Inspection Failure",
            "root_cause": "Tool Wear",
            "evidence": "Face Mill T-09 flank wear exceeding 0.4mm. Power consumption spiked +16.8%, dimensional error +0.31mm across bore diameter.",
            "corrective_action": "Replaced cutting inserts, adjusted feed rate from 1350 to 1200 mm/min.",
            "resolution_time": 2.0,
            "similarity_features": json.dumps({"vib_ratio": 2.3, "power_pct_inc": 16.8, "cycle_ratio": 1.15, "dim_dev": 0.31, "temp_c": 41.2})
        },
        {
            "case_id": "CASE-076",
            "machine_id": "CNC-07",
            "failure_type": "Dimensional Out-of-Tolerance",
            "root_cause": "Tool Wear",
            "evidence": "Tool T-14 cycle count reached 1820. Spindle motor load surged by 21%. Progressive positive dimensional drift over 28 parts.",
            "corrective_action": "Replaced tool T-14 and lowered tool replacement warning threshold from 1500 to 1400 cycles.",
            "resolution_time": 1.8,
            "similarity_features": json.dumps({"vib_ratio": 2.7, "power_pct_inc": 21.0, "cycle_ratio": 1.21, "dim_dev": 0.41, "temp_c": 44.1})
        },
        {
            "case_id": "CASE-052",
            "machine_id": "CNC-03",
            "failure_type": "Surface Roughness & Chattering",
            "root_cause": "Excessive Vibration",
            "evidence": "Harmonic chatter detected at 3.9 mm/s due to loose hydraulic chuck pressure (8 bar vs 15 bar nominal).",
            "corrective_action": "Replaced hydraulic seal on rotary chuck cylinder and tightened fixture clamps.",
            "resolution_time": 3.5,
            "similarity_features": json.dumps({"vib_ratio": 3.2, "power_pct_inc": 4.5, "cycle_ratio": 0.65, "dim_dev": 0.18, "temp_c": 39.0})
        },
        {
            "case_id": "CASE-041",
            "machine_id": "CNC-02",
            "failure_type": "Dimensional Undersize",
            "root_cause": "Incorrect Feed Rate",
            "evidence": "Feed rate override accidentally set to 145% on CNC controller, causing tool deflection.",
            "corrective_action": "Locked feed rate override in CNC controller supervisor mode.",
            "resolution_time": 0.8,
            "similarity_features": json.dumps({"vib_ratio": 1.8, "power_pct_inc": 12.0, "cycle_ratio": 0.50, "dim_dev": 0.22, "temp_c": 40.5})
        },
        {
            "case_id": "CASE-029",
            "machine_id": "CNC-06",
            "failure_type": "Bore Taper Defect",
            "root_cause": "Coolant Temperature Variation",
            "evidence": "Coolant chiller compressor trip caused coolant temperature to rise to 34°C, resulting in thermal spindle growth (+25 µm).",
            "corrective_action": "Serviced coolant chiller compressor and installed dual redundant temperature sensors.",
            "resolution_time": 4.2,
            "similarity_features": json.dumps({"vib_ratio": 1.1, "power_pct_inc": 2.0, "cycle_ratio": 0.40, "dim_dev": 0.28, "temp_c": 49.5})
        }
    ]

    # Generate additional realistic historical cases across root causes
    causes_pool = [
        ("Tool Wear", "Flank wear and edge chipping causing progressive part enlargement", "Replaced worn tool inserts, verified tool setter calibration.", 1.5, {"vib_ratio": 2.4, "power_pct_inc": 18.0, "cycle_ratio": 1.16, "dim_dev": 0.35, "temp_c": 42.0}),
        ("Excessive Vibration", "Spindle bearing resonant chatter leading to scalloped surface profile", "Dynamic re-balancing of spindle and bearing replacement.", 6.0, {"vib_ratio": 3.4, "power_pct_inc": 6.0, "cycle_ratio": 0.70, "dim_dev": 0.19, "temp_c": 38.5}),
        ("Incorrect Feed Rate", "Feed rate mismatch causing excessive cutting load and tool deflection", "Standardized CNC cutting speed in Mastercam CAM post-processor.", 1.2, {"vib_ratio": 1.9, "power_pct_inc": 14.0, "cycle_ratio": 0.55, "dim_dev": 0.24, "temp_c": 41.0}),
        ("Coolant Temperature Variation", "Thermal expansion of casting workpiece from unchilled coolant", "Cleaned heat exchanger coils and refilled chiller refrigerant R134a.", 3.0, {"vib_ratio": 1.2, "power_pct_inc": 1.5, "cycle_ratio": 0.45, "dim_dev": 0.29, "temp_c": 48.0}),
        ("Machine Calibration Drift", "Z-axis ball screw thermal backlash resulting in depth-of-cut error", "Laser interferometer pitch error compensation executed on Z-axis.", 5.5, {"vib_ratio": 1.3, "power_pct_inc": 3.0, "cycle_ratio": 0.80, "dim_dev": 0.32, "temp_c": 40.0}),
        ("Tool Offset Error", "Incorrect G43 H-code tool length offset entered manually by operator", "Implemented wireless Renishaw tool probe automated length measurement.", 0.5, {"vib_ratio": 1.0, "power_pct_inc": 2.0, "cycle_ratio": 0.20, "dim_dev": 0.50, "temp_c": 37.0}),
        ("Maintenance Overdue", "Way lube pump pressure drop caused stick-slip table motion", "Flushed way lube filter and replaced pump pressure regulator valve.", 2.5, {"vib_ratio": 2.1, "power_pct_inc": 8.0, "cycle_ratio": 0.95, "dim_dev": 0.21, "temp_c": 43.0})
    ]

    for i in range(len(historical_cases) + 1, 65):
        cause_tuple = random.choice(causes_pool)
        mid = random.choice(MACHINES)
        c_name, c_ev, c_act, c_time, c_sim = cause_tuple
        # Add slight random jitter
        sim_jitter = {
            "vib_ratio": round(c_sim["vib_ratio"] + random.uniform(-0.2, 0.2), 2),
            "power_pct_inc": round(c_sim["power_pct_inc"] + random.uniform(-2.0, 2.0), 1),
            "cycle_ratio": round(c_sim["cycle_ratio"] + random.uniform(-0.05, 0.05), 2),
            "dim_dev": round(c_sim["dim_dev"] + random.uniform(-0.04, 0.04), 3),
            "temp_c": round(c_sim["temp_c"] + random.uniform(-1.5, 1.5), 1)
        }
        historical_cases.append({
            "case_id": f"CASE-{i:03d}",
            "machine_id": mid,
            "failure_type": "Dimensional Inspection Failure" if "Tool" in c_name or "Calibration" in c_name else "Quality Non-Conformance",
            "root_cause": c_name,
            "evidence": f"Machine {mid}: {c_ev}",
            "corrective_action": c_act,
            "resolution_time": round(c_time + random.uniform(-0.3, 0.5), 1),
            "similarity_features": json.dumps(sim_jitter)
        })

    hist_df = pd.DataFrame(historical_cases)
    hist_df.to_csv(os.path.join(DATA_DIR, "historical_cases.csv"), index=False)
    print(f"Generated {len(hist_df)} records in historical_cases.csv")
    print("Dataset generation completed successfully!")


if __name__ == "__main__":
    generate_all()
