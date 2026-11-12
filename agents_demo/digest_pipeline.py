"""
Дайджест-пайплайн: Роутер -> Slack-агент / Почта-агент -> Писатель -> документ.

Запуск:
  python3 agents_demo/digest_pipeline.py
  python3 agents_demo/digest_pipeline.py "Сделай дайджест из Slack за 3 дня"

Результат:
  agents_demo/output/digest.md  - документ (заглушка вместо Google Docs)
  agents_demo/flow.html         - визуализация: откройте файл в браузере

Slack и почта здесь - фейковые данные. Настоящие подключения описаны в README.
"""

import html
import json
import re
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent

# ---------- Фейковые данные вместо реального Slack и почты ----------
SLACK = [
    {"days_ago": 0, "channel": "#design", "who": "Анна", "text": "Макеты экрана оплаты готовы, жду фидбэк до пятницы."},
    {"days_ago": 1, "channel": "#product", "who": "Игорь", "text": "Запуск переносим на следующий месяц из-за API."},
    {"days_ago": 1, "channel": "#design", "who": "Мария", "text": "Обновила палитру, новые цвета уже в дизайн-системе."},
    {"days_ago": 2, "channel": "#general", "who": "Олег", "text": "В пятницу общий обед в офисе."},
]

GMAIL = [
    {"days_ago": 0, "from": "Поддержка", "subject": "Жалобы на кнопку оплаты", "text": "Три клиента не смогли оплатить заказ."},
    {"days_ago": 2, "from": "Бухгалтерия", "subject": "Счёт за лицензии", "text": "Счёт прислан, срок оплаты 10 дней."},
]


# ---------- Трассировка: каждое сообщение между агентами ----------
class Trace:
    def __init__(self):
        self.events = []

    def send(self, frm, to, text):
        self.events.append({"from": frm, "to": to, "text": text})
        print(f"  {frm:>7} -> {to:<7} {text}")


# ---------- Роутер: решает, какие источники нужны ----------
def route(request: str) -> list:
    r = request.lower()
    plan = []
    if re.search(r"slack|слак", r):
        plan.append("slack")
    if re.search(r"почт|gmail|письм|mail", r):
        plan.append("gmail")
    return plan or ["slack", "gmail"]  # если не сказали - смотрим всё


def parse_days(request: str) -> int:
    m = re.search(r"(\d+)\s*дн", request.lower())
    return int(m.group(1)) if m else 3


def pretty_date(days_ago: int) -> str:
    return (date.today() - timedelta(days=days_ago)).strftime("%d.%m")


# ---------- Агенты-источники: каждый читает свой источник ----------
def slack_agent(days: int) -> list:
    return [
        f"{pretty_date(m['days_ago'])} {m['channel']} {m['who']}: {m['text']}"
        for m in SLACK if m["days_ago"] < days
    ]


def gmail_agent(days: int) -> list:
    return [
        f"{pretty_date(m['days_ago'])} {m['from']} ({m['subject']}): {m['text']}"
        for m in GMAIL if m["days_ago"] < days
    ]


AGENTS = {"slack": slack_agent, "gmail": gmail_agent}
SOURCE_NAMES = {"slack": "Slack", "gmail": "Почта"}


# ---------- Писатель: собирает summary и текст документа ----------
def write_doc(days: int, sources: list) -> str:
    total = sum(len(items) for _, items in sources)
    parts = ", ".join(f"{SOURCE_NAMES[s]}: {len(items)}" for s, items in sources)
    lines = [
        "## Кратко",
        f"За последние {days} дн. собрано записей: {total} ({parts}).",
        "",
    ]
    for src, items in sources:
        lines.append(f"## {SOURCE_NAMES[src]}")
        lines += [f"- {x}" for x in items] or ["- Ничего за этот период."]
        lines.append("")
    return "\n".join(lines)


# ---------- Сохранение документа (заглушка вместо Google Docs) ----------
def save_doc(title: str, body: str) -> Path:
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    path = out / "digest.md"
    path.write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
    return path


# ---------- Пайплайн целиком ----------
def run(request: str):
    trace = Trace()
    days = parse_days(request)
    trace.send("user", "router", request)

    plan = route(request)
    sources = []
    for src in plan:
        trace.send("router", src, f"Собери записи за {days} дн.")
        items = AGENTS[src](days)
        trace.send(src, "writer", f"Нашёл {len(items)} шт.")
        sources.append((src, items))

    title = f"Дайджест за {days} дн."
    body = write_doc(days, sources)
    trace.send("writer", "doc", f"Оформил документ «{title}», передаю на сохранение")
    path = save_doc(title, body)
    trace.send("doc", "user", f"Готово (заглушка Google Docs): {path.name}")

    write_flow_html(trace.events, f"# {title}\n\n{body}")
    return path


