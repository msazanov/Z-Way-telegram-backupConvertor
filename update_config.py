#!/usr/bin/python3
import argparse
import json

# Определение аргументов командной строки
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="имя файла")
parser.add_argument("--config", help="новое значение для параметра 'config'")
parser.add_argument("--port", help="новое значение для параметра 'port'")
args = parser.parse_args()

# Открытие файла и загрузка его содержимого в переменную data
with open(args.filename, "r") as file:
    data = json.load(file)

# Поиск первого блока с параметрами и обновление их значений, если параметры заданы в аргументах
for instance in data["config.json"]["instances"]:
    if instance["moduleId"] == "ZWave":
        if args.config is not None:
            instance["params"]["config"] = args.config
        if args.port is not None:
            instance["params"]["port"] = args.port
        break

# Сохранение обновленных данных в файле
with open(args.filename, "w") as file:
    json.dump(data, file, indent=4)
