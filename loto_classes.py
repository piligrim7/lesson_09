import random
from abc import abstractmethod

NUMBERS_COUNT = 90 #Количество номеров (бочонков)
LINE_CELLS_COUNT = 9 #Количество ячеек в одной полосе карточки
LINE_NUMBERS_COUNT = 5 #Количество чисел в одной полосе карточки
LINE_COUNT = 3 #Количесто строк в карточке

class NumGenerator:
    """Класс генерации случайных номеров в диапазоне от 1 до numbers_count+1
    """
    def __init__(self, numbers_count: int) -> None:
        self.numbers: list[int] = [i for i in range(1, numbers_count+1)]

    def get_next(self) -> int:
        """Получение очередного уникального номера

        Returns:
            int: номер
        """
        
        try:
            pos = random.randint(0, len(self.numbers)-1)
            result = self.numbers.pop(pos)
        except:
            result = 0
        return result

class Card:
    def __init__(self, player_name:str) -> None:
        self.name = player_name # Имя игрока
        self.lines: dict(int, list()) = dict()
        card_num_generator = NumGenerator(numbers_count=NUMBERS_COUNT)
        for n_line in range(LINE_COUNT):
            self.lines[n_line] = [0]*LINE_CELLS_COUNT
            line_num_generator = NumGenerator(numbers_count=LINE_CELLS_COUNT)
            line_numbers = []
            numbers_positions = []
            for _ in range(LINE_NUMBERS_COUNT):
                line_numbers.append(card_num_generator.get_next())
                numbers_positions.append(line_num_generator.get_next()-1)
            line_numbers=sorted(line_numbers)
            numbers_positions = sorted(numbers_positions)
            for i in range(LINE_NUMBERS_COUNT):
                self.lines[n_line][numbers_positions[i]] = line_numbers[i]
        self.cross_number_count = 0
        self.is_full = False #Флаг закрытия всех цифр на карточке

    def check_number(self, number: int) -> bool:
        for line in self.lines.values() :
            if number in line:
                return True
        return False

    def cross_number(self, number: int) -> bool:
        for line in self.lines.values():
            for i in range(len(line)):
                if line[i] == number:
                    line[i] = -1
                    self.cross_number_count+=1
                    if self.cross_number_count == LINE_NUMBERS_COUNT * LINE_COUNT:
                        self.is_full = True
                    return True
        else:
            return False

    def get_text(self) -> str:
        """Функция представления содержимого карточки в виде текста

        Returns:
            str: строка вывода
        """
        sep = ' '
        space = '  '
        cross = ' -'
        result = ''
        for _, line in self.lines.items(): 
            s_sep = ''
            for num in line:
                s_num = str(num)
                if len(s_num)==1:
                    s_num=' ' + s_num
                result += s_sep + (s_num if num > 0 else space if num == 0 else cross)
                s_sep = sep
            result+='\n'
        name = 'Карточка игрока ' + self.name
        name_len = len(name)
        width = 3 * LINE_CELLS_COUNT - 1
        if name_len < width:
            name = '-' * ((width-name_len)//2) + name
            name += '-' * (width - len(name))
        return name + '\n' + result + '-' * width

class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.card = Card(player_name=name)
        self.is_lost = False #Флаг проигрыша и выбытия из игры

    @abstractmethod
    def make_move(self, current_number: int):
        pass

class Computer(Player):
    def make_move(self, current_number: int):
        self.card.cross_number(number=current_number)

class Human(Player):
    def make_move(self, current_number: int):
        if self.get_choice():
            result = self.card.cross_number(number=current_number)
        else:
            result = not self.card.check_number(number=current_number)
        if not result:
            self.is_lost = True

    def get_choice(self)->bool:
        return input(f'{self.name}, ваш ход: зачеркнуть цифру? (y/n): ') == 'y'

class Game:
    def __init__(self) -> None:
        while True:
            try:
                players_count = int(self.get_players_count())
                if players_count>1:
                    break
            except:
                pass
            print('Количество игроков введено некорректно!')
        self.players = list()
        comp_num = 0
        for i in range(players_count):
            while True:
                try:
                    player_type = self.get_player_type()
                    if player_type == 'h':
                        name = self.get_human_name()
                        self.players.append(Human(name=name))
                        break
                    elif player_type == 'c':
                        comp_num+=1
                        name = f'Comp-{comp_num}'
                        self.players.append(Computer(name=name))
                        break
                except:
                    pass
                print('Тип игрока введен некорректно!')

    def get_players_count(self)->str:
        return input('Введите количество игроков >1: ')

    def get_player_type(self)->str:
        return input(f'Введите тип игрока №{i+1} человек или computer (h/c): ')

    def get_human_name(self)->str:
        return input(f'Введите имя игрока №{i+1}: ')

    def begin(self):
        bag = NumGenerator(numbers_count=NUMBERS_COUNT) #Мешок с бочонками лото
        while True:
            current_number = bag.get_next()
            if current_number == 0:
                print('Все номера разыграны!')
                return None
            print(f'\nНовый бочонок: {current_number} (осталось {len(bag.numbers)})')
            for player in self.players:
                assert isinstance(player, Player)
                print(player.card.get_text())
            for player in self.players:
                assert isinstance(player, Player)
                if not player.is_lost:
                    player.make_move(current_number=current_number)
                    if player.is_lost:
                        self.players.remove(player)
                        if len(self.players) == 1:
                            player = self.players[0]
                            print(f'Игрок {player.name} выиграл!')
                            return player
                        else:
                            print(f'Игрок {player.name} проиграл!')
                    elif player.card.is_full:
                        print(f'Игрок {player.name} выиграл!')
                        return player