import time
import psutil

def get_metrics(start_time):
    elapsed = time.time() - start_time
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    return elapsed, cpu, mem, time