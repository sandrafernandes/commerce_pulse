import subprocess
from src.transformation.events_transformer import main as transform_run

def task_bootstrap():
    print("STEP 1 — BOOTSTRAP")
    subprocess.run(["python", "src/bootstrap_loader.py"])

def task_live_events():
    print("STEP 2 — LIVE EVENTS")
    subprocess.run(["python", "src/live_events_loader.py"])

def task_transform():
    print("STEP 3 — TRANSFORM")
    transform_run()

def pipeline():
    task_bootstrap()
    task_live_events()
    task_transform()

if __name__ == "__main__":
    pipeline()
