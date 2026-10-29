import functools
from pathlib import Path
import json
from datetime import datetime

def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[开始] {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[完成] {func.__name__}")
        return result
    return wrapper



class SaveSession:
    def __init__(self, index_path: Path):
        self.index_path = index_path

    def __enter__(self):
        if self.index_path.exists():
            with open(self.index_path, "r", encoding="utf-8") as f:
                self.records = json.load(f)
        else:
            self.records = []
        return self

    def __exit__(self, exc_type, exc, tb):
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False)
        print(f"索引已写回：共 {len(self.records)} 条")




def make_save_data(player: str, level: int, items: list[str] | None = None) -> dict:
    if items is None:
        return {"player": player, "level": level, "items": []}
    return {"player": player, "level": level, "items": items}



@log_action
def save_game(session: SaveSession, data: dict) -> str:
    time = datetime.now()
    file = Path("save" + str(len(session.records) + 1) + time.strftime("_%Y%m%d_%H%M%S") + ".json")
    file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    session.records.append({"file": file.name, "time": time.strftime("%Y-%m-%d %H:%M:%S"), "level": data["level"]})
    return file.name


@log_action
def load_save(filename: str) -> dict:
    return json.loads(Path(filename).read_text(encoding="utf-8"))



def iter_high_level(records: list[dict], min_level: int):
    for record in records:
        if record["level"] >= min_level:
            yield f"{record['time']} | Lv{record['level']} | {record['file']}"




with SaveSession(Path("index.json")) as session:
    first = make_save_data("Aria", 3)
    first["items"].append("木剑")
    save_game(session, first)
    second = make_save_data("Aria", 5)
    print(f"second 的道具： {second['items']}")
    save_game(session, second)
    third = make_save_data("Aria", 8, ["火焰剑"])
    last = save_game(session, third)


print("== Lv>=5 的存档 ==")

for record in iter_high_level(session.records, 5):
    print(record)


print(f"最新存档： {load_save(last)}")




    


