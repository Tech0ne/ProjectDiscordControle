from discord import app_commands
import discord
import json
import os

SERVER_ID = 
CATEGORY_ID = 

ROLE_ID = 

# 🔴・Started  Project Name
# 🔵・Finished Project Name

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

personal_chans = {}
# {
#     user_id: chan_id
# }

projects_chans = {}
# {
#     category_id: {
#         "text_id": text_channel_id,
#         "voc_id": vocal_channel_id,
#         "project_over": True if project is over, False otherwise,
#         "collaborators" = [
#             user_id,
#             user_id,
#             ...
#         ]
#     }
# }

def save_infos(filename: str, data: dict):
    with open(filename, 'w+') as f:
        json.dump(data, f)

def load_infos(filename: str) -> dict:
    with open(filename, 'r') as f:
        return json.load(f)

@client.event
async def on_member_join(member):
    global personal_chans
    guild = client.get_guild(SERVER_ID)
    category = discord.Object(id=CATEGORY_ID)
    overrides = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True)
    }
    role = guild.get_role(ROLE_ID)
    await member.add_roles(role)
    channel = await guild.create_text_channel(f"🔵・chat-{member.global_name}", category=category, overwrites=overrides)
    personal_chans[member.id] = channel.id
    save_infos("./personnals.json", personal_chans)

@client.event
async def on_member_remove(member):
    global personal_chans
    guild = client.get_guild(SERVER_ID)
    try:
        channel = guild.get_channel(personal_chans[member.id])
    except:
        print(f"Could not find {member.id} in {personal_chans}")
    else:
        await channel.delete()
        del personal_chans[member.id]
        save_infos("./personnals.json", personal_chans)

@tree.command(
    name="addproject",
    description="Add a project",
    guild=client.get_guild(SERVER_ID)
)
async def add_project(interaction):
    pass

if not os.path.isfile("./personnals.json"):
    save_infos("./personnals.json", personal_chans)

if not os.path.isfile("./projects.json"):
    save_infos("./projects.json", projects_chans)

personal_chans = load_infos("./personnals.json")
projects_chans = load_infos("./projects.json")

client.run("TOKEN")