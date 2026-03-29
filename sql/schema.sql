create extension if not exists pgcrypto;

create table if not exists profiles (
    id uuid primary key default gen_random_uuid(),
    display_name text,
    created_at timestamptz not null default now()
);

create table if not exists birth_profiles (
    id uuid primary key default gen_random_uuid(),
    profile_id uuid not null references profiles(id) on delete cascade,
    birth_date date not null,
    birth_time text not null,
    birth_location text not null,
    year_anchor text not null default 'birthday',
    preferences jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists reports (
    id uuid primary key default gen_random_uuid(),
    profile_id uuid not null references profiles(id) on delete cascade,
    target_year integer not null,
    input_snapshot jsonb not null,
    report_json jsonb not null,
    created_at timestamptz not null default now()
);

create table if not exists llm_generations (
    id uuid primary key default gen_random_uuid(),
    report_id uuid not null references reports(id) on delete cascade,
    provider text not null,
    mode text not null,
    prompt_version text,
    output_text text not null,
    created_at timestamptz not null default now()
);

