import re
import curses
import time

class fake_system():

    available_commands = ['store', 'load', 'add', 'addi', 'sub', 'subi',
                    'mul', 'muli', 'div', 'divi', 'jump', 'jpos', 'jzero']

    def __init__(self, comment='//'):
        self._register = 0
        self._memory = [0]*100
        self._commands = []
        self._pointer = 0
        self._comment_tag = comment

    def load(self, x:int):
        self._register = self._memory[x]

    def store(self, x:int):
        self._memory[x] = self._register

    def add(self, x:int):
        self.addi(self._memory[x])

    def sub(self, x:int):
        self.subi(self._memory[x])

    def mul(self, x:int):
        self.muli(self._memory[x])

    def div(self, x:int):
        self.divi(self._memory[x])

    def addi(self, x:int):
        self._register += x

    def subi(self, x:int):
        self._register -= x

    def muli(self, x:int):
        self._register *= x

    def divi(self, x:int):
        self._register /= x

    def jpos(self, x:int):
        if self._register > 0:
            self._pointer = x-1

    def jzero(self, x:int):
        if not self._register:
            self._pointer = x-1

    def jump(self, x:int):
        self._pointer = x-1

    def run(self):
        while self._pointer < len(self._commands):
            command, value = self._commands[self._pointer]
            curses.wrapper(self.show_progress)

            getattr(self, command)(int(value))

            self._pointer += 1

    def show_progress(self, stdsrc):
        stdsrc.clear()
        command, value = self._commands[self._pointer]
        curses.noecho()
        # curses.curs_set(0)

        for index, cell in enumerate(self._memory):
            memorycell = '|{:^12}|'.format(cell)
            x, y = 45+((index//25)*15), (index%25)+3
            stdsrc.addstr(y,x,memorycell)
        
        stdsrc.addstr(3+self._pointer, 115, '==>')
        for index, comm in enumerate(self._commands):
            str_command, str_value = comm
            curses.curs_set(0)
            comma = '|{:^12}|'.format(str_command) + '|{:^12}|'.format(str_value)
            x, y = 120+((index//30)*13), (index%25)+3
            stdsrc.addstr(y,x,comma)
        stdsrc.addstr(4, 1, 'PC:       {:>15}'.format(self._pointer))
        stdsrc.addstr(5, 1, 'COMMAND:  {:>15}'.format(command) + '{:>8}'.format(value))
        # stdsrc.addstr(6, 1, 'MEM_VALUE:{:>15}'.format(str(self._memory[1:4]))) 
        stdsrc.addstr(7, 1, 'REGISTER: {:>15}'.format(self._register))
        stdsrc.refresh()
        # time.sleep(.5)
        stdsrc.getch()

    def compile(self, text):
        any_string_after_comment_tag = f'{self._comment_tag}.*?\n'
        
        text = text.lower()
        commands_text = re.sub(any_string_after_comment_tag, ' ', text)
        commands_text = commands_text.replace('\n', ' ')
        commands_list = commands_text.split()

        for index, command_line in enumerate(commands_list):
            if command_line in self.available_commands:
                self._commands.append((command_line,commands_list[index+1]))
