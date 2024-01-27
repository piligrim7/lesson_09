from __future__ import annotations

# Количество знаков после запятой для округления координат
ROUND_DIGITS_COUNT = 6

# Количество знаков после запятой для округления координат для print()
PRINT_ROUND_DIGITS_COUNT = 6

class Point:
    """Точка с координатами
    """
    
    # Количество знаков после запятой для округления координат при сравнении
    COMPARE_ROUND_DIGITS_COUNT = 8
    
    def __init__(self, x:float, y:float):
        """Функция инициализации объекта

        Args:
            x (float): Координата x
            y (float): Координата y
        """
        
        self.x: float = x
        self.y: float = y
        self.xi: int = int(round(x, 0))
        self.yi: int = int(round(y, 0))
        # Внутненний флаг, определяющий является ли текущий экземпляр нормализованным
        self._is_normalized: bool = 0 < self.x < 1 and 0 < self.y < 1

    def __str__(self):
        """Функция вывода данных экземпляра класса для print()
        """

        return f'x: {round(self.x, PRINT_ROUND_DIGITS_COUNT)}, y: {round(self.y, PRINT_ROUND_DIGITS_COUNT)}'


    def get_JSON(self)->str:        
        """Функция получения JSON

        Returns:
            str: Строка данных текущего экземпляра класса в формате JSON
        """
        
        return {
            'x': round(self.x, ROUND_DIGITS_COUNT),
            'y': round(self.y, ROUND_DIGITS_COUNT)
            }

    def get_normalized(self,
                      dx: float = 0.0, dy: float = 0.0,
                      div_x: float = 1.0, div_y: float = 1.0)->Point:
        
        """Функция получения Point в относительных координатах

        Args:
            dx (float, optional): Смещение по x. Defaults to 0.0.
            dy (float, optional): Смещение по y. Defaults to 0.0.
            div_x (float, optional): Делитель для x. Defaults to 1.0.
            div_y (float, optional): Делитель для y. Defaults to 1.0.

        Returns:
            Point: Нормированный Point
        """

        # Вызов ошибки, если текущий экземпляр Point уже нормализован
        if self._is_normalized:
            raise Exception('Нормализация уже нормализованного экземпляра Point!')

        return Point(x=(self.x-dx)/div_x,
                     y=(self.y-dy)/div_y
                     )

#____________________________________________________________________
class BoundingBox:
    """Класс ограничивающего объект прямоугольника
    """
    def __init__(self,
                left: float = 0.0,
                top: float = 0.0,
                right: float = 0.0,
                bottom: float = 0.0):
        """Функция инициализации объекта

        Args:
            left (float, optional): левая координата x. Defaults to 0.0.
            top (float, optional): верхняя координата y. Defaults to 0.0.
            right (float, optional): правая координата x. Defaults to 0.0.
            bottom (float, optional): нижняя координата y. Defaults to 0.0.
            is_normalized (ool, optional): флаг является ли
        """
        self.left: float = left
        self.top: float = top
        self.right: float = right
        self.bottom: float = bottom
        self.height: float = abs(self.bottom-self.top)
        self.width: float = abs(self.right-self.left)
        self.center: Point = Point((self.left+self.right)/2,
                                (self.top+self.bottom)/2)
        # Внутненний флаг, определяющий является ли текущий экземпляр нормализованным
        self._is_normalized: bool = self.center._is_normalized
        
    def __str__(self):
        """Функция вывода данных экземпляра класса для print()
        """

        return f' left: {round(self.left, PRINT_ROUND_DIGITS_COUNT)},'\
            f' top: {round(self.top, PRINT_ROUND_DIGITS_COUNT)},'\
            f' right: {round(self.right, PRINT_ROUND_DIGITS_COUNT)},'\
            f' bottom: {round(self.bottom, PRINT_ROUND_DIGITS_COUNT)},'\
            f' width: {round(self.width, PRINT_ROUND_DIGITS_COUNT)},'\
            f' height: {round(self.height, PRINT_ROUND_DIGITS_COUNT)}'

    def get_JSON(self)->str:
        """Функция получения JSON

        Returns:
            str: Строка данных текущего экземпляра класса в формате JSON
        """
        
        return {
            'left': round(self.left, ROUND_DIGITS_COUNT),
            'top': round(self.top, ROUND_DIGITS_COUNT),
            'right': round(self.right, ROUND_DIGITS_COUNT),
            'bottom': round(self.bottom, ROUND_DIGITS_COUNT)
            }

    def get_normalized(self,
                      dx: float = 0.0, dy: float = 0.0,
                      div_x: float = 1.0, div_y: float = 1.0)->BoundingBox:
        """Функция получения BoundingBox в относительных координатах

        Args:
            dx (float, optional): Смещение по x. Defaults to 0.0.
            dy (float, optional): Смещение по y. Defaults to 0.0.
            div_x (float, optional): Делитель для x. Defaults to 1.0.
            div_y (float, optional): Делитель для y. Defaults to 1.0.

        Returns:
            BoundingBox: Нормированный BoundingBox
        """

        # Вызов ошибки, если текущий экземпляр BoundingBox уже нормализован
        if self._is_normalized:
            raise Exception('Нормализация уже нормализованного экземпляра BoundingBox!')

        left = (self.left-dx)/div_x
        top = (self.top-dy)/div_y
        right = (self.right-dx)/div_x
        bottom = (self.bottom-dy)/div_y
        return BoundingBox(left=left,
                           top=top,
                           right=right,
                           bottom=bottom)

#____________________________________________________________________
class TextBox:
    """Класс строки для хранения текста с bbox
    """

    def __init__(self, text: str, bbox: BoundingBox):
        self.text: str = text
        self.bbox: BoundingBox = bbox
        # Внутненний флаг, определяющий является ли текущий экземпляр нормализованным
        self._is_normalized: bool = self.bbox._is_normalized
        
    def get_JSON(self)->str:    
        """Функция получения JSON

        Returns:
            str: Строка данных текущего экземпляра класса в формате JSON
        """
        
        return {
            'number': self.text,
            'bbox': self.bbox.get_JSON()
            }

    def get_normalized(self,
                      dx: float = 0.0, dy: float = 0.0,
                      div_x: float = 1.0, div_y: float = 1.0)->TextBox:
        """Функция получения TextBox в относительных координатах

        Args:
            dx (float, optional): Смещение по x. Defaults to 0.0.
            dy (float, optional): Смещение по y. Defaults to 0.0.
            div_x (float, optional): Делитель для x. Defaults to 1.0.
            div_y (float, optional): Делитель для y. Defaults to 1.0.

        Returns:
            TextBox: Экземпляр TextBox с нормированным BoundingBox
        """

        return TextBox(text=self.text,
                       bbox=self.bbox.get_normalized(dx=dx, dy=dy,
                                                     div_x=div_x, div_y=div_y
                                                     )
                       )
#____________________________________________________________________