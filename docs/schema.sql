-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. Licenses Table
create table if not exists licenses (
    key text primary key,
    owner_name text not null,
    school_name text,
    status text default 'active', -- 'active', 'expired', 'suspended'
    created_at timestamp with time zone default now()
);

-- 2. Question Bank Table
create table if not exists question_bank (
    id uuid primary key default uuid_generate_v4(),
    subject text not null, -- e.g. 'IPA', 'Matematika'
    grade text not null,   -- e.g. 'SD Kelas 5'
    topic text,            -- e.g. 'Sistem Pencernaan'
    question_type text,    -- 'Pilihan Ganda', 'Isian', 'Uraian'
    question_text text not null,
    options jsonb,         -- Array of strings for MCQ options
    answer_key text,
    taxonomy text,         -- Bloom's taxonomy level (C1-C6)
    source_file text,      -- Filename of where this came from (for tracing)
    created_at timestamp with time zone default now()
);

-- RLS Policies (Optional but recommended)
alter table licenses enable row level security;
alter table question_bank enable row level security;

-- Allow read access to all authenticated users (or anon if using public key for this app logic)
create policy "Public read access" on question_bank for select using (true);
create policy "Public insert access" on question_bank for insert with check (true);
