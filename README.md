# EVM Data Pipeline

## О проекте
Автоматизированный ELT-пайплайн для сбора, хранения и трансформации данных сети Ethereum. Проект демонстрирует проектирование современного хранилища данных (Data Lake -> DWH -> Data Mart).

## Архитектура и Стек
* **Extract (API):** Python (`requests`) — выгрузка сырых данных транзакций через Etherscan API.
* **Data Lake (Load):** MongoDB — хранение неструктурированных сырых JSON-ответов (NoSQL).
* **DWH (Load):** ClickHouse — колоночная аналитическая база. Использован движок `MergeTree`, индексы сортировки и партиционирование по месяцам (`toYYYYMM`).
* **Transform:** dbt Core (`dbt-clickhouse`) — построение витрин данных (Data Marts) с применением CTE и оконных функций (`lagInFrame`, `OVER`).
* **Orchestration:** Apache Airflow — управление зависимостями задач (DAG) и запуск по расписанию (`@daily`).
* **Infrastructure:** Docker Compose.

## Структура репозитория
* `/scripts` — Python-модули для ETL (Extract & Load).
* `/clickhouse_init` — скрипт инициализации DWH.
* `/dbt_web3` — dbt-проект (модели трансформации и конфиги).
* `/dags` — DAG-файл оркестратора Airflow.

## Быстрый запуск
1. Клонируйте репозиторий.
2. В файле `scripts/extract.py` укажите ваш `API_KEY` от Etherscan.
3. Запустите инфраструктуру:
   ```bash
   docker-compose up -d --build