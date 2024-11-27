import discord
from discord.ext import commands
import json
import orderweekly
import ordermonthly
from checktrx import check_transaction_status
kj = open('config.json')
data = json.load(kj)
bot = discord.Bot()
@bot.command(name="weekly", description="Order Weekly Script Key")
async def weeklysc(ctx):
    json_file = "order_idsw.json"
    user_id = ctx.user.id 
    new_order_ids = orderweekly.generate_order_ids(json_file, user_id, 1)
    responses = orderweekly.send_transactions(new_order_ids)
    response_text = ""
    for order_id, response in zip(new_order_ids, responses):
        try:
            response_data = json.loads(response)
            redirect_url = response_data.get("redirect_url", "No redirect URL found")
        except json.JSONDecodeError:
            redirect_url = "Invalid response received from API"
        response_text += f"**Order ID**: `{order_id}`\n**Payment Link**: {redirect_url}\n\n"
    embed = discord.Embed(
        title="Distrans | Weekly",
        description=response_text,
        color=0xc9eded
    )
    await ctx.response.send_message(embed=embed, ephemeral=True)

@bot.command(name="monthly", description="Order Monthly Script Key")
async def monthlysc(ctx):
    json_file = "order_idsm.json"
    user_id = ctx.user.id
    new_order_ids = ordermonthly.generate_order_ids(json_file, user_id, 1)
    responses = ordermonthly.send_transactions(new_order_ids)
    response_text = ""
    for order_id, response in zip(new_order_ids, responses):
        try:
            response_data = json.loads(response)
            redirect_url = response_data.get("redirect_url", "No redirect URL found")
        except json.JSONDecodeError:
            redirect_url = "Invalid response received from API"
        response_text += f"**Order ID**: `{order_id}`\n**Payment Link**: {redirect_url}\n\n"
    embed = discord.Embed(
        title="Distrans | Monthly",
        description=response_text,
        color=0xc9eded
    )
    await ctx.response.send_message(embed=embed, ephemeral=True)
@bot.command(name="claimkey", description="Claim Key")
async def claimkey(ctx, transaction_id: str):
    user_id = ctx.user.id
    result = check_transaction_status(transaction_id, user_id)
    
    embed = discord.Embed(
        title="Distrans | Transaction Status",
        description=result,
        color=0xc9eded
    )
    await ctx.response.send_message(embed=embed, ephemeral=True)
class KeyListView(discord.ui.View):
    def __init__(self, keys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = keys
        options = [
            discord.SelectOption(label=f"Key: {key['key']}", description=f"Type: {key['type']}")
            for key in keys
        ]
        self.add_item(discord.ui.Select(
            placeholder="Select a key to view details...",
            options=options,
            custom_id="key_list_select",
        ))

    @discord.ui.select(custom_id="key_list_select")
    async def select_callback(self, select, interaction):
        selected_key = next((key for key in self.keys if f"Key: {key['key']}" == select.values[0]), None)
        if selected_key:
            await interaction.response.send_message(
                f"You selected:\n**Key**: {selected_key['key']}\n**Type**: {selected_key['type']}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("Selected key not found.", ephemeral=True)
class PaginatedKeyListView(discord.ui.View):
    def __init__(self, keys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = keys
        self.current_page = 0
        self.keys_per_page = 25
        self.select_menu = discord.ui.Select(
            placeholder="Select a key to view details...",
            custom_id="key_list_select",
            options=[],
        )
        self.select_menu.callback = self.select_callback
        self.update_options()

    def update_options(self):
        start = self.current_page * self.keys_per_page
        end = start + self.keys_per_page
        page_keys = self.keys[start:end]

        # Update the select menu options
        self.select_menu.options = [
            discord.SelectOption(label=f"Key: {key['key']}", description=f"Type: {key['type']}")
            for key in page_keys
        ]
        self.clear_items()
        self.add_item(self.select_menu)
        if self.current_page > 0:
            self.add_item(discord.ui.Button(label="Previous", style=discord.ButtonStyle.primary, custom_id="prev_page"))
        if end < len(self.keys):
            self.add_item(discord.ui.Button(label="Next", style=discord.ButtonStyle.primary, custom_id="next_page"))

    async def select_callback(self, interaction: discord.Interaction):
        selected_label = interaction.data["values"][0]
        selected_key = next((key for key in self.keys if f"Key: {key['key']}" == selected_label), None)

        if selected_key:
            await interaction.response.send_message(
                f"{selected_key['key']}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("Selected key not found.", ephemeral=True)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, custom_id="prev_page")
    async def prev_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page -= 1
        self.update_options()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, custom_id="next_page")
    async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page += 1
        self.update_options()
        await interaction.response.edit_message(view=self)



@bot.command(name="keylist", description="List all keys a user has purchased")
async def keylist(ctx):
    user_id = ctx.user.id
    log_file = "transaction_log.json"
    try:
        with open(log_file, "r") as file:
            transaction_log = json.load(file)
    except FileNotFoundError:
        transaction_log = []
    purchased_keys = [
        {
            "key": log["key_issued"],
            "type": "Weekly" if log["transaction_id"].startswith("GRCW") else
                    "Monthly" if log["transaction_id"].startswith("GRCM") else "Unknown"
        }
        for log in transaction_log if log["user_id"] == user_id
    ]

    if not purchased_keys:
        await ctx.response.send_message("No keys found for this user.", ephemeral=True)
        return
    view = PaginatedKeyListView(purchased_keys)
    await ctx.response.send_message("Here are your purchased keys:", view=view, ephemeral=True)


@bot.event
async def on_ready():
    print("Bot is ready!")
bot.run(data["bot-token"])