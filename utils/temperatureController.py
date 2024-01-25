class FuzzyLogicController:
    def __init__(self):
        pass

    def evaluate_rules(self, error, error_derivative):
        rules = [[0] * 3 for _ in range(3)]

        fuzzified_error_neg = self.fuzzify_error_neg(error)
        fuzzified_error_zero = self.fuzzify_error_zero(error)
        fuzzified_error_pos = self.fuzzify_error_pos(error)

        fuzzified_error_dot_neg = self.fuzzify_error_dot_neg(error_derivative)
        fuzzified_error_dot_zero = self.fuzzify_error_dot_zero(error_derivative)
        fuzzified_error_dot_pos = self.fuzzify_error_dot_pos(error_derivative)

        # RULES
        rules[0][0] = min(fuzzified_error_neg, fuzzified_error_dot_neg)
        rules[0][1] = min(fuzzified_error_zero, fuzzified_error_dot_neg)
        rules[0][2] = min(fuzzified_error_pos, fuzzified_error_dot_neg)
        
        rules[1][0] = min(fuzzified_error_neg, fuzzified_error_dot_zero)
        rules[1][1] = min(fuzzified_error_zero, fuzzified_error_dot_zero)
        rules[1][2] = min(fuzzified_error_pos, fuzzified_error_dot_zero)
        
        rules[2][0] = min(fuzzified_error_neg, fuzzified_error_dot_pos)
        rules[2][1] = min(fuzzified_error_zero, fuzzified_error_dot_pos)
        rules[2][2] = min(fuzzified_error_pos, fuzzified_error_dot_pos)

        return rules

    def fuzzify_error_pos(self, error):
        return self.trimf(error, [0, 5, 5])

    def fuzzify_error_zero(self, error):
        return self.trimf(error, [-5, 0, 5])

    def fuzzify_error_neg(self, error):
        return self.trimf(error, [-5, -5, 0])

    def fuzzify_error_dot_pos(self, error_dot):
        return self.trapmf(error_dot, [1, 1.5, 5, 5])

    def fuzzify_error_dot_zero(self, error_dot):
        return self.trimf(error_dot, [-2, 0, 2])

    def fuzzify_error_dot_neg(self, error_dot):
        return self.trapmf(error_dot, [-5, -5, -1.5, -1])

    def fuzzify_output_cooler(self):
        return self.get_trapmf_plots(0, 200, [0, 0, 30, 95], "left")

    def fuzzify_output_no_change(self):
        return self.get_trimf_plots(0, 200, [90, 100, 110])

    def fuzzify_output_heater(self):
        return self.get_trapmf_plots(0, 200, [105, 170, 200, 200], "right")

    def fis_aggregation(self, rules, pcc, pcnc, pch):
        result = [0] * 200

        for rule in range(len(rules)):
            for i in range(200):
                if rules[rule][0] > 0 and i < 95:
                    result[i] = min(rules[rule][0], pcc[i])
                if rules[rule][1] > 0 and 90 < i < 110:
                    result[i] = min(rules[rule][1], pcnc[i])
                if rules[rule][2] > 0 and 105 < i < 200:
                    result[i] = min(rules[rule][2], pch[i])

        return result

    def main(self):
        target_temp = float(input('Enter Target Temperature: '))
        current_temp = float(input('Enter Current Temperature: '))
        prev_temp = float(input('Enter Previous Temperature: '))

        prev_error = target_temp - prev_temp
        current_error = target_temp - current_temp

        error = current_error
        error_derivative = prev_error - current_error

        rules = self.evaluate_rules(error, error_derivative)
        aggregate_values = self.fis_aggregation(
            rules,
            self.fuzzify_output_cooler(),
            self.fuzzify_output_no_change(),
            self.fuzzify_output_heater()
        )

        centroid = self.get_centroid(aggregate_values)

        print(f"Error: {error}")
        print(f"Error Derivative: {error_derivative}")
        print(f"Centroid: {centroid}")
        print(f"Temperature: {int(centroid)}*C")

    def trimf(self, x, points):
        point_a, point_b, point_c = points
        slope_ab = self.get_slope(point_a, 0, point_b, 1)
        slope_bc = self.get_slope(point_b, 1, point_c, 0)
        result = 0

        if point_a <= x <= point_b:
            result = slope_ab * x + self.get_y_intercept(point_a, 0, point_b, 1)
        elif point_b <= x <= point_c:
            result = slope_bc * x + self.get_y_intercept(point_b, 1, point_c, 0)

        return result

    def trapmf(self, x, points):
        point_a, point_b, point_c, point_d = points
        slope_ab = self.get_slope(point_a, 0, point_b, 1)
        slope_cd = self.get_slope(point_c, 1, point_d, 0)
        y_intercept_ab = self.get_y_intercept(point_a, 0, point_b, 1)
        y_intercept_cd = self.get_y_intercept(point_c, 1, point_d, 0)
        result = 0

        if point_a < x < point_b:
            result = slope_ab * x + y_intercept_ab
        elif point_b <= x <= point_c:
            result = 1
        elif point_c < x < point_d:
            result = slope_cd * x + y_intercept_cd

        return result

    def get_slope(self, x1, y1, x2, y2):
        try:
            slope = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            slope = 0

        return slope

    def get_y_intercept(self, x1, y1, x2, y2):
        m = self.get_slope(x1, y1, x2, y2)

        if y1 < y2:
            y, x = y2, x2
        else:
            y, x = y1, x1

        return y - m * x

    def get_trimf_plots(self, start, end, points):
        plots = [0] * (abs(start) + abs(end))
        point_a, point_b, point_c = points
        slope_ab = self.get_slope(point_a, 0, point_b, 1)
        slope_bc = self.get_slope(point_b, 1, point_c, 0)
        y_intercept_ab = self.get_y_intercept(point_a, 0, point_b, 1)
        y_intercept_bc = self.get_y_intercept(point_b, 1, point_c, 0)

        for i in range(point_a, point_b):
            plots[i] = slope_ab * i + y_intercept_ab

        for i in range(point_b, point_c):
            plots[i] = slope_bc * i + y_intercept_bc

        return plots

    def get_trapmf_plots(self, start, end, points, shoulder=None):
        plots = [0] * (abs(start) + abs(end))
        point_a, point_b, point_c, point_d = points
        slope_ab = self.get_slope(point_a, 0, point_b, 1)
        slope_cd = self.get_slope(point_c, 1, point_d, 0)
        y_intercept_ab = self.get_y_intercept(point_a, 0, point_b, 1)
        y_intercept_cd = self.get_y_intercept(point_c, 1, point_d, 0)

        if shoulder == "left":
            for i in range(start, point_a):
                plots[i] = 1
        elif shoulder == "right":
            for i in range(point_d, end):
                plots[i] = 1

        for i in range(point_a, point_b):
            plots[i] = slope_ab * i + y_intercept_ab

        for i in range(point_b, point_c):
            plots[i] = 1

        for i in range(point_c, point_d):
            plots[i] = slope_cd * i + y_intercept_cd

        return plots

    def get_centroid(self, aggregated_plots):
        n = len(aggregated_plots)
        x_axis = list(range(n))
        centroid_num = 0
        centroid_denum = 0

        for i in range(n):
            centroid_num += x_axis[i] * aggregated_plots[i]
            centroid_denum += aggregated_plots[i]

        return centroid_num / centroid_denum


if __name__ == "__main__":
    fuzzy_logic_controller = FuzzyLogicController()
    fuzzy_logic_controller.main()