from sentientis import envs


def run(iterations: int, env: str, train: bool):
    environment = envs.factory(env)