# ---------- Визуализация: отдельная HTML-страница с пошаговой анимацией ----------
FLOW_TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Как работают агенты</title>
<style>
:root{--bg:#f7f6f2;--card:#fff;--ink:#1d1d1b;--muted:#6b6a63;--line:#d9d6cc;--accent:#d97757;--ok:#3f8f5a}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1d1d1b;--card:#2a2a27;--ink:#f0eee6;--muted:#a8a69c;--line:#44433e;--accent:#e08a6b;--ok:#6cc08b}}
:root[data-theme="dark"]{--bg:#1d1d1b;--card:#2a2a27;--ink:#f0eee6;--muted:#a8a69c;--line:#44433e;--accent:#e08a6b;--ok:#6cc08b}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,sans-serif;padding:16px}
h1{font-size:20px;margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 16px}
.stage{display:grid;grid-template-columns:repeat(5,1fr);grid-template-rows:auto auto;gap:12px;align-items:center}
.node{background:var(--card);border:2px solid var(--line);border-radius:12px;padding:12px 8px;text-align:center;transition:all .3s}
.node small{display:block;color:var(--muted);font-size:12px}
.node.done{border-color:var(--ok)}
.node.active{border-color:var(--accent);box-shadow:0 0 0 4px rgba(217,119,87,.25);transform:scale(1.04)}
.controls{margin:16px 0;display:flex;gap:8px;flex-wrap:wrap}
button{background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 14px;font:inherit;cursor:pointer}
button:hover{border-color:var(--accent)}
.now{font-weight:600;color:var(--accent);min-height:24px}
.panel{background:var(--card);border-radius:12px;padding:12px 14px;margin-top:12px}
.ev{padding:8px 10px;border-left:3px solid var(--line);margin:6px 0;opacity:.4;transition:opacity .3s}
.ev.past{opacity:.7}
.ev.on{opacity:1;border-color:var(--accent)}
.ev b{color:var(--accent)}
pre{white-space:pre-wrap;word-wrap:break-word;margin:0;font:13px/1.5 ui-monospace,monospace}
@media (max-width:700px){.stage{grid-template-columns:1fr 1fr}.node.span{grid-row:auto}}
</style>
</head>
<body>
<h1>Как работают агенты</h1>
<p class="sub">Нажимайте «Далее», чтобы идти по шагам. Подсвеченный блок - тот, кто сейчас работает.</p>

<div class="stage">
  <div class="node" id="n-user" style="grid-column:1;grid-row:1/span 2">Вы<small>даёте задачу</small></div>
  <div class="node" id="n-router" style="grid-column:2;grid-row:1/span 2">Роутер<small>решает, кого спросить</small></div>
  <div class="node" id="n-slack" style="grid-column:3;grid-row:1">Slack-агент<small>читает Slack</small></div>
  <div class="node" id="n-gmail" style="grid-column:3;grid-row:2">Почта-агент<small>читает почту</small></div>
  <div class="node" id="n-writer" style="grid-column:4;grid-row:1/span 2">Писатель<small>делает summary</small></div>
  <div class="node" id="n-doc" style="grid-column:5;grid-row:1/span 2">Google Док<small>документ</small></div>
</div>

<div class="controls">
  <button id="prev">← Назад</button>
  <button id="next">Далее →</button>
  <button id="auto">▶ Авто</button>
  <button id="reset">↺ Сначала</button>
</div>
<div class="now" id="now"></div>

<div class="panel" id="log"></div>

<div class="panel">
  <b>Итоговый документ</b>
  <pre id="doc"></pre>
</div>

<script>
const TRACE = __TRACE__;
const DOC = __DOC__;
const LABEL = {user:"Вы", router:"Роутер", slack:"Slack-агент", gmail:"Почта-агент", writer:"Писатель", doc:"Google Док"};
const logEl = document.getElementById("log");
const nowEl = document.getElementById("now");
const docEl = document.getElementById("doc");
let i = -1, timer = null;

TRACE.forEach((e) => {
  const d = document.createElement("div");
  d.className = "ev";
  d.innerHTML = "<b>" + LABEL[e.from] + " → " + LABEL[e.to] + "</b><br>";
  d.appendChild(document.createTextNode(e.text));
  logEl.appendChild(d);
});

function render() {
  const nodes = ["user","router","slack","gmail","writer","doc"];
  const visited = new Set();
  for (let k = 0; k <= i; k++) { visited.add(TRACE[k].from); visited.add(TRACE[k].to); }
  const current = i >= 0 ? TRACE[i].to : null;
  nodes.forEach((n) => {
    const el = document.getElementById("n-" + n);
    el.classList.toggle("active", n === current);
    el.classList.toggle("done", visited.has(n) && n !== current);
  });
  [...logEl.querySelectorAll(".ev")].forEach((el, k) => {
    el.classList.toggle("on", k === i);
    el.classList.toggle("past", k < i);
  });
  nowEl.textContent = i >= 0 ? "Шаг " + (i + 1) + " из " + TRACE.length + ": " + LABEL[TRACE[i].from] + " передаёт задачу: " + LABEL[TRACE[i].to] : "Нажмите «Далее», чтобы начать";
  docEl.textContent = i === TRACE.length - 1 ? DOC : "Документ ещё не создан. Он появится на последнем шаге.";
}

function stop() { clearInterval(timer); timer = null; }
document.getElementById("next").onclick = () => { stop(); if (i < TRACE.length - 1) i++; render(); };
document.getElementById("prev").onclick = () => { stop(); if (i > -1) i--; render(); };
document.getElementById("reset").onclick = () => { stop(); i = -1; render(); };
document.getElementById("auto").onclick = () => {
  if (timer) return stop();
  if (i >= TRACE.length - 1) i = -1;
  timer = setInterval(() => { if (i >= TRACE.length - 1) return stop(); i++; render(); }, 1200);
};
render();
</script>
</body>
</html>
"""


def write_flow_html(events: list, doc_text: str):
    # Подставляем данные в шаблон; "</" экранируем, чтобы текст не закрыл тег <script>
    trace_js = json.dumps(events, ensure_ascii=False).replace("</", "<\\/")
    doc_js = json.dumps(doc_text, ensure_ascii=False).replace("</", "<\\/")
    page = FLOW_TEMPLATE.replace("__TRACE__", trace_js).replace("__DOC__", doc_js)
    (HERE / "flow.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    import sys

    request = sys.argv[1] if len(sys.argv) > 1 else "Сделай дайджест из Slack и почты за 3 дня"
    print(f"=== Запрос: {request}")
    result = run(request)
    print(f"\nДокумент: {result}")
    print(f"Визуализация: {HERE / 'flow.html'}")
