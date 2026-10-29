import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ---------- membership_cost: every decision, both outcomes ----------
def test_plan_not_in_price_table():
    with pytest.raises(ValueError):
        membership_cost("daily", 25, False, False)


def test_plan_in_price_table_quarterly():
    assert membership_cost("quarterly", 25, False, False) == 4000


def test_age_below_minimum():
    with pytest.raises(ValueError):
        membership_cost("monthly", 13, False, False)


def test_age_at_minimum_boundary():
    assert membership_cost("monthly", 14, False, False) == 1500


def test_age_just_below_senior_boundary():
    assert membership_cost("monthly", 59, False, False) == 1500


def test_age_at_senior_boundary():
    assert membership_cost("monthly", 60, False, False) == 1125


def test_senior_who_is_also_student_gets_senior_discount_only():
    # age >= 60 branch wins, student branch is skipped (elif)
    assert membership_cost("monthly", 60, True, False) == 1125


def test_student_under_60():
    assert membership_cost("monthly", 20, True, False) == 1350


def test_non_student_under_60_no_discount():
    assert membership_cost("yearly", 20, False, False) == 12000


def test_trainer_false_branch():
    assert membership_cost("quarterly", 30, False, False) == 4000


def test_trainer_true_non_yearly_branch():
    assert membership_cost("quarterly", 30, False, True) == 6000


def test_trainer_true_yearly_branch():
    assert membership_cost("yearly", 30, False, True) == 13500


def test_senior_student_yearly_with_trainer_all_paths_combined():
    # 12000 - 3000 = 9000; + 2000 - 500 = 10500
    assert membership_cost("yearly", 70, True, True) == 10500


# ---------- can_enter: every decision, both outcomes ----------
def test_enter_plan_inactive():
    assert can_enter(12, False, False, "F") is False


def test_enter_hour_before_open():
    assert can_enter(4, True, False, "M") is False


def test_enter_hour_at_open_boundary():
    assert can_enter(5, True, False, "M") is True


def test_enter_hour_at_close_boundary():
    assert can_enter(22, True, False, "M") is True


def test_enter_hour_after_close():
    assert can_enter(23, True, False, "M") is False


def test_enter_women_only_female_allowed():
    assert can_enter(18, True, True, "F") is True


def test_enter_women_only_male_denied():
    assert can_enter(18, True, True, "M") is False


def test_enter_regular_slot_any_gender():
    assert can_enter(18, True, False, "F") is True
    assert can_enter(18, True, False, "M") is True


# ---------- bmi_category: every branch and boundary ----------
def test_bmi_height_zero():
    with pytest.raises(ValueError):
        bmi_category(60, 0)


def test_bmi_height_negative():
    with pytest.raises(ValueError):
        bmi_category(60, -1.6)


def test_bmi_underweight():
    assert bmi_category(50, 1.8) == "underweight"


def test_bmi_lower_normal_boundary():
    # 18.5 exactly is not underweight
    assert bmi_category(18.5, 1.0) == "normal"


def test_bmi_normal():
    assert bmi_category(70, 1.75) == "normal"


def test_bmi_upper_normal_boundary():
    # 25 exactly is overweight
    assert bmi_category(25, 1.0) == "overweight"


def test_bmi_overweight():
    assert bmi_category(80, 1.75) == "overweight"


def test_bmi_obese_boundary():
    # 30 exactly is obese
    assert bmi_category(30, 1.0) == "obese"


def test_bmi_obese():
    assert bmi_category(120, 1.75) == "obese"
