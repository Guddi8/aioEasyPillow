import asyncio

from aioEasyPillow import Canvas, Editor, Font, Text, load_image


user_data = {  # Most likely coming from database or calculation
    'name': 'Guddi#9552',
    'level': 8,
    'current_xp': 605,
    'next_level_xp': 820,
    'rank': 2
}


async def create_rank_card():
    background = Editor(Canvas((900, 280), color='#23272A'))  # create a background image
    profile = Editor('assets/avatar.png')   # open the avatar
    # To use users profile picture load it from url using the `load_image` function

    await profile.resize((190, 190))
    await profile.circle_image()

    font_big = Font.poppins(size=35)

    await background.rectangle((20, 20), 860, 240, "#2a2e35")

    await background.paste(profile, (50, 50))
    await background.ellipse((42, 42), width=206, height=206, outline="#43b581", stroke_width=10)
    await background.rectangle((260, 180), width=600, height=40, fill="#484b4e", radius=20)
    await background.bar(
        (260, 180),
        max_width=600,
        height=40,
        percentage=int(user_data['current_xp'] / user_data['next_level_xp'] * 100),
        fill='#00fa81',
        radius=20,
    )

    await background.text((270, 120), user_data['name'], font=font_big, color='#00fa81')
    await background.text(
        (845, 125),
        f"{user_data['current_xp']} / {user_data['next_level_xp']}",
        font=font_big,
        color='#00fa81',
        align='right',
    )

    rank_level_texts = [
        Text('Rank ', color='#00fa81', font=font_big),
        Text(f'{user_data["rank"]}', color='#1EAAFF', font=font_big),
        Text('   Level ', color='#00fa81', font=font_big),
        Text(f'{user_data["level"]}', color='#1EAAFF', font=font_big),
    ]
    await background.multicolor_text((820, 30), texts=rank_level_texts, align='right')

    await background.show()


asyncio.run(create_rank_card())