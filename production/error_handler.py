from production.logger import get_logger

logger = get_logger("error_handler")

def safe_execute(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in {fn.__name__}: {e}", exc_info=True)
        return None
