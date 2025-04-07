import json 
import datetime

from src.actps.core.trafic_monitor import AbstractTraficStorageManager


class TraficStorageManager(AbstractTraficStorageManager):

    def __init__(self, file_path: str):
        self._file_path = file_path

    def write(self, logs):
        today = datetime.date.today()
        month = today.month  
        day = today.day     
        year = today.year

        self.ndjon_wirte(
            logs=logs,
            year=year,
            month=month,
            day=day
        )


    def ndjon_wirte(self, logs, year: int, month: int, day: int):
        path_to_file = str(year)+"_"+str(month)+"_"+str(day)
        path = self._file_path + path_to_file 
        with open(path, "a", encoding="utf-8") as f:
            for log in logs:
                data = json.dumps(log, ensure_ascii=False)
                f.write(data+"\n")


    def ndjson_read(self, year: int, month: int, day: int, start_hour: int, end_hour: int, depth: int):
        path_to_file = str(year)+"_"+str(month)+"_"+str(day)
        path = self._file_path + path_to_file 

# Если ни start_hour, ни depth не заданы, выбрасываем ошибку
        if start_hour is None and depth is None:
            raise ValueError("incorrect initial data")

        # Вычисляем временные границы (если заданы)
        if start_hour is not None:
            lower_bound = datetime.datetime(year, month, day, start_hour, 0, 0).timestamp()
        if end_hour is not None:
            upper_bound = datetime.datetime(year, month, day, end_hour, 0, 0).timestamp()

        logs = []
        count_log = 0

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    log = json.loads(line)
                except Exception:
                    continue

                if "time" not in log:
                    continue

                t = float(log["time"])

                if start_hour is not None and end_hour is not None:
                    if lower_bound <= t <= upper_bound:
                        logs.append(log)
                    elif t > upper_bound:
                        break
                else:
                    logs.append(log)

                count_log += 1
                if depth is not None and count_log >= depth:
                    break

        return logs
