import pytest
from app.services.signal_normalizer import SignalNormalizer


def test_tool_cycles_monotonicity_and_bounds():
    """Verify tool cycle severity strictly increases with accumulated machining cycles."""
    c500 = SignalNormalizer.normalize_tool_cycles(500, 1500)
    c1000 = SignalNormalizer.normalize_tool_cycles(1000, 1500)
    c1200 = SignalNormalizer.normalize_tool_cycles(1200, 1500)
    c1500 = SignalNormalizer.normalize_tool_cycles(1500, 1500)
    c1832 = SignalNormalizer.normalize_tool_cycles(1832, 1500)
    c2500 = SignalNormalizer.normalize_tool_cycles(2500, 1500)

    assert 0.0 < c500 < c1000 < c1200 < c1500 < c1832 < c2500 < 1.0
    assert c500 < 0.10  # early life
    assert 0.45 <= c1500 <= 0.55  # threshold boundary
    assert 0.75 <= c1832 <= 0.90  # accelerated tertiary wear
    assert c2500 > 0.95  # extreme overrun


def test_vibration_monotonicity_and_bounds():
    """Verify vibration evidence increases continuously from nominal to extreme chatter."""
    v1_2 = SignalNormalizer.normalize_vibration(1.2, 2.0)
    v1_5 = SignalNormalizer.normalize_vibration(1.5, 2.0)
    v2_0 = SignalNormalizer.normalize_vibration(2.0, 2.0)
    v2_8 = SignalNormalizer.normalize_vibration(2.8, 2.0)
    v3_73 = SignalNormalizer.normalize_vibration(3.73, 2.0)
    v5_0 = SignalNormalizer.normalize_vibration(5.0, 2.0)

    assert 0.0 < v1_2 < v1_5 < v2_0 < v2_8 < v3_73 < v5_0 < 1.0
    assert v1_2 < 0.15
    assert 0.20 <= v2_0 <= 0.35
    assert 0.55 <= v2_8 <= 0.70
    assert v3_73 > 0.85


def test_power_surge_monotonicity_and_bounds():
    """Verify cutting power surge produces continuous non-saturating evidence."""
    p4_2 = SignalNormalizer.normalize_power_surge(4.20, 4.20)
    p4_4 = SignalNormalizer.normalize_power_surge(4.41, 4.20)  # +5%
    p4_8 = SignalNormalizer.normalize_power_surge(4.83, 4.20)  # +15%
    p5_31 = SignalNormalizer.normalize_power_surge(5.31, 4.20) # +26.4%
    p6_0 = SignalNormalizer.normalize_power_surge(6.00, 4.20)  # +42.8%

    assert 0.0 == p4_2 < p4_4 < p4_8 < p5_31 < p6_0 < 1.0
    assert p4_4 < 0.20
    assert 0.45 <= p4_8 <= 0.60
    assert 0.75 <= p5_31 <= 0.90


def test_dimensional_deviation_monotonicity_and_bounds():
    """Verify dimensional deviation relative to tolerance produces smooth continuous evidence."""
    d0_02 = SignalNormalizer.normalize_dimensional_deviation(0.02, 0.10)  # 0.2x tol
    d0_05 = SignalNormalizer.normalize_dimensional_deviation(0.05, 0.10)  # 0.5x tol
    d0_10 = SignalNormalizer.normalize_dimensional_deviation(0.10, 0.10)  # 1.0x tol
    d0_25 = SignalNormalizer.normalize_dimensional_deviation(0.25, 0.10)  # 2.5x tol
    d0_42 = SignalNormalizer.normalize_dimensional_deviation(0.42, 0.10)  # 4.2x tol
    d0_80 = SignalNormalizer.normalize_dimensional_deviation(0.80, 0.10)  # 8.0x tol

    assert 0.0 < d0_02 < d0_05 < d0_10 < d0_25 < d0_42 < d0_80 < 1.0
    assert d0_02 < 0.05
    assert 0.20 <= d0_10 <= 0.35
    assert 0.60 <= d0_25 <= 0.80
    assert d0_42 > 0.88


def test_feed_rate_deviation_monotonicity():
    """Verify feed rate deviation evidence increases continuously."""
    f1200 = SignalNormalizer.normalize_feed_rate_deviation(1200, 1200)
    f1250 = SignalNormalizer.normalize_feed_rate_deviation(1250, 1200)
    f1350 = SignalNormalizer.normalize_feed_rate_deviation(1350, 1200)
    f1650 = SignalNormalizer.normalize_feed_rate_deviation(1650, 1200)

    assert 0.0 == f1200 < f1250 < f1350 < f1650 < 1.0
    assert f1250 < 0.30
    assert f1650 > 0.90


def test_coolant_temperature_monotonicity():
    """Verify coolant temperature deviation evidence."""
    c21_0 = SignalNormalizer.normalize_coolant_temperature(21.0, 19.0, 23.0)
    c23_8 = SignalNormalizer.normalize_coolant_temperature(23.8, 19.0, 23.0)
    c25_5 = SignalNormalizer.normalize_coolant_temperature(25.5, 19.0, 23.0)
    c28_5 = SignalNormalizer.normalize_coolant_temperature(28.5, 19.0, 23.0)

    assert c21_0 <= 0.05
    assert c21_0 < c23_8 < c25_5 < c28_5 < 1.0
    assert c23_8 < 0.30
    assert c28_5 > 0.85


def test_maintenance_status_and_life_ratio():
    """Verify maintenance evidence behavior."""
    m_new = SignalNormalizer.normalize_maintenance_status("Completed", 500, 1500)
    m_mid = SignalNormalizer.normalize_maintenance_status("Completed", 1300, 1500)
    m_overdue = SignalNormalizer.normalize_maintenance_status("Overdue", 1832, 1500)

    assert m_new < m_mid < m_overdue
    assert m_new == 0.10
    assert 0.30 <= m_mid <= 0.60
    assert m_overdue == 0.90


def test_historical_similarity_decaying_aggregation():
    """Verify historical case matching aggregates without artificial premature saturation."""
    single_match = [{"root_cause": "Tool Wear", "similarity_score": 95.0}]
    double_match = [
        {"root_cause": "Tool Wear", "similarity_score": 95.0},
        {"root_cause": "Tool Wear", "similarity_score": 92.0}
    ]
    triple_match = [
        {"root_cause": "Tool Wear", "similarity_score": 96.5},
        {"root_cause": "Tool Wear", "similarity_score": 94.2},
        {"root_cause": "Tool Wear", "similarity_score": 89.1}
    ]
    weak_match = [{"root_cause": "Tool Wear", "similarity_score": 40.0}]

    s_single = SignalNormalizer.normalize_historical_similarity(single_match, "Tool Wear")
    s_double = SignalNormalizer.normalize_historical_similarity(double_match, "Tool Wear")
    s_triple = SignalNormalizer.normalize_historical_similarity(triple_match, "Tool Wear")
    s_weak = SignalNormalizer.normalize_historical_similarity(weak_match, "Tool Wear")

    assert s_weak < s_single < s_double < s_triple < 1.0
    assert 0.55 <= s_single <= 0.70
    assert 0.75 <= s_double <= 0.88
    assert 0.90 <= s_triple <= 0.98
