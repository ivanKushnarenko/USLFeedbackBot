def answers_str(answers: list[str]) -> str:
    res = '\nВідповіді:'
    for answer in answers:
        res += f'\n\n{answer}'
    return res
