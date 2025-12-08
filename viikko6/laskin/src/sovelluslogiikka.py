class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo
        self._steps = []

    def miinus(self, operandi):
        self._arvo = self._arvo - operandi
        self._steps.append(-operandi)

    def plus(self, operandi):
        self._arvo = self._arvo + operandi
        self._steps.append(operandi)

    def nollaa(self):
        self._arvo = 0

    def aseta_arvo(self, arvo):
        self._arvo = arvo

    def kumoa(self):
        if self._steps:
            viimeisin = self._steps.pop()
            self._arvo -= viimeisin

    def arvo(self):
        return self._arvo
