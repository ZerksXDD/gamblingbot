import discord
from discord.ext import commands
import json
import os
import time
import asyncio
from discord.ui import Button, View
import random
import datetime
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from datetime import datetime






# Define your rank thresholds (ensure it's defined only once)
ranks = [
    ("Novice Gambler", 0), ("Casual Bettor", 5000), ("Lucky Player", 10000),
    ("Serious Gambler", 15000), ("High Roller", 20000), ("Jackpot Winner", 25000),
    ("Casino Pro", 30000), ("Master of Dice", 35000), ("Card Shark", 40000),
    ("Roulette King", 45000), ("Betting Legend", 50000), ("Wager Wizard", 55000),
    ("Poker Titan", 60000), ("Slot Machine Champion", 65000), ("Gambling Guru", 70000),
    ("Epic Gambler", 75000), ("Casino Emperor", 80000), ("Legendary Bettor", 85000),
    ("Ultimate Jackpot", 90000), ("High Stakes Master", 95000), ("Casino Royalty", 100000),
    ("Betting Deity", 105000), ("Wagering God", 110000), ("Casino Virtuoso", 115000),
    ("Gambling Sovereign", 120000), ("Jackpot Legend", 125000), ("High Roller Elite", 130000),
    ("Gambling Champion", 135000), ("Master of Fortune", 140000), ("Casino Overlord", 145000),
    ("Betting Supremacy", 150000), ("Ultimate Gambler", 155000), ("Gambling Maestro", 160000),
    ("High Stakes Legend", 165000), ("Grand Casino Champion", 170000), ("Master Gambler", 175000),
    ("Supreme Wagerer", 180000), ("Casino Legend", 185000), ("Betting God", 190000),
    ("Ultimate Casino Master", 195000), ("Legendary High Roller", 200000), ("Supreme Jackpot Winner", 205000),
    ("Gambling Icon", 210000), ("Ultimate Gambling Legend", 215000), ("Royal Casino Sovereign", 220000),
    ("Master of the Casino", 225000), ("Grand Wagering Champion", 230000), ("Elite High Stakes Master", 235000),
    ("Gambling Royalty", 240000), ("Ultimate Gambling Legend", 245000), ("Supreme Casino Champion", 250000),
    ("Ultimate High Roller", 255000), ("Legendary Gambling Deity", 260000), ("Grand Casino Royalty", 265000),
    ("Supreme Gambling Legend", 270000), ("Gambling Overlord", 275000), ("Ultimate Casino Master", 280000),
    ("Legendary High Stakes Overlord", 285000), ("Grand Master Gambler", 290000), ("Supreme Casino Sovereign", 295000),
    ("Ultimate Gambling Emperor", 300000), ("Legendary Jackpot Master", 305000), ("Grand High Roller", 310000),
    ("Supreme Gambling Sovereign", 315000), ("Ultimate Gambling Icon", 320000), ("Legendary Gambling Emperor", 325000),
    ("Supreme Casino Champion", 330000), ("Ultimate High Stakes Sovereign", 335000), ("Legendary Casino Overlord", 340000),
    ("Grand Gambling Sovereign", 345000), ("Ultimate Gambling Icon", 350000), ("Legendary Casino Sovereign", 355000),
    ("Supreme Gambling Champion", 360000), ("Ultimate Casino Master", 365000), ("Legendary High Stakes Overlord", 370000),
    ("Grand Casino Master", 375000), ("Supreme Gambling Icon", 380000), ("Ultimate Gambling Overlord", 385000),
    ("Legendary High Roller Sovereign", 390000), ("Supreme Casino Emperor", 395000), ("Ultimate Gambling God", 400000),
    ("Legendary Jackpot Master", 405000), ("Grand High Roller", 410000), ("Supreme Gambling Royalty", 415000),
    ("Ultimate Casino Overlord", 420000), ("Legendary High Stakes Champion", 425000), ("Grand Gambling Legend", 430000),
    ("Supreme High Stakes Master", 435000), ("Ultimate Casino Sovereign", 440000), ("Legendary Gambling Deity", 445000),
    ("Supreme Gambling Sovereign", 450000), ("Ultimate Gambling Legend", 455000), ("Legendary Casino Champion", 460000),
    ("Supreme Gambling Emperor", 465000), ("Ultimate High Stakes Sovereign", 470000), ("Legendary Casino Master", 475000),
    ("Supreme Gambling Icon", 480000), ("Ultimate Gambling Overlord", 485000), ("Legendary High Roller Sovereign", 490000),
    ("Supreme Casino Emperor", 495000), ("Ultimate Gambling God", 500000)
]
def load_json_file(filepath):
    """Load JSON data from a file."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json_file(filepath, data):
    """Save JSON data to a file."""
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving file {filepath}: {e}")

def get_rank(chips):
    """Get the user's rank based on their chips."""
    for rank, threshold in reversed(ranks):
        if chips >= threshold:
            return rank, threshold
    return ranks[0][0], 0

