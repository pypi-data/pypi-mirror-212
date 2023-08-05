class ToolsError():

    class LoadBodyError(Exception):
        def __init__(self, message: str = 'Failed to load json from request body.'):
            self.message = message

        def __str__(self):
            return self.message
