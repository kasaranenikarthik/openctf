_logger = None


# simple logger based on werkzeug's
def _log(type, message, *args, **kwargs):
    global _logger
    if _logger is None:
        import logging
        _logger = logging.getLogger("openctf")
        if not logging.root.handlers:
            _logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            _logger.addHandler(handler)
    getattr(_logger, type)(message.rstrip(), *args, **kwargs)
