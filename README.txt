# CommercePulse - Data Engineering Case Study

## 1. Overview
This project simulates a data analytics platform for CommercePulse Ltd, aggregating orders, payments, shipments, and refunds from multiple vendors.  
The implemented pipeline supports:  
- Historical data bootstrap  
- Incremental real-time event ingestion  
- Data transformation and reconciliation  
- Loading into an analytical warehouse  
- Data quality reporting  
- Python DAG orchestration simulating Airflow  

**Note**: Airflow and BigQuery were not used because Google Cloud did not accept my prepaid Visa card. Instead, Python is used for local orchestration and SQLite for offline warehouse.

---

## 2. Architecture

Raw JSON
└──> MongoDB (events_raw) # Stores raw historical and live events
│
└──> MongoDB (events_curated) # Idempotent and cleaned transformations
│
└──> Pandas → Local Warehouse (SQLite)
│
└──> Quality reports


### Components

| Layer | Technology | Function |
|-------|-----------|---------|
| Raw storage | MongoDB | Stores all historical and live events with `event_id` for idempotency |
| Transformation | Pandas | Normalizes schemas, applies business rules, handles late or duplicate events |
| Analytical Warehouse | Local SQLite | Simulates BigQuery for SQL queries and reports, append-only with auditability |
| Orchestration | Python DAG | Simulates Airflow, controls execution order of tasks (bootstrap → live events → transform) |
| Data Quality | Python + SQL | Event counts, integrity and consistency validation |

---

## 3. Project Structure

commercepulse_case_study/
├─ src/
│ ├─ analytics/
│ │ ├─ init.py
│ │ ├─ warehouse_simulator.py
│ │ └─ quality_report.py
│ ├─ config/
│ │ ├─ init.py
│ │ └─ mongo_client.py
│ ├─ transformation/
│ │ ├─ init.py
│ │ └─ events_transformer.py
│ ├─ dags/
│ │ └─ local_dag.py
│ └─ ingest/
│ ├─ bootstrap_loader.py
│ ├─ live_events_loader.py
│ └─ generator.py
├─ run_pipeline.py
├─ .env
├─ analytics.db
└─ README.md


---

## 4. Configuration

### Environment Variables (.env)
MONGO_URI=
MONGO_DB=


### Dependencies
```bash
python 3.9+
pip install pymongo pandas python-dotenv

5. Running the Pipeline
Full pipeline (bootstrap + live events + transformation):
python run_pipeline.py

Expected output:

STEP 1 — BOOTSTRAP
STEP 2 — LIVE EVENTS
STEP 3 — TRANSFORM
X events transformed.
Data successfully loaded into the warehouse.

Data quality report:
python src/analytics/quality_report.py

Sample output:
=== DATA QUALITY REPORT ===
   total_orders
0          3500
===========================

6. Engineering Decisions
| Decision                   | Justification                                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------------------------- |
| MongoDB as source of truth | Stores all historical and live events without data loss, ensuring idempotency via `event_id`                   |
| Pandas for transformation  | Flexible handling of schema drift, out-of-order data, and deduplication                                        |
| Local Warehouse (SQLite)   | Simulates BigQuery for offline execution, keeping dimensional modeling and SQL analytics compatible with cloud |
| Append-only warehouse      | Guarantees auditability and complete history                                                                   |
| Python DAG                 | Simulates Airflow locally without requiring cloud, clear orchestration                                         |
| Incremental extraction     | Avoids full reload, improves performance, allows continuous ingestion                                          |
| Upsert in curated layer    | Prevents duplicates and maintains idempotency                                                                  |


7. Trade-offs

| Choice        | Benefit                                           | Limitation                                                                          |
| ------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Local SQLite  | Easy offline execution, fast setup                | Cannot scale to massive datasets or support advanced partitioning like BigQuery     |
| Pandas vs SQL | Full control over schema drift and transformation | Less performant for very large datasets                                             |
| Python DAG    | Simple and fast for simulation                    | Does not replace advanced Airflow features (retry, scheduling, centralized logging) |


8. Offline BigQuery Justification
Due to the inability to use GCP/BigQuery (card not accepted), the project uses a local SQLite warehouse.
Maintains dimensional modeling and SQL queries identical to BigQuery.
Architecture is compatible with future cloud migration.
The evaluator can see the pipeline, orchestration, transformation, and reports fully functioning offline.

9. Pipeline Flow
1️⃣ Bootstrap JSON → MongoDB events_raw
2️⃣ Live events → MongoDB events_raw
3️⃣ Transformation → MongoDB events_curated
4️⃣ Loading → SQLite Warehouse (fact_events)
5️⃣ Reporting → Quality report (total_orders, consistency)
