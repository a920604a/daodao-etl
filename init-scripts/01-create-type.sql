-- TYPE

CREATE TYPE "gender_t" AS ENUM ('male', 'female', 'other');
CREATE TYPE "education_stage_t" AS ENUM ('university', 'high', 'other');
CREATE TYPE "role_list_t" AS ENUM (
    'normal-student',
    'citizen',
    'experimental-educator',
    'other',
    'parents',
    'experimental-education-student'
);

CREATE TYPE "city_t" AS ENUM (
    'Taipei City',
    'Keelung City',
    'New Taipei City',
    'Lianjiang County',
    'Taoyuan City',
    'Hsinchu City',
    'Hsinchu County',
    'Miaoli County',
    'Taichung City',
    'Changhua County',
    'Yunlin County',
    'Chiayi County',
    'Chiayi City',
    'Tainan City',
    'nantou county',
    'kaohsiung city',
    'Pingtung County',
    'Hainan Island',
    'Penghu County',
    'Kinmen County',
    'Yilan County',
    'Hualien County',
    'Taitung County',
    'Other'
);


CREATE TYPE "want_to_do_list_t" AS ENUM (
    'interaction',
    'do-project',
    'make-group-class',
    'find-student',
    'find-teacher',
    'find-group'
);

CREATE TYPE "group_type_t" AS ENUM (
    'reading club',
    'workshop',
    'project',
    'competition',
    'Activity',
    'Societies',
    'course',
    'practice',
    'other'
);
CREATE TYPE "partner_education_step_t" AS ENUM ('high school', 'other', 'University');


CREATE TYPE "cost_t" AS ENUM ('free', 'part', 'payment');
CREATE TYPE "age_t" AS ENUM ('preschool', 'Elementary', 'high', 'University');


CREATE TYPE "freqency_t" AS ENUM ( 'two', 'one', 'three', 'month');

CREATE TYPE "qualifications_t" AS ENUM (
    'low_income',
    'discount',
    'personal',
    'double',
    'three',
    'four'
);

CREATE TYPE "role_t" AS ENUM ('Initiator', 'Participant');


CREATE TYPE "motivation_t" AS ENUM (
    'driven_by_curiosity',
    'interest_and_passion',
    'self_challenge',
    'personal_growth',
    'career_development',
    'pursuing_education_or_qualifications',
    'social_recognition',
    'exploring_possibilities',
    'preparing_for_the_future',
    'innovation_and_development',
    'practical_needs',
    'inspired_by_events',
    'interpersonal_connections',
    'life_changes',
    'impact_on_society',
    'influenced_by_a_group',
    'others'
);

CREATE TYPE "policy_t" AS ENUM (
    'data_collection_research_analysis',
    'book_reading',
    'watching_videos',
    'listening_to_podcasts',
    'examinations',
    'participating_in_competitions',
    'finding_study_partners',
    'joining_communities',
    'consulting_experts_and_scholars',
    'doing_projects',
    'initiating_actions',
    'field_internship',
    'organizing_events_or_courses',
    'attending_events_or_courses',
    'field_research',
    'conducting_interviews',
    'conducting_surveys',
    'others'
);
CREATE TYPE "presentation_t" AS ENUM (
    'building_websites',
    'managing_social_media',
    'writing_research_reports',
    'artistic_creation',
    'initiating_projects_or_organizations',
    'making_videos',
    'organizing_events',
    'teaching_courses',
    'participating_in_competitions',
    'others'
);