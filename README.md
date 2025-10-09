# PiLock

Everything lives in one DB (modular monolith)

## User Management bounded context

- `User`
  - id (PK)
  - organization_identifier (identifier from the organization)
  - firstname
  - lastname
  - email

## Web bounded context  
- `WebUser`
  - user_id (PK, FK from `User.id`, 01:1)
  - hashed_password: str
  - created_on: timestamp
  - deactivated_on: timestamp|NULL
  - email (readonly, resolved from `User` at read time; not stored here)


- `WebSession`
  - id (PK)
  - webuser_id (from `WebUser.user_id`, *:1)
  - created_on: timestamp
  - token: string
  - last_use: timestamp
  - expiration: timestamp

## Tag bounded context
- `RFIDTag`
  - id (PK, surrogate of [user_id, tag_id])
  - user_id (FK from `User`, +:1)
  - tag_id (the actual identifier of the tag)
  - created_on (timestamp)
  - deactivated_on (timestamp|NULL)

- `AccessLog`
  - id (PK, surrogate of [timestamp, rfid_tag_id])
  - timestamp
  - rfid_tag_id (from `RFIDTag.tag_id`)
  - event (enum: `OPEN`, `CLOSE`)
  - user_id (FK from `User.id`)
  - user_info -> (first_name, last_name) (readonly, resolved from `User` at read time; not stored here)
