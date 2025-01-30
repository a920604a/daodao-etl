## User
- id NOT NULL
- birthDay
- gender
- education_stage R
- tagList R
- contact_id NOT NULL R
- location_id NOT NULL R
- nickname NOT NULL R
- role_list
- is_open_profile (公開個人頁面尋找夥伴)
- basic_info_id NOT NULL


- created_at
- created_by
- updated_at
- updated_by



- recommend_resource_id_list
- activity_id_list

## location
- location_id
- text
- is_open_location (公開顯示居住地)

## contact
- contact_id
- google_id
- photo_url
- is_subscribe_email NOT NULL
- email NOT NULL
- ig
- discord
- line
- fb


## Partners
- partner_id (user_id)
- basic_info_id


- activity_id_list
- recommend_resource_id_list


## basic_info
- basic_info_id 
- self_introduction R
- interest_list 可分享 R
- want_to_do_list R (interaction, do-project, make-group-class, find-group, find-teacher, find-student)


## activity
- activity_id
- user_id NOT NULL
- title 
- photoURL
- photoALT
- category
- partnerEducationStep
- description
- area
- isGrouping
- updatedDate

- time
- partnerStyle
- tagList


- createdDate
- created_at
- created_by
- updated_at
- updated_by


## resource
- resource_id NOT NULL


- image_url
- resource_name NOT NULL
- cost NOT NULL
- tagList NOT NULL
- username (user_id) NOT NULL
- age_list NOT NULL
- type_list NOT NULL


- url_link 
- filed_name_list
- video_url
- introduction
- area
- 補充資料

## Store
- store_id NOT NULL
- name
- image
- author_list (user_list_id)
- tags
- created_at


- ai_summary
- description
- content