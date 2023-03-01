from util import Submarine


class ALU(Submarine):
    """A fun ALU emulator, impractical for the actual search."""

    def _parseLine(self, line: str):
        sline = line.split()
        if len(sline) == 3:
            if sline[-1] not in 'wxyz':
                sline[-1] = int(sline[-1])
        else:
            sline.append(None)
        return sline

    def __init__(self) -> None:
        self.reg = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        self.monad = self.getInput()

    def add(self, fst: str, snd: int):
        self.reg[fst] += snd

    def mul(self, fst: str, snd: int):
        self.reg[fst] *= snd

    def div(self, fst: str, snd: int):
        fstnum = self.reg[fst]
        if fstnum >= 0:
            result = fstnum // snd
        else:
            result = (-fstnum) // snd * (-1)
        self.reg[fst] = result

    def mod(self, fst: str, snd: int):
        self.reg[fst] %= snd

    def eql(self, fst: str, snd: int):
        self.reg[fst] = int(self.reg[fst] == snd)

    def run(self, modelno: str):
        assert len(modelno) == 14, 'Invalid model number'
        self.modelno = modelno
        self.reader = 0

        self.reg = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        for op, fst, snd in self.monad:
            if op == 'inp':
                self.reg[fst] = int(self.modelno[self.reader])
                self.reader += 1
            else:
                if isinstance(snd, str):
                    snd = self.reg[snd]
                opfunc = getattr(self, op)
                opfunc(fst, snd)
        z = self.reg['z']
        print(f'Model No. {modelno}, z = {z}')


class SmartALU(Submarine):

    def _parseLine(self, line: str):
        return ALU()._parseLine(line)

    def __init__(self) -> None:
        """MONAD contains 14 chunks of nearly identical instructions:

        inp w
        mul x 0
        add x z
        mod x 26
        div z [divz]  divz = 1 or 26
        add x [a1]    a1 >= 10 <=> divz = 1
        eql x w
        eql x 0
        mul y 0
        add y 25
        mul y x
        add y 1
        mul z y
        mul y 0
        add y w
        add y [a2]
        mul y x
        add z y

        the tuple (divz, a1, a2) is stored in self.smonad.
        """
        monad = self.getInput()
        self.smonad = [(monad[i+4][2], monad[i+5][2], monad[i+15][2])
                       for i in range(0, len(monad), 18)]
        self.cache = [('', 0)]
        self.validnos = []

    def runChunk(self, w, z, smo):
        """Run one chunk of smonad.

        Args:
            w: digit 1-9, input at start of chunk.
            z: z value at the start of chunk.
            smo: (divz, a1, a2)

        Returns:
            z value after the chunk is executed, or None.

        Note that z at the end is only determined by w and z
        and independent of x or y.
        Furthermore, when divz == 1, log_26(z) must increase by 1;
        when divz == 26, log_26(z) decreases by 1 if (z % 26 + a1 == w)
        and stays the same otherwise.
        In the 14 chunks of monad, 7 divz's is 1 and the other 7 is 26,
        which means if z is 0 after all 14 chunks, log_26(z) must decrease
        whenever divz == 26. When this is not satified, return None.
        """

        divz, a1, a2 = smo
        if divz == 1:
            return z * 26 + (w + a2)
        else:
            if z % 26 + a1 == w:
                return z // 26
            else:
                return None

    def searchValidNo(self):
        while self.cache:
            ws, z = self.cache.pop()
            if len(ws) == 14:
                if z == 0:
                    self.validnos.append(ws)
                continue
            for w in range(1, 10):
                newz = self.runChunk(w, z, self.smonad[len(ws)])
                if newz is not None:
                    newws = ws + str(w)
                    self.cache.append((newws, newz))
        print(f'{len(self.validnos)} valid model numbers found.')
        maxno = max(self.validnos)
        minno = min(self.validnos)
        return maxno, minno


if __name__ == '__main__':
    submarine = SmartALU()
    maxno, minno = submarine.searchValidNo()

    alu = ALU()
    alu.run(maxno)
    alu.run(minno)
