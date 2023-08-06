from typing import Tuple

from pymodbus.client.serial import ModbusSerialClient as ModbusClient


class MecanumWheelMotor:
    def __init__(
        self,
        client: ModbusClient,
        address: int,
        direction_address: int,
        speed_address: int,
        inverse: bool = False,
    ):
        self.address = address  # Адрес модуля мотора
        self.direction_address = direction_address  # Адрес регистра для установки направления движения
        self.speed_address = speed_address  # Адрес регистра для установки скорости движения
        self.speed = 0  # Текущая установленная скорость
        self.direction = 0  # Текущее установленное направление
        self.client = client  # Клиент Modbus
        self.inverse = inverse  # Флаг инверсии направления движения

    def set_speed(self, speed: float) -> None:
        self.set_direction(speed >= 0)  # Установка направления движения в зависимости от знака скорости
        speed_value = self.calculate_speed_value(speed)  # Вычисление значения скорости
        self.handle_initial_speed_condition(speed_value)  # Обработка начального условия скорости
        self.write_speed_registers(speed_value)  # Запись значения скорости в регистр

    def calculate_speed_value(self, speed: float) -> int:
        if abs(speed) > 0:
            return int(524 + abs(speed) * 499)  # Вычисление значения скорости в соответствии с диапазоном
        return 0  # Если скорость меньше 0.1, то установка значения скорости в 0

    def handle_initial_speed_condition(self, speed_value: int) -> None:
        if self.speed == 0 and speed_value != 0:
            self.client.write_registers(self.speed_address, 1023, self.address)  # Запись значения инициализации скорости

    def write_speed_registers(self, speed_value: int) -> None:
        self.client.write_registers(self.speed_address, speed_value, self.address)  # Запись значения скорости в регистр
        self.speed = speed_value  # Обновление текущей установленной скорости

    def set_direction(self, direction: bool) -> None:
        if self.inverse:
            direction = not direction  # Инвертирование направления движения, если установлен флаг инверсии
        #if self.direction != direction:
        self.client.write_registers(self.direction_address, int(direction), self.address)  # Запись значения направления движения в регистр
        self.direction = direction
    def get_registers(self) -> None:
        read_reg = self.client.read_input_registers(0, 10, self.address)  # Чтение регистров из устройства
        print(read_reg.registers)  # Вывод прочитанных значений регистров

class MecanumMoveController:
    def __init__(self):
        client = ModbusClient(
            method="rtu", port="/dev/ttyUSB1", stopbits=1, bytesize=8, parity='N', baudrate=9600
        )
        client.connect()

        self.front_left = MecanumWheelMotor(client, 22, 2, 3)  # Создание объекта мотора для переднего левого колеса
        self.front_right = MecanumWheelMotor(client, 23, 0, 1, True)  # Создание объекта мотора для переднего правого колеса с инверсией
        self.rear_left = MecanumWheelMotor(client, 22, 0, 1)  # Создание объекта мотора для заднего левого колеса
        self.rear_right = MecanumWheelMotor(client, 23, 2, 3, True)  # Создание объекта мотора для заднего правого колеса с инверсией

    def move(self, linear_velocity: Tuple[float, float], angular_velocity: float) -> None:
        vx, vy = linear_velocity
        wz = angular_velocity
        
        speeds = [
            vy + vx + wz,
            vy - vx - wz,
            vy - vx + wz,
            vy + vx - wz
        ]
        
        max_speed = max(map(abs, speeds))  # Вычисление максимальной скорости среди всех колес

        if max_speed > 1:
            speeds = [speed / max_speed for speed in speeds]  # Нормализация скоростей, если максимальная скорость больше 1
        
        for motor, speed in zip([self.front_left, self.front_right, self.rear_left, self.rear_right], speeds):
            motor.set_speed(speed)
        
        # self.front_left.set_speed(speeds[0])  # Установка скорости для переднего левого колеса
        # self.front_right.set_speed(speeds[1])  # Установка скорости для переднего правого колеса
        # self.rear_left.set_speed(speeds[2])  # Установка скорости для заднего левого колеса
        # self.rear_right.set_speed(speeds[3])  # Установка скорости для заднего правого колеса