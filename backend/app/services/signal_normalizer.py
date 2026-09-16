import numpy as np
from typing import List, Dict, Any, Union


class SignalNormalizer:
    """
    Continuous Mathematical Signal Normalization for Manufacturing Root Cause Analysis.
    
    Converts raw physical sensor deviations and maintenance/history records into 
    continuous normalized evidence scores in [0.0, 1.0] without premature clipping.
    """

    @staticmethod
    def normalize_tool_cycles(cycle_count: float, max_cycles: float = 1500.0) -> float:
        """
        Continuous tool cycle wear severity function based on Taylor's tool life curve.
        
        Formula:
          r = cycle_count / max_cycles
          S_cycles(r) = 1 / (1 + exp(-7.0 * (r - 1.0)))
          
        Characteristics:
          - r = 0.33 (500 cycles)  -> 0.01
          - r = 0.80 (1200 cycles) -> 0.18 (early/moderate life)
          - r = 1.00 (1500 cycles) -> 0.50 (rated replacement threshold boundary)
          - r = 1.22 (1832 cycles) -> 0.82 (accelerated tertiary flank wear)
          - r = 1.50 (2250 cycles) -> 0.97 (extreme overrun)
        """
        if max_cycles <= 0:
            return 0.50
        r = float(cycle_count) / float(max_cycles)
        score = 1.0 / (1.0 + np.exp(-7.0 * (r - 1.0)))
        return float(np.clip(score, 0.001, 0.999))

    @staticmethod
    def normalize_vibration(vibration: float, nominal_max: float = 2.0) -> float:
        """
        Continuous dynamic spindle vibration severity function based on ISO 10816 standards.
        
        Formula:
          r = vibration / nominal_max
          S_vib(r) = 1 / (1 + exp(-4.5 * (r - 1.25)))
          
        Characteristics:
          - 1.2 mm/s (nominal smooth) -> 0.07
          - 2.0 mm/s (alert threshold) -> 0.24
          - 2.8 mm/s (elevated chatter)-> 0.61
          - 3.73 mm/s (heavy resonance)-> 0.94
          - 4.5 mm/s (extreme unbalance)-> 0.98
        """
        if nominal_max <= 0:
            return 0.50
        r = float(vibration) / float(nominal_max)
        score = 1.0 / (1.0 + np.exp(-4.5 * (r - 1.25)))
        return float(np.clip(score, 0.001, 0.999))

    @staticmethod
    def normalize_power_surge(power: float, baseline: float = 4.20) -> float:
        """
        Continuous spindle cutting force surge function.
        Blunted cutting edges increase specific cutting energy and spindle motor torque draw.
        
        Formula:
          pct_surge = max(0, ((power - baseline) / baseline) * 100)
          S_power = 1 - exp(- (pct_surge / 18.0)^1.5)
          
        Characteristics:
          - +0.0% surge (4.20 kW baseline) -> 0.00
          - +5.0% surge (4.41 kW minor load) -> 0.14
          - +15.0% surge (4.83 kW noticeable wear) -> 0.53
          - +26.4% surge (5.31 kW heavy flank wear) -> 0.83
          - +40.0% surge (5.88 kW severe choking) -> 0.96
        """
        if baseline <= 0:
            return 0.50
        pct_surge = max(0.0, ((float(power) - float(baseline)) / float(baseline)) * 100.0)
        score = 1.0 - np.exp(-((pct_surge / 18.0) ** 1.5))
        return float(np.clip(score, 0.0, 0.999))

    @staticmethod
    def normalize_dimensional_deviation(deviation: float, tolerance: float = 0.10) -> float:
        """
        Continuous dimensional tolerance deviation function.
        
        Formula:
          u = |deviation| / tolerance
          S_dim = 1 - exp(- (u / 2.2)^1.6)
          
        Characteristics:
          - |dev| = 0.02 mm (0.2x tol) -> 0.02 (within normal 6-sigma process capability)
          - |dev| = 0.10 mm (1.0x tol) -> 0.25 (tolerance boundary)
          - |dev| = 0.25 mm (2.5x tol) -> 0.70 (significant out-of-tolerance)
          - |dev| = 0.42 mm (4.2x tol) -> 0.94 (critical dimensional failure)
          - |dev| = 0.80 mm (8.0x tol) -> 0.999 (extreme gross geometry breach)
        """
        if tolerance <= 0:
            return 0.50
        u = abs(float(deviation)) / float(tolerance)
        score = 1.0 - np.exp(-((u / 2.2) ** 1.6))
        return float(np.clip(score, 0.0, 0.999))

    @staticmethod
    def normalize_feed_rate_deviation(feed_rate: float, nominal: float = 1200.0) -> float:
        """
        Continuous feed rate override deviation function.
        
        Formula:
          delta_f = |feed_rate - nominal|
          S_feed = 1 - exp(- (delta_f / 130.0)^1.6)
          
        Characteristics:
          - delta_f = 4 mm/min (1196 nominal) -> 0.004
          - delta_f = 50 mm/min (1250 minor override) -> 0.20
          - delta_f = 100 mm/min (1300 noticeable override) -> 0.48
          - delta_f = 200 mm/min (1400 severe override) -> 0.86
          - delta_f = 450 mm/min (1650 extreme override) -> 0.999
        """
        df = abs(float(feed_rate) - float(nominal))
        score = 1.0 - np.exp(-((df / 130.0) ** 1.6))
        return float(np.clip(score, 0.0, 0.999))

    @staticmethod
    def normalize_coolant_temperature(
        temp: float,
        target_min: float = 19.0,
        target_max: float = 23.0
    ) -> float:
        """
        Continuous coolant fluid temperature deviation function.
        
        Formula:
          delta_t = max(0, temp - target_max, target_min - temp)
          If delta_t == 0: 0.05
          Else: 0.05 + 0.95 * (1 - exp(- (delta_t / 2.8)^1.4))
          
        Characteristics:
          - 21.5 °C (in window) -> 0.05
          - 23.8 °C (+0.8 °C elevation) -> 0.20
          - 25.5 °C (+2.5 °C high elevation) -> 0.60
          - 28.5 °C (+5.5 °C severe chiller failure) -> 0.93
        """
        t = float(temp)
        dt = max(0.0, t - float(target_max), float(target_min) - t)
        if dt == 0.0:
            return 0.05
        score = 0.05 + 0.95 * (1.0 - np.exp(-((dt / 2.8) ** 1.4)))
        return float(np.clip(score, 0.05, 0.999))

    @staticmethod
    def normalize_maintenance_status(
        status: str,
        cycle_count: float,
        max_cycles: float = 1500.0
    ) -> float:
        """
        Deterministic maintenance evidence function.
        
        Characteristics:
          - status == 'Overdue' -> 0.90
          - status == 'Completed' and cycle ratio < 0.70 -> 0.10
          - status == 'Completed' and cycle ratio 0.85 -> 0.35
          - status == 'Completed' and cycle ratio 1.00 -> 0.60
        """
        if status == "Overdue":
            return 0.90
        r = float(cycle_count) / float(max_cycles) if max_cycles > 0 else 0.5
        score = 0.10 + 0.50 * max(0.0, min(1.0, (r - 0.70) / 0.30))
        return float(np.clip(score, 0.05, 0.90))

    @staticmethod
    def normalize_historical_similarity(
        matches: List[Union[Dict[str, Any], Any]],
        root_cause: str
    ) -> float:
        """
        Continuous geometric decaying aggregation for historical case similarity.
        Differentiates between 1 strong match vs multiple corroborating matches without hard clipping.
        
        Formula:
          c_matches = sorted similarities for target root cause (descending) in [0.0, 1.0]
          S_hist = sum(w_j * s_j) for j in 1..3, weights = [0.65, 0.22, 0.13]
          
        Characteristics:
          - 1 match at 0.95 -> 0.65 * 0.95 = 0.618
          - 2 matches at (0.95, 0.92) -> 0.65(0.95) + 0.22(0.92) = 0.820
          - 3 matches at (0.965, 0.942, 0.891) -> 0.65(0.965) + 0.22(0.942) + 0.13(0.891) = 0.950
          - 1 weak match at 0.40 -> 0.260
        """
        c_matches = []
        for m in matches:
            if hasattr(m, "root_cause") and hasattr(m, "similarity_score"):
                if m.root_cause == root_cause:
                    c_matches.append(float(m.similarity_score) / 100.0)
            elif isinstance(m, dict):
                if m.get("root_cause") == root_cause:
                    c_matches.append(float(m.get("similarity_score", 0.0)) / 100.0)

        if not c_matches:
            return 0.0

        c_matches.sort(reverse=True)
        weights = [0.65, 0.22, 0.13]
        total = sum(w * s for w, s in zip(weights, c_matches[:3]))
        return float(np.clip(total, 0.0, 0.999))

    @staticmethod
    def normalize_calibration_drift(
        days: float,
        deviation: float,
        tolerance: float = 0.10
    ) -> float:
        """
        Continuous calibration drift function based on laser calibration age and dimensional bias.
        """
        d_score = min(1.0, float(days) / 180.0)
        dim_score = SignalNormalizer.normalize_dimensional_deviation(deviation, tolerance)
        score = 0.40 * d_score + 0.35 * dim_score + 0.25 * 0.05
        return float(np.clip(score, 0.05, 0.999))
