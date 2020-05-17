# -*- coding: utf-8 -*-

sql_rth1_any = u"""
    SELECT top 10
        GPS_ID, 
        DATDOC, 
        LR_NUM, 
        GOS_NUM, 
        CAST(MIN(CAST(date_out AS SQL_CHAR) + ' ' + REPLACE(IIF(LENGTH(TRIM(time_out)) = 4, '0'+TRIM(time_out), TRIM(time_out)), '.', ':') + ':00') AS SQL_TIMESTAMP) DATE_OUT, 
        CAST(MIN(CAST(date_in AS SQL_CHAR) + ' ' + REPLACE(IIF(LENGTH(TRIM(time_in)) = 4, '0'+TRIM(time_in), TRIM(time_in)), '.', ':') + ':00') AS SQL_TIMESTAMP) DATE_IN	
    FROM( 
        select 
            RGNUM, 
            numdoc, 
            datdoc, 
            dattr1 as date_out,  
            cattr2 as time_out, 
            dattr2 as date_in, 
            cattr3 as time_in, 
            trim(debt) as lr_num, 
            ifnull(replace(d3name, ' ', ''),'') as gos_num, 
            ifnull(replace(r112.regnum, ' ', ''),'') as gos_num, 
            ifnull(cast(replace(r112.GSM_CARD, ' ', '') as sql_integer),0) as gps_id, 
            KODTCAR 
        from [..\\opdata\\dict.add].docs:mmyy 
        left join [..\\reflis\\dict.add].r112 on r112.kod = danal3 
        where kinddoc = 'RTH' and lvlnum = '1' 
            and krefl2 <> 'Д' 
            and (dattr1 is not null and dattr1 <= ':date' and dattr2 = ':date') 
            and cast(replace(r112.GSM_CARD, ' ', '') as sql_integer) <> 0 
            and UPPER(LEFT(TRIM(debt),1)) NOT IN ('','K','X') 
            and TRIM(DREFL2) = '' 
        UNION 
        select 
            RGNUM, 
            numdoc, 
            datdoc, 
            dattr1 as date_out,  
            cattr2 as time_out, 
            dattr2 as date_in, 
            cattr3 as time_in, 
            trim(debt) as lr_num, 
            ifnull(replace(d3name, ' ', ''),'') as gos_num,
            ifnull(replace(r112.regnum, ' ', ''),'') as gos_num, 
            ifnull(cast(replace(r112.GSM_CARD, ' ', '') as sql_integer),0) as gps_id, 
            KODTCAR 
        from [..\\opdata\\dict.add].docs:mmyy
        left join [..\\reflis\\dict.add].r112 on r112.kod = danal3 
        where kinddoc = 'RTH' and lvlnum = '1' 
            and krefl2 <> 'Д' 
            and (dattr1 is not null and dattr1 <= ':date' and dattr2 = ':date') 
            and cast(replace(r112.GSM_CARD, ' ', '') as sql_integer) <> 0 
            and UPPER(LEFT(TRIM(debt),1)) NOT IN ('','K','X') 
            and TRIM(DREFL2) = '' 
    ) ROUTES 
    GROUP BY 1,2,3,4 
    ORDER BY LR_NUM 
"""

sql_rth1_one = u"""
    SELECT 
        GPS_ID, 
        DATDOC, 
        LR_NUM, 
        GOS_NUM, 
        CAST(MIN(CAST(date_out AS SQL_CHAR) + ' ' + REPLACE(IIF(LENGTH(TRIM(time_out)) = 4, '0'+TRIM(time_out), TRIM(time_out)), '.', ':') + ':00') AS SQL_TIMESTAMP) DATE_OUT, 
        CAST(MIN(CAST(date_in AS SQL_CHAR) + ' ' + REPLACE(IIF(LENGTH(TRIM(time_in)) = 4, '0'+TRIM(time_in), TRIM(time_in)), '.', ':') + ':00') AS SQL_TIMESTAMP) DATE_IN	
    FROM( 
        select 
            RGNUM, 
            numdoc, 
            datdoc, 
            dattr1 as date_out,  
            cattr2 as time_out, 
            dattr2 as date_in, 
            cattr3 as time_in, 
            trim(debt) as lr_num, 
            ifnull(replace(d3name, ' ', ''),'') as gos_num, 
            ifnull(replace(r112.regnum, ' ', ''),'') as gos_num, 
            ifnull(cast(replace(r112.GSM_CARD, ' ', '') as sql_integer),0) as gps_id, 
            KODTCAR 
        from [..\\opdata\\dict.add].docs:mmyy 
        left join [..\\reflis\\dict.add].r112 on r112.kod = danal3 
        where kinddoc = 'RTH' and lvlnum = '1' 
            and krefl2 <> 'Д' 
            and (dattr1 is not null and dattr1 <= ':date' and dattr2 = ':date') 
            and cast(replace(r112.GSM_CARD, ' ', '') as sql_integer) <> 0 
            and UPPER(LEFT(TRIM(debt),1)) NOT IN ('','K','X') 
            and trim(debt) = ':lr_num'
    ) ROUTES 
    GROUP BY 1,2,3,4 
    ORDER BY LR_NUM 
"""

sql_rth1_update = u"""
UPDATE [..\\opdata\\dict.add].docs:mmyy
SET DREFL2 = 'Д'
WHERE 1 = 1
    AND KINDDOC = 'RTH' and LVLNUM = '1'
    AND DATDOC = ?
    AND TRIM(DEBT) = ?
"""