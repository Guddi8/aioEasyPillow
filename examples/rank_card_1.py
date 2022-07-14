import asyncio

from aioEasyPillow import Canvas, Editor, Font, Text, load_image


user_data = {  # Most likely coming from database or calculation
    'name': 'Guddi#9552',
    'level': 8,
    'current_xp': 605,
    'next_level_xp': 820,
    'total_xp': 3486
}


async def create_rank_card():
    background = Editor(Canvas((900, 300), color='#23272A'))  # create a background image
    profile = Editor('assets/avatar.png')   # open the avatar
    # To use users profile picture load it from url using the `load_image` function

    await profile.resize((150, 150))
    await profile.circle_image()

    font_big = Font.montserrat('bold', size=40)
    font_small = Font.montserrat('italic', size=30)


    card_shape_points = [(600, 0), (750, 300), (900, 300), (900, 0)]
    await background.polygon(card_shape_points, '#2C2F33')

    await background.paste(profile, (30, 30))

    await background.rectangle((30, 220), width=650, height=40, color='#494b4f', radius=20)
    await background.bar(
        (30, 220),
        max_width=650,
        height=40,
        percentage=int((user_data['current_xp'] / user_data['next_level_xp'] *100)),
        color='#3db374',
        radius=20,
    )
    await background.text((200, 40), user_data['name'], font=font_big, color='white')

    await background.rectangle((200, 100), width=350, height=2, color='#17F3F6')
    await background.text(
        (200, 130),
        f"Level: {user_data['level']}   XP: {user_data['current_xp']} / {user_data['next_level_xp']}",
        font=font_small,
        color='white',
    )

    await background.show()


asyncio.run(create_rank_card())