def get_next_rank(chips):
    """Get the next rank and chips needed for the next rank."""
    for i in range(len(ranks)):
        if chips < ranks[i][1]:
            next_rank = ranks[i][0]
            chips_needed = ranks[i][1] - chips
            return next_rank, chips_needed
    return None, None

def embed_message(title, description):
    """Create an embedded message."""
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    return embed

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix=['/', '!'], intents=intents, help_command=None)

def initialize_user_data_file():
    """Initialize the user data file with an empty dictionary."""
    if not os.path.exists(USER_DATA_FILE):
        save_user_data({})


# File paths
CHIPS_FILE = 'chips.json'
DATA_FILE = 'user_data.json'
USER_DATA_FILE = 'user_data.json'

# Define rewards
REWARDS = {
    'hourly': 500,
    'daily': 5000,
    'weekly': 10000,
    'monthly': 30000
}

# Define cooldown periods
COOLDOWNS = {
    'hourly': timedelta(hours=1),
    'daily': timedelta(days=1),
    'weekly': timedelta(weeks=1),
    'monthly': timedelta(weeks=4)
}

def load_user_data():
    """Load user data from a JSON file."""
    try:
        with open(USER_DATA_FILE, 'r') as file:
            content = file.read()
            print(f"Content of {USER_DATA_FILE}: {content}")  # Debugging line
            data = json.loads(content)
            if not isinstance(data, dict):
                return {}  # If the data is not a dictionary, return an empty dictionary
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading user data: {e}")
        return {}


def save_user_data(data):
    """Save user data to a JSON file."""
    try:
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving user data: {e}")


def get_last_redeemed(user_data, reward_type):
    return user_data.get('last_redeemed', {}).get(reward_type, None)

def set_last_redeemed(user_data, reward_type):
    now = datetime.now().isoformat()
    if 'last_redeemed' not in user_data:
        user_data['last_redeemed'] = {}
    user_data['last_redeemed'][reward_type] = now

@bot.command(name='redeem')
async def redeem(ctx, reward_type: str = None):
    if reward_type is None:
        await ctx.send("You have to type `/redeem hourly`, `/redeem daily`, `/redeem weekly`, or `/redeem monthly`.")
        return

    if reward_type.lower() not in REWARDS:
        await ctx.send("Invalid reward type. Use 'hourly', 'daily', 'weekly', or 'monthly'.")
        return
    
    user_id = str(ctx.author.id)
    user_data = load_user_data().get(user_id, {})

    now = datetime.now()
    last_redeemed = get_last_redeemed(user_data, reward_type.lower())
    
    if last_redeemed:
        last_redeemed_time = datetime.fromisoformat(last_redeemed)
        cooldown_period = COOLDOWNS[reward_type.lower()]
        if now - last_redeemed_time < cooldown_period:
            remaining_time = cooldown_period - (now - last_redeemed_time)
            await ctx.send(f"You can redeem this reward in {remaining_time}.")
            return
    
    # Update user data
    user_data['chips'] = user_data.get('chips', 0) + REWARDS[reward_type.lower()]
    set_last_redeemed(user_data, reward_type.lower())
    save_user_data({user_id: user_data})

    await ctx.send(f"You have redeemed {REWARDS[reward_type.lower()]} chips for the {reward_type.lower()} reward!")
    
