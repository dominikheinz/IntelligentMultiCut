class SmoothController:

    __smoothing_factor = 8


    def __init__(self, x_values, y_values):
        self.__x_arr = x_values
        self.__y_arr = y_values


    def smooth(self):
        z = []
        for i in range(0, len(self.__x_arr)):
            num = 0
            temp = []
            for j in range(i - self.__smoothing_factor, i + self.__smoothing_factor):
                if 0 <= j < len(self.__x_arr):
                    temp.append(self.__y_arr[j])
                    num += 1
            temp.sort()
            z.append(temp[int(len(temp) / 2)])
        return z


