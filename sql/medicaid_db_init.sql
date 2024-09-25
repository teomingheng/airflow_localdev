CREATE SCHEMA IF NOT EXISTS medicaid;

CREATE TABLE IF NOT EXISTS medicaid.listing (
  mmis_id text,
  npi text,
  mmis_name text,
  medicaid_type text,
  profession_or_service text,
  provider_specialty text,
  service_address text,
  city text,
  us_state text,
  zip_code text,
  county text,
  telephone text,
  latitude text,
  longitude text,
  enrollment_begin_date timestamp,
  next_anticipated_revalidation_date timestamp,
  updated timestamp,
  medically_fragile_children_directory_ind text
);