# Load and save functions
def load_chips():
    try:
        with open(CHIPS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_chips(data):
    with open(CHIPS_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.command(name='slots')
async def slots(ctx, bet: int = None):
    if bet is None:
        await ctx.send("Please specify an amount to bet using `/slots [amount]`. Example: `/slots 100`")
        return

    if bet <= 0:
        await ctx.send("Bet amount must be positive.")
        return
    
    user_id = str(ctx.author.id)
    chips = load_json_file(CHIPS_FILE)

    if user_id not in chips or chips[user_id] < bet:
        await ctx.send("You don't have enough chips to play.")
        return

    symbols = ['🍒', '🍋', '🍊', '🍉', '🍇', '🍓']
    
    # Initial message
    initial_embed = embed_message("Slots", "🎰 **| | |**\nSpinning...")
    message = await ctx.send(embed=initial_embed)

    # Spin animation
    for _ in range(10):
        spin = [random.choice(symbols) for _ in range(3)]
        spin_display = f"**{spin[0]} | {spin[1]} | {spin[2]}**"
        updated_embed = embed_message("Slots", f"🎰 {spin_display}\nSpinning...")
        await message.edit(embed=updated_embed)
        await asyncio.sleep(0.5)

    # Final result
    spin = [random.choice(symbols) for _ in range(3)]
    win = len(set(spin)) == 1
    reward = bet * 5 if win else -bet
    chips[user_id] = chips.get(user_id, 0) + reward
    save_json_file(CHIPS_FILE, chips)

    result_message = f"{'Congratulations, you won!' if win else 'Sorry, you lost.'} {abs(reward)} chips. Your new balance is {chips[user_id]} chips."
    final_embed = embed_message("Slots", f"🎰 **{spin[0]} | {spin[1]} | {spin[2]}**\n{result_message}")
    await message.edit(embed=final_embed)

@bot.command(name='help')
async def help_command(ctx):
    help_text = """
    **Gambling Commands:**

    **/balance/bal** - Show your current chip balance and rank. 💵
    **/rank** - Get information about your current rank and chips needed for the next rank. 🏅
    **/profile** - Display your profile with your chips balance and rank. 📜
    **/donate [amount] [@recipient]** - Donate chips to another user. 🎁
    **/slots [amount]** - Gamble away your life savings. 🎰
    **/spin [amount]** - Spin your life savings away.🛞
    **/dice [amount]** - Get 4+ to win anything less you loose.🎲
    **/coinflip [heads/tails] [amount]** - Heads or Tails?🪙
    **/blackjack [amount]** - Classic blackjack game.🃏
    **/scratchoff [amount of cards to scratch]** - Scratch off tickets!⛏️
    **/redeem [hourly,daily,weekly,monthly]** - Free rewards! 🎁

    **More commands and features coming soon! Any recommendations text me @boujiec on discord**
    """
    
    embed = discord.Embed(title="Help Menu", description=help_text, color=discord.Color.green())
    await ctx.send(embed=embed)

# Define emojis for the wheel
wheel_emojis = ['🍎', '🍊', '🍒', '🍉', '🍇', '🍋', '🍓']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command(name='dice')
async def dice(ctx, bet: int = None):
    if bet is None:
        await ctx.send(f"Make sure to do /dice [amount] to place your bet.")
        return

    user_id = str(ctx.author.id)
    chips = load_json_file(CHIPS_FILE)

    if bet <= 0:
        await ctx.send("Bet amount must be positive.")
        return
    
    if user_id not in chips or chips[user_id] < bet:
        await ctx.send("You don't have enough chips to play.")
        return

    symbols = ['🎲', '🎲', '🎲', '🎲', '🎲', '🎲']
    message = await ctx.send(embed=embed_message("Dice Roll", "Rolling the die..."))

    for _ in range(10):
        roll = random.choice(symbols)
        await message.edit(embed=embed_message("Dice Roll", f"🎲 **{roll}**\nRolling..."))
        await asyncio.sleep(0.5)
    
    die_result = random.randint(1, 6)
    reward = bet * die_result
    chips[user_id] = chips.get(user_id, 0) + reward
    save_json_file(CHIPS_FILE, chips)
    await message.edit(embed=embed_message("Dice Roll", f"🎲 **{die_result}**\nYou rolled a {die_result}. You {'won' if die_result > 3 else 'lost'} {abs(reward)} chips."))

@bot.command(name='coinflip')
async def coinflip(ctx, choice: str = None, bet: int = None):
    # Check if both choice and bet are provided
    if choice is None or bet is None:
        await ctx.send("Make sure to use /coinflip [heads/tails] [amount] to place your bet.")
        return

    choice = choice.lower()
    # Validate the choice
    if choice not in ['heads', 'tails']:
        await ctx.send("Invalid choice. Please choose 'heads' or 'tails'.")
        return

    user_id = str(ctx.author.id)
    chips = load_json_file(CHIPS_FILE)

    # Validate the bet amount
    if bet <= 0:
        await ctx.send("Bet amount must be positive.")
        return
    
    if user_id not in chips or chips[user_id] < bet:
        await ctx.send("You don't have enough chips to play.")
        return

    # Start the coin flip animation
    symbols = ['🪙', '🪙']  # Same emoji used for animation effect
    message = await ctx.send(embed=embed_message("Coin Flip", "Flipping the coin..."))

    # Simulate the coin flip animation
    for _ in range(10):
        flip = random.choice(symbols)
        await message.edit(embed=embed_message("Coin Flip", f"🪙 **{flip}**\nFlipping..."))
        await asyncio.sleep(0.5)
    
    # Determine the random result of the coin flip
    result = random.choice(['heads', 'tails'])
    win = (result == choice)
    reward = bet * 2 if win else -bet
    chips[user_id] = chips.get(user_id, 0) + reward
    save_json_file(CHIPS_FILE, chips)
    
    # Display the final result
    await message.edit(embed=embed_message("Coin Flip", f"🪙 **{result.capitalize()}**\nThe coin landed on {result}. You {'won' if win else 'lost'} {abs(reward)} chips."))




@bot.command(name='spin')
async def spin(ctx, bet: int = None):
    if bet is None:
        await ctx.send("Please specify an amount to bet using `/spin [amount]`. Example: `/spin 100`")
        return

    if bet <= 0:
        await ctx.send("Bet amount must be positive.")
        return
    
    user_id = str(ctx.author.id)
    chips = load_json_file(CHIPS_FILE)

    if user_id not in chips or chips[user_id] < bet:
        await ctx.send("You don't have enough chips to play.")
        return

    symbols = ['❌', '❌', '❌', '❌', '❌', '💰']  # Low chance for money bag
    arrow = '➡️'
    
    # Initial message
    initial_embed = embed_message("Spin the Wheel", f"🎡 **{arrow} | ❌ | ❌ | ❌**\nSpinning...")
    message = await ctx.send(embed=initial_embed)

    # Spin animation
    for _ in range(5):  # Number of animation frames
        # Move the arrow over the symbols
        symbol_sequence = symbols.copy()
        random.shuffle(symbol_sequence)  # Shuffle symbols to create variability
        arrow_position = random.randint(0, len(symbols) - 1)
        symbol_sequence[arrow_position] = arrow
        
        spin_display = ' | '.join(symbol_sequence)
        updated_embed = embed_message("Spin the Wheel", f"🎡 **{spin_display}**\nSpinning...")
        await message.edit(embed=updated_embed)
        await asyncio.sleep(0.2)  # Short delay between updates
    
    # Final result
    final_result = random.choices(symbols, weights=[1]*5 + [0.1])[0]  # Low chance for money bag
    win = final_result == '💰'
    reward = bet * 10 if win else -bet
    chips[user_id] = chips.get(user_id, 0) + reward
    save_json_file(CHIPS_FILE, chips)

    result_message = f"{'Congratulations, you won!' if win else 'Sorry, you lost.'} {abs(reward)} chips. Your new balance is {chips[user_id]} chips."
    final_embed = embed_message("Spin the Wheel", f"🎡 **{final_result}**\n{result_message}")
    await message.edit(embed=final_embed)



@bot.command(name='rank')
async def rank(ctx):
    user_id = str(ctx.author.id)
    chips = load_chips()
    user_balance = chips.get(user_id, 0)
    current_rank, current_threshold = get_rank(user_balance)
    next_rank, chips_needed = get_next_rank(user_balance)

    embed = discord.Embed(title=f"{ctx.author.name}'s Rank Information", color=discord.Color.purple())
    embed.add_field(name="Current Rank", value=current_rank, inline=False)
    
    if next_rank:
        embed.add_field(name="Next Rank", value=next_rank, inline=False)
        embed.add_field(name="Chips Needed for Next Rank", value=f"{chips_needed} 💎", inline=False)
    else:
        embed.add_field(name="Next Rank", value="N/A", inline=False)
        embed.add_field(name="Chips Needed for Next Rank", value="You are at the highest rank!", inline=False)

    await ctx.send(embed=embed)

@bot.command(name='profile')
async def profile(ctx):
    user_id = str(ctx.author.id)
    chips = load_chips()
    user_balance = chips.get(user_id, 0)
    
    rank, _ = get_rank(user_balance)
    
    embed = discord.Embed(title="Profile", description=f"{ctx.author.mention}, here's your profile information:", color=discord.Color.blue())
    embed.add_field(name="💵 Chips Balance", value=f"{user_balance} chips", inline=False)
    embed.add_field(name="🏅 Rank", value=rank, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='donate')
async def donate(ctx, amount: int, recipient: discord.User):
    if amount <= 0:
        await ctx.send("Donation amount must be positive.")
        return
    
    user_id = str(ctx.author.id)
    recipient_id = str(recipient.id)
    chips = load_chips()
    
    if user_id not in chips or chips[user_id] < amount:
        await ctx.send("You don't have enough chips to donate.")
        return
    
    chips[user_id] -= amount
    chips[recipient_id] = chips.get(recipient_id, 0) + amount
    save_chips(chips)
    
    await ctx.send(f"Successfully donated {amount} chips to {recipient.mention}.")

# Helper functions for rank calculations
def get_rank(chips):
    for rank, threshold in reversed(ranks):
        if chips >= threshold:
            return rank, threshold
    return ranks[0][0], 0

def get_next_rank(chips):
    for i in range(len(ranks)):
        if chips < ranks[i][1]:
            next_rank = ranks[i][0]
            chips_needed = ranks[i][1] - chips
            return next_rank, chips_needed
    return None, None






# Deck setup with emoji representation for the cards
deck = {
    '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣',
    '10': '🔟', 'J': '🃏', 'Q': '👸', 'K': '🤴', 'A': '🅰️'
}

card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def calculate_hand_value(hand):
    value = sum(card_values[card] for card in hand)
    ace_count = hand.count('A')
    
    while value > 21 and ace_count > 0:
        value -= 10
        ace_count -= 1
    
    return value

def draw_card():
    return random.choice(list(deck.keys()))

deck = {
    '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣',
    '10': '🔟', 'J': '🃏', 'Q': '👸', 'K': '🤴', 'A': '🅰️'
}

card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def calculate_hand_value(hand):
    value = sum(card_values[card] for card in hand)
    ace_count = hand.count('A')
    
    while value > 21 and ace_count > 0:
        value -= 10
        ace_count -= 1
    
    return value

def draw_card():
    return random.choice(list(deck.keys()))

@bot.command(name='blackjack')
async def blackjack(ctx, bet: int = None):
    if bet is None:
        await ctx.send("Please provide a bet amount: `/blackjack [amount]`.")
        return
    
    user_id = str(ctx.author.id)
    chips = load_json_file(CHIPS_FILE)

    if bet <= 0:
        await ctx.send("Bet amount must be positive.")
        return
    
    if user_id not in chips or chips[user_id] < bet:
        await ctx.send("You don't have enough chips to play.")
        return

    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]
    
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    player_hand_display = ' '.join(deck[card] for card in player_hand)
    dealer_hand_display = f"{deck[dealer_hand[0]]} ❓"

    message = await ctx.send(embed=embed_message("Blackjack", f"**Your hand:** {player_hand_display} ({player_value})\n**Dealer's hand:** {dealer_hand_display}"))

    view = BlackjackView(player_hand, dealer_hand, chips, user_id, bet, message)
    await message.edit(embed=embed_message("Blackjack", f"**Your hand:** {player_hand_display} ({player_value})\n**Dealer's hand:** {dealer_hand_display}"), view=view)

class BlackjackView(View):
    def __init__(self, player_hand, dealer_hand, chips, user_id, bet, message):
        super().__init__()
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.chips = chips
        self.user_id = user_id
        self.bet = bet
        self.message = message

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == int(self.user_id)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary)
    async def hit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_card = draw_card()
        self.player_hand.append(new_card)
        player_value = calculate_hand_value(self.player_hand)
        player_hand_display = ' '.join(deck[card] for card in self.player_hand)
        dealer_hand_display = f"{deck[self.dealer_hand[0]]} ❓"

        if player_value > 21:
            result_message = "You busted! Dealer wins."
            self.chips[self.user_id] -= self.bet
            self.stop()
        else:
            result_message = f"**Your hand:** {player_hand_display} ({player_value})\n**Dealer's hand:** {dealer_hand_display}"

        await self.message.edit(embed=embed_message("Blackjack", result_message))

        if player_value > 21:
            await self.end_game(interaction)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.secondary)
    async def stand_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        player_value = calculate_hand_value(self.player_hand)
        dealer_hand_display = ' '.join(deck[card] for card in self.dealer_hand)

        while calculate_hand_value(self.dealer_hand) < 17:
            new_card = draw_card()
            self.dealer_hand.append(new_card)
            dealer_hand_display = ' '.join(deck[card] for card in self.dealer_hand)

        dealer_value = calculate_hand_value(self.dealer_hand)
        if dealer_value > 21 or player_value > dealer_value:
            result_message = "You win!"
            self.chips[self.user_id] += self.bet
        elif player_value < dealer_value:
            result_message = "Dealer wins."
            self.chips[self.user_id] -= self.bet
        else:
            result_message = "It's a tie."

        await self.message.edit(embed=embed_message("Blackjack", f"**Your hand:** {' '.join(deck[card] for card in self.player_hand)} ({player_value})\n**Dealer's hand:** {dealer_hand_display} ({dealer_value})\n\n{result_message}"))
        await self.end_game(interaction)

    async def end_game(self, interaction):
        save_json_file(CHIPS_FILE, self.chips)
        self.stop()
        await interaction.response.defer()

