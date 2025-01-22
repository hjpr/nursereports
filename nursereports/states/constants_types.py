from typing import Literal

#################################################################
# COMPENSATION
#################################################################
COMP_SELECT_EMP_TYPE_SELECTIONS = ["Full-time", "Part-time", "Contract"]
COMP_SELECT_PAY_TYPE_SELECTIONS = ["Hourly", "Weekly"]
COMP_SELECT_SHIFT_SELECTIONS = ["Day", "Night", "Rotating"]
COMP_SELECT_WEEKLY_SHIFTS_SELECTIONS = ["Less than 1", "1", "2", "3", "4", "5"]
COMP_SELECT_HOSPITAL_EXPERIENCE = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "More than 25 years",
]

ValidEmploymentType = Literal["", "Full-time", "Part-time", "Contract"]
ValidPayType = Literal["", "Hourly", "Weekly"]
ValidCalculatorInputType = Literal[
    "", "hourly", "weekly", "night", "weekend", "weekend_night"
]
ValidShiftType = Literal["", "Day", "Night", "Rotating"]
ValidWeeklyShiftsType = Literal[
    "",
    "Less than 1",
    "1",
    "2",
    "3",
    "4",
    "5",
]
ValidHospitalExperienceType = Literal[
    "",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "More than 25 years",
]

#################################################################
# ASSIGNMENT
#################################################################
ASSIGN_SELECT_CLASSIFY_SELECTIONS = ["Unit", "Area", "Role"]
ASSIGN_SELECT_ACUITY_SELECTIONS = ["Intensive", "Intermediate", "Floor", "Mixed"]
ASSIGN_SELECT_SPECIALTY_SELECTIONS = [
    "Allergy",
    "Burn",
    "Cardiac",
    "Cardiothoracic",
    "Cardiovascular",
    "Dermatology",
    "Diabetes",
    "Education",
    "Emergency",
    "Endocrine",
    "Gastroenterology",
    "Hematology",
    "Infusion",
    "Labor & Delivery",
    "Medicine",
    "Neonatal",
    "Nephrology",
    "Neurology",
    "Neuroscience",
    "Obstetrics",
    "Occupational Health",
    "Oncology",
    "Orthopedic",
    "Pain",
    "Perinatal",
    "Perioperative",
    "Psychiatric",
    "Pulmonary",
    "Research",
    "Rheumatology",
    "Substance Abuse",
    "Surgical",
    "Toxicology",
    "Transplant",
    "Trauma",
    "Urology",
    "Wound, Ostomy, and Continence",
]
ASSIGN_SELECT_RECOMMEND_SELECTIONS = ["Yes", "No"]

ValidClassifyType = Literal["", "Unit", "Area", "Role"]
ValidAcuityType = Literal["", "Intensive", "Intermediate", "Floor", "Mixed"]
ValidSpecialtyType = Literal[
    "",
    "Allergy",
    "Burn",
    "Cardiac",
    "Cardiothoracic",
    "Cardiovascular",
    "Dermatology",
    "Diabetes",
    "Education",
    "Emergency",
    "Endocrine",
    "Gastroenterology",
    "Hematology",
    "Infusion",
    "Labor & Delivery",
    "Medicine",
    "Neonatal",
    "Nephrology",
    "Neurology",
    "Neuroscience",
    "Obstetrics",
    "Occupational Health",
    "Oncology",
    "Orthopedic",
    "Pain",
    "Perinatal",
    "Perioperative",
    "Psychiatric",
    "Pulmonary",
    "Research",
    "Rheumatology",
    "Substance Abuse",
    "Surgical",
    "Toxicology",
    "Transplant",
    "Trauma",
    "Urology",
    "Wound, Ostomy, and Continence",
]
ValidYesNoType = Literal["", "Yes", "No"]

#################################################################
# STAFFING
#################################################################
STAFFING_SELECT_RATIO_SELECTIONS = ["Yes", "No"]
STAFFING_SELECT_RATIO_APPROPRIATE = ["Yes", "No"]
STAFFING_SELECT_WORKLOAD_SELECTIONS = ["Light", "Moderate", "Heavy", "Overwhelming"]
STAFFING_SELECT_CHARGE_PRESENT_SELECTIONS = ["Yes", "No"]
STAFFING_SELECT_CHARGE_ASSIGNMENT_SELECTIONS = ["Never", "Rarely", "Sometimes", "Often", "Always"]

ValidRatioType = Literal["", "Yes", "No"]
ValidCalculatorToggleRatioType = Literal["", "actual_ratio", "ideal_ratio"]
ValidWorkloadType = Literal["", "Light", "Moderate", "Heavy", "Overwhelming"]
ValidChargeAssignmentType = Literal["", "Never", "Rarely", "Sometimes", "Often", "Always"]

