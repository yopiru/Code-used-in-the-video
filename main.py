import discord
from discord import app_commands,Enum
from typing import Optional

MY_GUILD = discord.Object(id=)

class MyClient(discord.Client):
    def __init__(self,*,intents:discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

class test_choice(Enum):
    red = "red"
    blue = "blue"

class mybutton(discord.ui.View):
    def __init__(self,):
        super().__init__(timeout=5)
        self.value = None
    
    @discord.ui.button(label="ボタン",style=discord.ButtonStyle.green)
    async def confirm(self,inter:discord.Interaction,button:discord.ui.Button):
        await inter.response.send_message("ボタンが押されました。")
    @discord.ui.button(label="ボタン2",style=discord.ButtonStyle.green)

    async def cancel(self,inter:discord.Interaction,button:discord.ui.Button):
        await inter.response.send_message("ボタン2が押されました。")

        

class test_menu(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label="選択肢1",value="1",description="選択肢1です。"),discord.SelectOption(label="選択肢2",value="2",description="選択肢2です。"),discord.SelectOption(label="選択肢3",value="3",description="選択肢3です。")]
        super().__init__(placeholder="セレクトメニュー",min_values=1,max_values=1,options=options)
    async def callback(self,inter:discord.Interaction):
        await inter.response.send_message(f"セレクトメニュー{self.values[0]}が押されました")

class menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(test_menu())

intent = discord.Intents.default()
intent.message_content = True
client = MyClient(intents=intent)

@client.event
async def on_readey():
    print("botが起動しました。")

@client.tree.command(
    name = "test",
    description="これはテストです。",
)
async def test(inter:discord.Interaction):
    await inter.response.defer(ephemeral=True)
    await inter.followup.send("これはテストです！！")

@client.tree.command(
    name = "arg_test",
    description="これは引数のテストです。",
)
@app_commands.describe(arg="これは引数です。",arg2="これは選択引数です。")
async def test(inter:discord.Interaction,arg:str,arg2:test_choice):
    await inter.response.defer()
    await inter.followup.send(f"これはテストです！！ \n {arg} \n 任意引数: {arg2.value}")

@client.tree.command(
    name = "button_test",
    description="これは引数のテストです。",
)
async def test(inter:discord.Interaction):
    await inter.response.defer()
    v = mybutton()
    await inter.followup.send(embed=discord.Embed(title="ボタンを押してね",color=discord.Color.blue()),view=v)
    await v.wait()
    if v.value is None:
        await inter.edit_original_response(embed=discord.Embed(title="タイムアウト",color=discord.Color.red()),view=None)

@client.tree.command(
    name = "menu_test",
    description="これはセレクトメニューのテストです。",
)
async def test(inter:discord.Interaction):
    await inter.response.defer()
    v = menu()
    await inter.followup.send(embed=discord.Embed(title="選んでねを押してね",color=discord.Color.blue()),view=v)
    await v.wait()
    if v.value is None:
        await inter.edit_original_response(embed=discord.Embed(title="タイムアウト",color=discord.Color.red()),view=None)

@client.tree.context_menu(name="メッセージコマンド")
async def message_command(inter:discord.Interaction,message:discord.Message):
    await inter.response.defer()
    await inter.followup.send(f"このメッセージの投稿さんは {message.author.name} さん \n このメッセージのIDは {message.id}")

@client.tree.context_menu(name="ユーザージコマンド")
async def message_command(inter:discord.Interaction,member:discord.User):
    await inter.response.defer()
    await inter.followup.send(f"この人のお名前は {member.name} この人のユーザーIDは {member.id}")

client.run("")
