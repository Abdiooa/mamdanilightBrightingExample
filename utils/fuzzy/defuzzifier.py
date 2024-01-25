class Defuzzifier:
    def centroid(output_g: dict):
        '''
        Дефаззификация методом центроида.

        Дефаззификация
        Ее можно определить как процесс преобразования нечеткого множества в четкий набор
          или преобразования нечеткого элемента в четкий элемент.
        
        Параметры:
        - output_g (dict): Словарь, содержащий значения выходных нечетких множеств.

        Возвращает:
        - float: Значение центроида, вычисленное с использованием процесса дефаззификации.
        '''

        print("Дефаззификация")

        print(f"D: {output_g}")

        # Инициализация переменных для вычисления центроида
        centroid = 0
        numerator = 0
        denominator = 0

        # Итерирование по значениям принадлежности каждого нечеткого множества в выходных данных
        for x, mem_val in output_g.items():
            # Накопление числителя (взвешенная сумма x*значение_принадлежности)
            numerator += x * mem_val
            # Накопление знаменателя (сумма значений принадлежности)
            denominator += mem_val

        # Вычисление центроида по формуле: Центроид = (взвешенная сумма)/(сумма значений принадлежности)
        centroid = numerator / denominator

        # Возвращение вычисленного значения центроида
        return centroid
