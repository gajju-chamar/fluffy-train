# Shinobu Music Bot
# Owner: @Sanji_fr


class AssistantErr(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)