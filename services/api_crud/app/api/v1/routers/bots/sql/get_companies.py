from sqlmodel import text

get_companies_sql = text("""
WITH base AS (
    SELECT
        companies.id    AS company_id,
        companies.code  AS company_code,

        EXISTS (
            SELECT 1
            FROM        subscriptions AS sub
            JOIN        bots ON bots.id = sub.bot_id
            WHERE       sub.company_id = companies.id
                AND     sub.is_active = TRUE
                AND     bots.name = :bot_name
        ) AS subscription_status,

        reels.label     AS reel_label,

        jsonb_build_object(
            'id', processes.id,
            'code', processes.code,
            'alias', process_reel_links.process_alias
        ) AS process_obj
    FROM companies
    JOIN operational_units
        ON operational_units.company_id = companies.id
    JOIN processes
        ON processes.operational_unit_id = operational_units.id
        AND processes.is_active = TRUE
    JOIN process_reel_links
        ON process_reel_links.process_id = processes.id
    JOIN reels
        ON reels.id = process_reel_links.reel_id
        AND reels.is_active = TRUE
),
reel_per_company AS (
    SELECT
        company_id,
        company_code,
        subscription_status,
        reel_label,

        jsonb_agg(
            process_obj ORDER BY (process_obj ->> 'alias')
        ) AS processes
    FROM (
        SELECT DISTINCT
            company_id, company_code, subscription_status, reel_label,
            process_obj
        FROM base
    )
    GROUP BY company_id, company_code, subscription_status, reel_label
),
company_rows AS (
    SELECT
        company_id,
        company_code,
        subscription_status,
        jsonb_agg(
            jsonb_build_object(
                'label', reel_label,
                'processes', processes
            ) ORDER BY reel_label
        ) AS reels
    FROM reel_per_company
    GROUP BY company_id, company_code, subscription_status
)
SELECT jsonb_object_agg(
    company_code,
    jsonb_build_object(
        'company_id',           company_id,
        'subscription_active',  subscription_status,
        'reels',                COALESCE(reels, '[]'::jsonb)
    )
)
FROM company_rows
""")