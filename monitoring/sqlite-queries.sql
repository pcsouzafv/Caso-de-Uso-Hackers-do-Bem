-- 1. Monitorar crescimento do banco de dados
SELECT
    name as table_name,
    CAST(SUM(pgsize) as REAL) / 1024 / 1024 as size_mb
FROM sqlite_dbpage
GROUP BY name
ORDER BY size_mb DESC;

-- 2. Verificar número de registros por tabela
SELECT
    name as table_name,
    COUNT(*) as row_count
FROM sqlite_master
WHERE type = 'table'
GROUP BY name
ORDER BY row_count DESC;

-- 3. Verificar espaço ocupado por índices
SELECT
    name as table_name,
    CAST(SUM(pgsize) as REAL) / 1024 / 1024 as index_size_mb
FROM sqlite_dbpage
WHERE name LIKE '%_idx'
GROUP BY name
ORDER BY index_size_mb DESC;

-- 4. Verificar número de conexões ativas
SELECT
    COUNT(*) as active_connections
FROM sqlite_master
WHERE type = 'table';

-- 5. Verificar tabelas sem índices
SELECT
    name as table_name
FROM sqlite_master
WHERE type = 'table'
AND name NOT IN (
    SELECT DISTINCT tbl_name
    FROM sqlite_master
    WHERE type = 'index'
)
ORDER BY name;

-- 6. Verificar queries lentas (se tiver logging habilitado)
SELECT
    query,
    COUNT(*) as count,
    AVG(elapsed_time) as avg_time,
    MAX(elapsed_time) as max_time
FROM slow_queries
GROUP BY query
ORDER BY avg_time DESC
LIMIT 10;

-- 7. Verificar tamanho de cada coluna
SELECT
    name as table_name,
    CAST(SUM(pgsize) as REAL) / 1024 / 1024 as column_size_mb
FROM sqlite_dbpage
WHERE name IN (
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
)
GROUP BY name
ORDER BY column_size_mb DESC;

-- 8. Verificar fragmentação do banco
SELECT
    CAST(SUM(pgsize) as REAL) / 1024 / 1024 as total_size_mb,
    COUNT(DISTINCT pgno) as page_count,
    CAST(COUNT(DISTINCT pgno) as REAL) / (SELECT COUNT(*) FROM sqlite_dbpage) as fragmentation
FROM sqlite_dbpage;

-- 9. Verificar tabelas com mais locks
SELECT
    name as table_name,
    COUNT(*) as lock_count
FROM sqlite_master
WHERE type = 'table'
GROUP BY name
ORDER BY lock_count DESC;

-- 10. Verificar queries mais comuns
SELECT
    query,
    COUNT(*) as count
FROM query_log
GROUP BY query
ORDER BY count DESC
LIMIT 10;
