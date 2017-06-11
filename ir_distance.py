import pigpio

TRANSLATIONS = [
    [68, 120], [69, 110], [71, 100], [73, 90], [75, 80],
    [78, 70], [81, 60], [88, 50], [95, 40],
    [108, 30], [135, 20], [190, 10], [230, 5]
]


class IRDistance:

    def __init__(self, pi, gpio_out, gpio_in):
        self.pi = pi

        pi.set_mode(gpio_out, pigpio.OUTPUT)
        pi.set_mode(gpio_in, pigpio.INPUT)

        self.script_id = pi.store_script(self._create_script(gpio_out, gpio_in))
        if self.script_id < 0:
            print 'could not store script: ', self.script_id

    @staticmethod
    def _create_script(gpio_out, gpio_in):
        o = str(gpio_out)
        i = str(gpio_in)
        script = 'TAG 000 '
        script += 'W ' + o + ' 0 MILS 70 '
        script += 'LD v0 8 '

        script += 'LD p4 p3 '
        script += 'LD p3 p2 '
        script += 'LD p2 p1 '
        script += 'LD p1 0 '
        script += 'TAG 999 '
        script += 'W ' + o + ' 1 MICS 100 W ' + o + ' 0 '
        script += 'R ' + i + ' '
        script += 'OR p1 '
        script += 'STA p1 '
        script += 'DCR v0 '
        script += 'JZ 888 '
        script += 'RL p1 1 '
        script += 'MICS 100 '
        script += 'JMP 999 '

        script += 'TAG 888 '
        script += 'W ' + o + ' 1 MILS 2 '
        script += 'LDA p1 '
        script += 'ADD p2 '
        script += 'ADD p3 '
        script += 'ADD p4 '
        script += 'RRA 2 '
        script += 'STA p0 '
        script += 'JMP 000'
        print script
        return script

    @staticmethod
    def _calc_distance(measure):
        if measure <= 0:
            return measure

        if measure <= TRANSLATIONS[0][0]:
            return float(TRANSLATIONS[0][1])

        for i in range(0, len(TRANSLATIONS)-1):
            if measure <= TRANSLATIONS[i+1][0]:
                return TRANSLATIONS[i][1] + \
                    float(measure - TRANSLATIONS[i][0]) / float(TRANSLATIONS[i][0] - TRANSLATIONS[i+1][0]) * \
                    float(TRANSLATIONS[i][1] - TRANSLATIONS[i+1][1])

        return float(TRANSLATIONS[len(TRANSLATIONS)-1][1])

    def get_measurement(self):
        status, params = self.pi.script_status(self.script_id)
        if status != 2:
            return -1
        return params[0]

    def get_distance(self):
        return IRDistance._calc_distance(self.get_measurement())

    def start(self):
        if self.script_id >= 0:
            self.pi.run_script(self.script_id)
            print 'started script', self.script_id

    def stop(self):
        if self.script_id >= 0:
            self.pi.delete_script(self.script_id)