def embed_message(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    return embed


@bot.command(name='balance')
async def balance(ctx):
    user_id = str(ctx.author.id)
    chips = load_json_file(CHIPS_FILE)
    user_balance = chips.get(user_id, 0)
    rank, _ = get_rank(user_balance)
    
    embed = discord.Embed(title=f"{ctx.author.name}'s Balance", color=discord.Color.blue())
    embed.add_field(name="Chips", value=f"{user_balance} 💎", inline=False)
    embed.add_field(name="Rank", value=rank, inline=False)
    
    await ctx.send(embed=embed)
@bot.command(name='bal')
async def bal(ctx):
    user_id = str(ctx.author.id)
    chips = load_json_file(CHIPS_FILE)
    user_balance = chips.get(user_id, 0)
    rank, _ = get_rank(user_balance)
    
    embed = discord.Embed(title=f"{ctx.author.name}'s Balance", color=discord.Color.blue())
    embed.add_field(name="Chips", value=f"{user_balance} 💎", inline=False)
    embed.add_field(name="Rank", value=rank, inline=False)
    
    await ctx.send(embed=embed)








#Emoji set for scratch cards with updated chances
scratch_symbols = ['💎', '❌', '❌', '❌', '❌', '💰', '❌', '❌', '❌', '💵']
hidden_symbol = '❓'

# Define rewards for matching symbols
reward_mapping = {
    '💎': 100,
    '❌': 0,
    '💰': 5000,
    '💵': 50000
}

def calculate_reward(card):
    """Calculate the reward based on the card symbols."""
    reward = 0
    for symbol in set(card):
        if card.count(symbol) >= 3:
            reward += reward_mapping.get(symbol, 0)
    return reward

@bot.command(name='scratchoff')
async def scratchoff(ctx, num_cards: int = 1):
    cost_per_card = 500
    total_cost = cost_per_card * num_cards

    user_id = str(ctx.author.id)
    chips = load_json_file(CHIPS_FILE)

    if num_cards <= 0:
        await ctx.send("The number of scratch offs must be positive.")
        return
    
    if user_id not in chips or chips[user_id] < total_cost:
        await ctx.send(f"You don't have enough chips to buy {num_cards} scratch off{'s' if num_cards > 1 else ''}.")
        return

    chips[user_id] -= total_cost
    save_json_file(CHIPS_FILE, chips)

    total_reward = 0
    for _ in range(num_cards):
        # Create a 3x3 scratch card grid
        card = random.choices(scratch_symbols, k=9)
        displayed_card = [hidden_symbol] * 9
        card_str = format_card(displayed_card)

        # Initial message
        message = await ctx.send(embed=embed_message("Scratch Off", f"{card_str}\n\nScratch to reveal!"))

        # Simulate scratching
        await asyncio.sleep(2)
        revealed_card = format_card(card)
        await message.edit(embed=embed_message("Scratch Off", f"{revealed_card}\n\nRevealing..."))

        # Determine the reward
        reward = calculate_reward(card)
        total_reward += reward

        # Final message for each card
        if reward > 0:
            result_message = f"You won {reward} chips!"
        else:
            result_message = f"You lost {cost_per_card} chips!"
        await asyncio.sleep(2)
        await message.edit(embed=embed_message("Scratch Off", f"{revealed_card}\n\n{result_message}"))

    # Update total chips after all cards are revealed
    chips[user_id] += total_reward
    save_json_file(CHIPS_FILE, chips)

    # Summary message
    total_loss = total_cost - total_reward
    if total_reward > 0:
        summary_message = f"You won {total_reward} chips in total from {num_cards} card{'s' if num_cards > 1 else ''}!"
    else:
        summary_message = f"You lost {total_loss} chips in total from {num_cards} card{'s' if num_cards > 1 else ''}."

    await ctx.send(embed=embed_message("Scratch Off Summary", summary_message))
    
def format_card(card):
    """Format the card into a 3x3 grid."""
    return f"{card[0]} {card[1]} {card[2]}\n{card[3]} {card[4]} {card[5]}\n{card[6]} {card[7]} {card[8]}"

def calculate_reward(card):
    """Calculate the reward based on the card symbols."""
    reward = 0
    for symbol in set(card):
        if card.count(symbol) >= 3:
            reward += reward_mapping.get(symbol, 0)
    return reward

def embed_message(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.gold())
    return embed







@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


# Run the bot
TOKEN = ''  # Replace with your bot token
bot.run(TOKEN)
