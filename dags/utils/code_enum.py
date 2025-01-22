from sqlalchemy import create_engine, Column, Integer, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM

metadata = MetaData()

gender_t = ENUM('male', 'female', 'other', name="gender_t")
education_stage_t = ENUM('university', 'high', 'other', name="education_stage_t")
identity_list_t = ENUM(
    'normal-student', 'citizen', 'experimental-educator',
    'other', 'parents', 'experimental-education-student', name="identity_list_t"
)

city_t = ENUM(
    'Taipei City', 'Keelung City', 'New Taipei City', 'Lianjiang County', 'Taoyuan City',
    'Hsinchu City', 'Hsinchu County', 'Miaoli County', 'Taichung City', 'Changhua County',
    'Yunlin County', 'Chiayi County', 'Chiayi City', 'Tainan City', 'nantou county',
    'kaohsiung city', 'Pingtung County', 'Hainan Island', 'Penghu County', 'Kinmen County',
    'Yilan County', 'Hualien County', 'Taitung County', 'Other', name="city_t"
)


partnerEducationStep_t = Enum(
    'high school','other', 'University', name = "partnerEducationStep_t"    
)

want_to_do_list_t = ENUM(
    'interaction', 'do-project', 'make-group-class',
    'find-student', 'find-teacher', 'find-group', name="want_to_do_list_t"
)
age_t = Enum(
    'preschool', 'Elementary', 'high', 'University', name="age_t"
)

cost_t = Enum('free', 'part', 'payment', name="cost_t")


group_participation_role_t = ENUM('Initiator', 'Participant', name="group_participation_role_t")
qualifications_t = ENUM(
    'low_income', 'discount', 'personal', 'double', 'three', 'four', name="qualifications_t"
)
