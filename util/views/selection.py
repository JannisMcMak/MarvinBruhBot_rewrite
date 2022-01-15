import nextcord


class SimpleSelection(nextcord.ui.View):
    def __init__(self, num_choices: int, timeout: float = 20):
        super().__init__(timeout=timeout)
        self.choice = None

        while num_choices < len(self.children):
            self.remove_item(self.children[-1])


    @nextcord.ui.button(label="1")
    async def choice1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 1
        self.stop()

    @nextcord.ui.button(label="2")
    async def choice2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 2
        self.stop()

    @nextcord.ui.button(label="3")
    async def choice3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 3
        self.stop()

    @nextcord.ui.button(label="4")
    async def choice4(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 4
        self.stop()

    @nextcord.ui.button(label="5")
    async def choice5(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 5
        self.stop()

    @nextcord.ui.button(label="6")
    async def choice6(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 6
        self.stop()

    @nextcord.ui.button(label="7")
    async def choice7(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 7
        self.stop()

    @nextcord.ui.button(label="8")
    async def choice8(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 8
        self.stop()

    @nextcord.ui.button(label="9")
    async def choice9(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 9
        self.stop()

    @nextcord.ui.button(label="10")
    async def choice10(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = 10
        self.stop()

    