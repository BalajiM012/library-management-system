from apscheduler.schedulers.background import BackgroundScheduler
from src.features.automated_fine_calculation.api import calculate_fines_logic

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=calculate_fines_logic, trigger="interval", hours=24)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    import atexit
    atexit.register(lambda: scheduler.shutdown())
