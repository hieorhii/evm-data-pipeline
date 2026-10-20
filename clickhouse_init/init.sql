CREATE DATABASE IF NOT EXISTS web3_dwh;

CREATE TABLE IF NOT EXISTS web3_dwh.stg_usdt_transfers (
    blockNumber UInt64,
    timeStamp DateTime,
    hash String,
    from_address String,
    to_address String,
    value Float64,
    gasUsed UInt64
) ENGINE = MergeTree()
ORDER BY (timeStamp, hash)
PARTITION BY toYYYYMM(timeStamp);