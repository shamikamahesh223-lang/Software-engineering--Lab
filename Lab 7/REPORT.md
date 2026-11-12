# Lab 7 Report — Fuzz Testing for Input Validation Bugs

**Student:** Shamika  
**Assigned repository:** `SETAPESU26/L6_L7_21_gym_membership`  
**Lab folder:** `Lab 7`

## 1. Objective
Explore fuzz testing as a security and quality-assurance technique by applying the Hypothesis property-based testing library to the assigned gym membership application, identifying edge cases, and improving input validation.

## 2. Application under test
The assigned repository's Lab 7 folder contains `gym_membership.py` and `test_gym_membership.py`. The three functions tested are:
- `parse_plan(code)` — parses a plan code and membership duration.
- `calculate_bmi(data)` — parses weight and height and calculates BMI.
- `average_workout(minutes)` — calculates the average of workout-minute values.

The handout uses the generic names `processor.py` and `test_processor.py`; this submission retains the actual repository filenames.

## 3. Baseline execution and fuzzing
The original application was run with valid sample inputs:
- Plan code: `GOLD-12`
- Weight and height: `70,1.75`
- Workout minutes: `45 60 30`

The application returned `('GOLD', 12)`, BMI `22.9`, and average workout minutes `45`.

Hypothesis was then run against the original buggy module. The captured pytest summary showed **4 failed and 3 passed**. One minimized failure shown in the terminal was `None` passed to `parse_plan`, causing an `AttributeError` because `None` has no `split` method. The other fuzz tests also exposed invalid-input failures in the BMI and workout processing functions.

## 4. Fixes implemented
- `parse_plan`: validates the input type, exact field count, alphabetic plan name, numeric month count, and positive duration. Invalid input returns `None`.
- `calculate_bmi`: validates input type and format, numeric conversion, finite values, and positive weight and height. Invalid or unsafe calculations return `None`.
- `average_workout`: validates input type, rejects empty input and invalid integer tokens, and rejects negative minute values. Invalid input returns `None`.
- The interactive application prints readable validation messages instead of terminating on malformed values.

## 5. Final verification
After switching the tests to import the fixed `gym_membership` module, the user ran:

`python3 -m pytest -v test_gym_membership.py`

The captured terminal output (Python 3.13.7, pytest 9.2.0, Hypothesis 6.170.15) reports **7 passed in 0.38s** and no failures.

The four genuine screenshots captured during the lab run are included in the `screenshots/` directory:
1. Original application with valid sample inputs.
2. Hypothesis failures against the buggy implementation.
3. Fixed application with the same valid sample inputs.
4. Final Hypothesis run with all seven tests passing.

## 6. Conclusion
Hypothesis exposed edge cases that ordinary valid-input demonstrations did not reveal. Defensive input validation was added to all three functions, and the final property-based and regression test suite passed on the student's Mac environment.
