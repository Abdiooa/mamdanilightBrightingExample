from fuzzy.fuzzifier import fuzzification
from fuzzy.inference import inference
from dataclasses import dataclass

class LightingController_Mamdani:
    '''Mamdani'''
    ## # Определение класса результирующих данных для хранения выходной информации
    @dataclass
    class Result:
        output_graph: dict  # Словарь для хранения нечеткого графика выхода
        crisp_value_output: float  # Четкое значение, представляющее окончательный выход
        log_rules: dict  # Словарь для хранения примененных логических правил
        x1: float  # Значение входа, представляющее интенсивность окружающего света
        x2: float  # Значение входа, представляющее скорость изменения интенсивности окружающего света

        
        def __init__(self):
            self.output_graph = {}      # Инициализация пустого словаря для хранения нечеткого графика выхода
            self.crisp_value_output = 0.0  # Инициализация четкого значения выхода равным 0.0

    
    # Конструктор для инициализации объекта LightingController_Mamdani начальными значениями входных переменных
    def __init__ (self, x1: float, x2: float):
        self.x1 = x1  # Инициализация x1 интенсивностью окружающего света
        self.x2 = x2  # Инициализация x2 скоростью изменения интенсивности окружающего света
        self.result = self.Result()  # Инициализация объекта result для хранения выходных данных

    
    # Метод для установки новых значений входных переменных
    def set_input(self, new_x1: float, new_x2: float):
        self.x1 = new_x1  # Обновление x1 новой интенсивностью окружающего света
        self.x2 = new_x2  # Обновление x2 новой скоростью изменения интенсивности окружающего света

        
    # Метод для получения текущих значений входных переменных
    def get_input(self):
        return self.x1, self.x2  # Возвращение текущей интенсивности окружающего света и скорости изменения


    # Метод для получения четкого значения выхода
    def get_crisp_value_output(self):
        return self.result.crisp_value_output  # Возвращение окончательного четкого значения выхода

        
    # Метод для выполнения нечеткой логической системы
    def run(self):
        # Фаззификация значений входных переменных (преобразование их в нечеткие множества)
        self.fuzzificated_x1, self.fuzzificated_x2 = fuzzification(self.x1, self.x2)
        
        # Выполнение вывода с использованием нечетких правил
        self.result.crisp_value_output, self.result.output_graph, self.result.log_rules = inference(self.fuzzificated_x1, self.fuzzificated_x2)
        
        # Сохранение значений входных переменных в объекте result
        self.result.x1, self.result.x2 = self.get_input()
        
        # Возвращение объекта result
        return self.result

