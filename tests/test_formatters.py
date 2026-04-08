"""Unit tests for formatting helper functions in garmin-activities.py."""

import sys
import os
import types
import importlib
import importlib.util

# Allow importing from the repo root without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Stub out external packages that aren't available in the test environment
for _stub in ("pytz", "dotenv", "garminconnect", "notion_client", "notion_client.errors"):
    if _stub not in sys.modules:
        _mod = types.ModuleType(_stub)
        if _stub == "notion_client.errors":
            _mod.APIResponseError = Exception  # type: ignore[attr-defined]
        sys.modules[_stub] = _mod

# Provide minimal attribute stubs
sys.modules["pytz"].timezone = lambda tz: None  # type: ignore[attr-defined]
sys.modules["dotenv"].load_dotenv = lambda *a, **kw: None  # type: ignore[attr-defined]
sys.modules["garminconnect"].Garmin = object  # type: ignore[attr-defined]
sys.modules["notion_client"].Client = object  # type: ignore[attr-defined]

_spec = importlib.util.spec_from_file_location(
    "garmin_activities",
    os.path.join(os.path.dirname(__file__), "..", "garmin-activities.py"),
)
garmin_activities = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(garmin_activities)  # type: ignore[union-attr]

format_hr_zone = garmin_activities.format_hr_zone
format_intensity = garmin_activities.format_intensity
format_pace = garmin_activities.format_pace
format_training_message = garmin_activities.format_training_message
format_training_effect = garmin_activities.format_training_effect
format_activity_type = garmin_activities.format_activity_type


# ---------------------------------------------------------------------------
# format_hr_zone
# ---------------------------------------------------------------------------

class TestFormatHrZone:
    def test_zero_returns_empty(self):
        assert format_hr_zone(0) == ""

    def test_none_returns_empty(self):
        assert format_hr_zone(None) == ""

    def test_zone1(self):
        assert format_hr_zone(80) == "Zone 1 · Warm Up"
        assert format_hr_zone(99) == "Zone 1 · Warm Up"

    def test_zone2(self):
        assert format_hr_zone(100) == "Zone 2 · Easy"
        assert format_hr_zone(119) == "Zone 2 · Easy"

    def test_zone3(self):
        assert format_hr_zone(120) == "Zone 3 · Aerobic"
        assert format_hr_zone(139) == "Zone 3 · Aerobic"

    def test_zone4(self):
        assert format_hr_zone(140) == "Zone 4 · Threshold"
        assert format_hr_zone(159) == "Zone 4 · Threshold"

    def test_zone5(self):
        assert format_hr_zone(160) == "Zone 5 · Max"
        assert format_hr_zone(200) == "Zone 5 · Max"


# ---------------------------------------------------------------------------
# format_intensity
# ---------------------------------------------------------------------------

class TestFormatIntensity:
    def test_none_returns_recovery(self):
        assert format_intensity(None) == "😴 Recovery"

    def test_zero_returns_recovery(self):
        assert format_intensity(0) == "😴 Recovery"

    def test_minor_benefit(self):
        assert format_intensity(1.0) == "🟢 Minor Benefit"
        assert format_intensity(1.9) == "🟢 Minor Benefit"

    def test_maintaining(self):
        assert format_intensity(2.0) == "🟡 Maintaining"
        assert format_intensity(2.9) == "🟡 Maintaining"

    def test_improving(self):
        assert format_intensity(3.0) == "🟠 Improving"
        assert format_intensity(3.9) == "🟠 Improving"

    def test_highly_impacting(self):
        assert format_intensity(4.0) == "🔴 Highly Impacting"
        assert format_intensity(4.4) == "🔴 Highly Impacting"

    def test_overreaching(self):
        assert format_intensity(4.5) == "🔴 Overreaching"
        assert format_intensity(5.0) == "🔴 Overreaching"


# ---------------------------------------------------------------------------
# format_pace
# ---------------------------------------------------------------------------

class TestFormatPace:
    def test_zero_speed_returns_empty(self):
        assert format_pace(0) == ""

    def test_typical_running_pace(self):
        # 3 m/s  →  1000 / (3 * 60) ≈ 5.555 min/km  →  "5:33 min/km"
        result = format_pace(3.0)
        assert result == "5:33 min/km"

    def test_format_structure(self):
        result = format_pace(2.5)
        assert "min/km" in result
        assert ":" in result


# ---------------------------------------------------------------------------
# format_training_message
# ---------------------------------------------------------------------------

class TestFormatTrainingMessage:
    def test_known_prefixes(self):
        assert format_training_message("NO_LOAD") == "No Benefit"
        assert format_training_message("IMPROVING_LOAD") == "Impacting"
        assert format_training_message("HIGHLY_IMPACTING") == "Highly Impacting"
        assert format_training_message("OVERREACHING_LOAD") == "Overreaching"

    def test_unknown_prefix_passthrough(self):
        assert format_training_message("UNKNOWN_THING") == "UNKNOWN_THING"


# ---------------------------------------------------------------------------
# format_training_effect
# ---------------------------------------------------------------------------

class TestFormatTrainingEffect:
    def test_underscores_replaced_and_titlecased(self):
        assert format_training_effect("AEROBIC_BASE") == "Aerobic Base"
        assert format_training_effect("HIGHLY_AEROBIC") == "Highly Aerobic"

    def test_already_clean_label(self):
        assert format_training_effect("Tempo") == "Tempo"

    def test_empty_string(self):
        assert format_training_effect("") == ""


# ---------------------------------------------------------------------------
# format_activity_type
# ---------------------------------------------------------------------------

class TestFormatActivityType:
    def test_running(self):
        t, s = format_activity_type("running")
        assert t == "Running"
        assert s == "Running"

    def test_treadmill_running(self):
        t, s = format_activity_type("treadmill_running")
        assert t == "Running"
        assert s == "Treadmill Running"

    def test_yoga(self):
        t, s = format_activity_type("yoga")
        assert t == "Yoga/Pilates"
        assert s == "Yoga"

    def test_name_override_stretch(self):
        t, s = format_activity_type("cardio", "Morning Stretching")
        assert t == "Stretching"
        assert s == "Stretching"

    def test_name_override_meditation(self):
        t, s = format_activity_type("cardio", "Guided Meditation")
        assert t == "Meditation"
        assert s == "Meditation"
