import psutil

def check_system_health():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        return {
            "status": "healthy" if cpu_usage < 80 and memory_usage < 80 else "unhealthy",
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        }
    except Exception as e:
        return {"status": "unhealthy", "cpu_usage": None, "memory_usage": None}
