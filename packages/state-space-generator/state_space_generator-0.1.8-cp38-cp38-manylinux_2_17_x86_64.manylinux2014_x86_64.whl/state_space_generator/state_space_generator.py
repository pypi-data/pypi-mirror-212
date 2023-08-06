import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

def build_callstring(max_time: float, max_num_states: int):
    result = "dump_reachable_search_space("
    if max_time is not None:
        result += f"max_time={max_time},"
    if max_num_states is not None:
        result += f"max_num_states={max_num_states},"
    result +=  ")"
    return result

def generate_state_space(domain: str, problem: str, max_time: str = None, max_num_states: int=None):
    command = [
        "python3",
        Path(HERE / 'scorpion/fast-downward.py').resolve(),
        "--keep-sas-file",
        Path(domain).resolve(),
        Path(problem).resolve(),
        "--translate-options",
        "--dump-static-predicates",
        "--dump-predicates",
        "--dump-constants",
        "--dump-static-atoms",
        "--dump-goal-atoms",
        "--search-options",
        "--search",
        build_callstring(max_time, max_num_states)]
    print(f'Executing "{" ".join(map(str, command))}"')
    with open("run.log", "w") as file:
        subprocess.run(command, stdout=file,text=True)

# for debugging purposes
# python3 ./fast-downward.py ../../domain.pddl ../../p-1-0.pddl --translate-options --dump-static-predicates --dump-predicates --dump-constants --dump-static-atoms --dump-goal-atoms --search-options --search "dump_reachable_search_space(max_time=0)"
