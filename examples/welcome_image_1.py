import asyncio

from aioEasyPillow import Canvas, Editor, Font, Text, load_image


data = {  # Most likely coming from the on_member_join event
    'name': 'Guddi#9552',
    'guild': 'This Guild',
    'member': '1638'
}


async def create_welcome_image():
    background = Editor(Canvas((900, 280), color='#23272A'))
    profile = Editor('assets/avatar.png')
    # To use users profile picture load it from url using the `load_image` function

    await profile.resize((200, 200))
    await profile.circle_image()


    font_regular = Font.montserrat(variant='italic', size=30)
    font_thin = Font.montserrat(variant='light', size=18)
    font_medium = Font.poppins(variant='bold', size=40)
    font_big = Font.poppins(variant='bold', size=50)

    card_left_shape = [(0, 0), (0, 270), (330, 270), (260, 0)]

    await background.polygon(card_left_shape, '#2C2F33')

    await background.paste(profile, (40, 35))
    await background.ellipse((40, 35), 200, 200, outline='white', stroke_width=3)

    await background.text((600, 20), 'WELCOME', font=font_big, color='white', align='center')
    await background.text((600, 70), data['name'], font=font_regular, color='#5865f2', align='center')

    await background.text((600, 130), 'YOU ARE MEMBER', font=font_medium, color='white', align='center')
    await background.text((600, 175), data['member'], font=font_regular, color='#5865f2', align='center')

    await background.text(
        (620, 245), 'THANK YOU FOR JOINING. WE HOPE YOU LIKE IT!',
        font=font_thin,
        color='white',
        align='center'
    )



    await background.save('outputs/welcome_image_1.png')
    await background.show()


asyncio.run(create_welcome_image())