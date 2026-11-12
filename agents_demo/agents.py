"""
Три простых агента, соединённых в пайплайн. Без библиотек и без API-ключа.

Запуск:  python3 agents_demo/agents.py

Что здесь есть:
  - tools    : обычные функции, которые агент может вызвать
  - brain    : "мозг" агента. Здесь это простые правила.
               В настоящем агенте мозг = вызов языковой модели (см. README.md)
  - Agent    : цикл "подумать -> вызвать инструмент -> получить результат -> ответить"
  - pipeline : маршрутизатор передаёт задачу нужному агенту
"""

import re

# ---------- Инструменты (tools) ----------
EVENTS = [
    {"day": "Mon", "time": "10:00", "title": "Стендап"},
    {"day": "Tue", "time": "14:00", "title": "Врач"},
    {"day": "Tue", "time": "16:00", "title": "Созвон с командой"},
]


def get_events(day: str) -> list:
    return [e for e in EVENTS if e["day"].lower() == day.lower()]


def count_words(text: str) -> int:
    return len(text.split())


# ---------- Трассировка: печатаем каждый шаг, чтобы видеть поток ----------
def log(agent: str, msg: str):
    print(f"  [{agent}] {msg}")


# ---------- Агент ----------
class Agent:
    def __init__(self, name, instructions, tools, brain, max_steps=5):
        self.name = name
        self.instructions = instructions  # роль агента ("системный промпт")
        self.tools = tools                # словарь: имя -> функция
        self.brain = brain                # решает, что делать дальше
        self.max_steps = max_steps

    def run(self, task: str) -> str:
        history = []  # что уже сделано в этом запуске (память агента)
        for _ in range(self.max_steps):
            decision = self.brain(task, history, self.tools)
            if "answer" in decision:                      # готов ответ -> выходим
                log(self.name, f"ответ: {decision['answer']}")
                return decision["answer"]
            tool_name, args = decision["tool"], decision["args"]
            log(self.name, f"вызывает инструмент {tool_name}({args})")
            result = self.tools[tool_name](**args)
            log(self.name, f"получил результат: {result}")
            history.append((tool_name, args, result))
        return "Лимит шагов исчерпан"


# ---------- "Мозги" агентов (правила вместо языковой модели) ----------
def summarizer_brain(task, history, tools):
    # Шаг 1: попросить инструмент посчитать слова
    if not history:
        return {"tool": "count_words", "args": {"text": task}}
    # Шаг 2: получили число -> формулируем ответ
    words = history[-1][2]
    short = " ".join(task.split()[:12])
    return {"answer": f"«{short}…» (всего слов: {words})"}


DAY_WORDS = {"mon": "Mon", "понедельник": "Mon", "tue": "Tue", "вторник": "Tue"}


def calendar_brain(task, history, tools):
    # Шаг 1: понять, какой день, и вызвать get_events
    if not history:
        day = next((d for k, d in DAY_WORDS.items() if k in task.lower()), None)
        if day is None:
            return {"answer": "Не понял, на какой день смотреть."}
        return {"tool": "get_events", "args": {"day": day}}
    # Шаг 2: получили список встреч -> пересказываем
    events = history[-1][2]
    if not events:
        return {"answer": "В этот день встреч нет."}
    return {"answer": ", ".join(f"{e['time']} {e['title']}" for e in events)}


summarizer_agent = Agent(
    name="Summarizer",
    instructions="Сокращай тексты.",
    tools={"count_words": count_words},
    brain=summarizer_brain,
)

calendar_agent = Agent(
    name="Calendar",
    instructions="Отвечай про встречи в календаре.",
    tools={"get_events": get_events},
    brain=calendar_brain,
)

AGENTS = {"calendar": calendar_agent, "summarizer": summarizer_agent}


# ---------- Маршрутизатор (Router): решает, кому отдать задачу ----------
def router_choice(task: str) -> str:
    if re.search(r"встреч|календар|вторник|понедельник|mon|tue", task.lower()):
        return "calendar"
    return "summarizer"


# ---------- Пайплайн: Router -> агент -> результат ----------
def pipeline(task: str) -> str:
    log("Router", "решает, кому отдать задачу...")
    chosen = router_choice(task)
    log("Router", f"передаёт -> {chosen}")
    return AGENTS[chosen].run(task)


if __name__ == "__main__":
    tasks = [
        "Какие у меня встречи во вторник?",
        "Что у меня в понедельник?",
        "Сократи этот текст: Сегодня хорошая погода и мы идём гулять в парк, а потом пьём чай дома.",
    ]
    for t in tasks:
        print(f"\n=== Задача: {t}")
        print(f"=== Итог: {pipeline(t)}")
