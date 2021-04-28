import re
import curses
import time

class system_viewer():

    def show_list(self, stdsrc, iterable, axis_y=1, column_size=25, axis_x=1, commands=False): 
        x = y = 0
        max_y, max_x = stdsrc.getmaxyx()
        spare_y = max_y - axis_y
        spare_x = max_x - axis_x

        rows = spare_x//len(iterable[0])
        columns = spare_y - 1

        spare_cells = rows*columns

        if commands:
            section_begin = (self._pointer//spare_cells)*spare_cells
            section_end = section_begin+spare_cells
            iterable = iterable[section_begin:section_end:]
            # stdsrc.addstr(max_y-1, max_x-50, f"begin {section_begin}, end {section_end}, p {self._pointer}")

        for index, string in enumerate(iterable):
            relative_column_position = (index//columns)*len(string)
            relative_row_position = (index%columns)
            y = axis_y+relative_row_position
            x = axis_x+relative_column_position
            stdsrc.addstr(y,x,string)
            if commands and section_begin+index == self._pointer:
                stdsrc.addstr(y,x,string, curses.A_STANDOUT)

        return x+len(iterable[0]), y


class fake_system(system_viewer):

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
            self._pointer = x-2

    def jzero(self, x:int):
        if not self._register:
            self._pointer = x-2

    def jump(self, x:int):
        self._pointer = x-2

    def run(self):
        while self._pointer < len(self._commands):
            command, value = self._commands[self._pointer]
            curses.wrapper(self.show_progress)

            getattr(self, command)(int(value))

            self._pointer += 1

    def show_progress(self, stdsrc):
        stdsrc.clear()
        curses.noecho()

        memorycell = []
        comma = []

        for index, cell in enumerate(self._memory[1::]):
            memorycell.append('{:<4}[{:^6}] '.format(index+1, cell))

        for index, comm in enumerate(self._commands):
            str_command, str_value = comm
            comma.append('{:<4}|{:<7} {:>7}| '.format(index+1, str_command, str_value))

        try:
            x, _ = self.show_list(stdsrc, memorycell, axis_y=5,axis_x=1, column_size=33)
            self.show_list(stdsrc, comma, axis_y=3, axis_x=x, column_size=36, commands=True)

            self.show_program_status(stdsrc)
        except curses.error as e:
            x, y = stdsrc.getmaxyx()
            y = (y//2)-27 if (y//2)-27 > 0 else 0

            stdsrc.clear()
            stdsrc.addstr(x//2, y, 'This window is too tight. Please open up your Terminal')
        except ZeroDivisionError:
            x, y = stdsrc.getmaxyx()
            y = (y//2)-27 if (y//2)-27 > 0 else 0

            stdsrc.clear()
            stdsrc.addstr(x//2, y, 'There\'s no space for any cell')


        stdsrc.refresh()
        while stdsrc.getch() != 10: pass

    def show_program_status(self, stdsrc, axis_y=1, axis_x=1):
        command, value = self._commands[self._pointer]

        stdsrc.addstr(axis_y, axis_x, 'PC:       {:>15}'.format(self._pointer))
        stdsrc.addstr(axis_y+1, axis_x, 'COMMAND:  {:>15}{:>8}'.format(command, value))
        # stdsrc.addstr(axis_y+1, axis_x, 'MEM_VALUE:{:>15}'.format(str(self._memory[1:4]))) 
        stdsrc.addstr(axis_y+3, axis_x, 'REGISTER: {:>15}'.format(self._register))

    def compile(self, text):
        any_string_after_comment_tag = f'{self._comment_tag}.*?\n'
        
        text = text.lower()
        commands_text = re.sub(any_string_after_comment_tag, ' ', text)
        commands_text = commands_text.replace('\n', ' ')
        commands_list = commands_text.split()

        for index, command in enumerate(commands_list):
            if command in self.available_commands:
                try:
                    value = int(commands_list[index+1])
                    self._commands.append((command,value))
                except ValueError:
                    traceback = -5 if len(self._commands) > 5 else 0
                    for index, previous_lines in enumerate(self._commands[traceback::]):
                        print(f'{len(self._commands)-4+index}{previous_lines}')
                    print(f'Error on line {len(self._commands)+1}, value isn\'t right')
                    exit()
                

