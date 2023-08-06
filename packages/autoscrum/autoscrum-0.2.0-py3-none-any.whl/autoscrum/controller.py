import guidance
import re
import textwrap
import json
from pathlib import Path
from datetime import datetime
guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo")

ROOT = Path(__file__).resolve().parent
PROGRAM = "controller"
critic = guidance((ROOT / "critic.hbs").read_text())
controller = guidance((ROOT / "controller.hbs").read_text())
subtasker = guidance((ROOT / "subgoals.hbs").read_text())
qna_program = guidance((ROOT / "questioner.hbs").read_text())

data=json.loads((Path(__file__).parent / "data.json").read_text())

critic = critic(
    goal=data["goal"],
    desired_state=data["desired_state"],
    current_state=data["current_state"],
    inventory=data["inventory"],
    task=data["task"],
    context=data["context"],
)
print(critic["response"])
critique = json.loads(critic["response"])
controller = controller(
    goal=data["goal"],
    desired_state=data["desired_state"],
    current_state=data["current_state"],
    inventory=data["inventory"],
    tasks_completed=data["tasks_completed"],
    tasks_failed=data["tasks_failed"],
    questions=[],
    critique=critique["critique"]
)
print(controller["response"])
task = json.loads(controller["response"])

subtasks = subtasker(
    task=task,
)
subtask = json.loads(subtasks["response"])

res = qna_program(
    goal=data["goal"],
    desired_state=data["desired_state"],
    current_state=data["current_state"],
    inventory=data["inventory"],
    task=task["task"],
    context=data["context"],
    time=datetime.now().strftime("%H:%M:%S")
)
with open(str(ROOT / Path(PROGRAM+".adoc")), 'a') as f:
    f.write(str(controller))

print(json.dumps(critique, indent=4))
print(json.dumps(task, indent=4))
print(json.dumps(subtask, indent=4))
print(res["response"])
#print(json.dumps(questions, indent=4))

