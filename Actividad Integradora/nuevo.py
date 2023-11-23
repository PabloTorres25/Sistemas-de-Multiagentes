
def information(model):
    auto_info = []
    for agent in model.schedule.agents:
        if isinstance(agent, Auto):
            auto_info.append(f"{agent.info}")
    return auto_info

class AutoInfoText(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        info = information(model)
        info_html = ''.join([f'<div>{line}</div>' for line in info])
        return f'<div>{info_html}</div>'
