import asyncio

from aioEasyPillow import Canvas, Editor, Font, Text, load_image


data = {  # Most likely coming from the on_member_join event
    'name': 'Guddi#9552',
    'guild': 'This Guild',
    'member': '1638'
}


async def create_welcome_image():
    background = Editor('assets/background.png')
    profile = Editor('assets/avatar.png')
    # To use users profile picture load it from url using the `load_image` function

    await profile.resize((150, 150))
    await profile.circle_image()

    font_big = Font.poppins(variant='bold', size=50)
    font_small = Font.poppins(variant='bold', size=25)

    await background.paste(profile, (325, 90))
    await background.ellipse((325, 90), 150, 150, outline='#0BE7F5', stroke_width=4)
    await background.text(
        (400, 260), 'WELCOME',
        color='white', font=font_big, align='center', stroke_color='black', stroke_width=3
    )
    await background.text(
        (400, 325), data['name'],
        color='white', font=font_small, align='center', stroke_color='black', stroke_width=2
    )
    await background.text(
        (400, 370), 'You are the 457th Member',
        color='#ec4804', font=font_small, align='center', stroke_color='black', stroke_width=2
    )

    await background.show()


asyncio.run(create_welcome_image())