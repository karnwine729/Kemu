from Kemu_Engine import Engine

class JetEngine(Engine):
    def __init__(self, filePath, lines):
        super().__init__(filePath, lines)
        self.velCurve = []
        self.atmCurve = []
