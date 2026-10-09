import math
from PIL import Image, ImageDraw, ImageFont

def generate_music_banner():
    width = 740
    height = 200
    total_frames = 36
    
    try:
        font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
        font_lyrics = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 17)
        font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_lyrics = ImageFont.load_default()
        font_small = ImageFont.load_default()

    lyrics_lines = [
        "\"You know I'm better than all the guys up in your cell phone",
        " If you leave me on read, I'll just move onto the next one",
        " I wanna see you again, but I don't wanna hurt myself, though",
        " Guess I'd rather see you and hurt than never see you again\""
    ]

    frames = []

    for f_idx in range(total_frames):
        # Base image
        img = Image.new("RGB", (width, height), (10, 25, 47)) # #0A192F
        draw = ImageDraw.Draw(img)

        # Rounded card in #0B132B with #1E3A8A border
        draw.rounded_rectangle(
            [(3, 3), (width - 4, height - 4)],
            radius=16,
            fill=(11, 19, 43),
            outline=(30, 58, 138),
            width=2
        )

        # Top dots (player window dots)
        draw.ellipse([(20, 18), (30, 28)], fill=(56, 189, 248)) # cyan
        draw.ellipse([(36, 18), (46, 28)], fill=(96, 165, 250)) # blue
        draw.ellipse([(52, 18), (62, 28)], fill=(30, 58, 138))  # navy

        # Title: NOW PLAYING • unrealgrave - not a game
        draw.text((74, 13), "NOW PLAYING :", font=font_small, fill=(148, 163, 184))
        draw.text((178, 11), "unrealgrave  —  not a game (2026)", font=font_title, fill=(56, 189, 248))

        # Animated Equalizer Bars on top-right
        eq_x = width - 110
        eq_y = 28
        bar_count = 6
        for b in range(bar_count):
            phase = f_idx / total_frames * 2 * math.pi + b * 1.1
            bar_h = int(6 + 10 * (math.sin(phase) + 1) / 2)
            draw.rectangle(
                [(eq_x + b * 8, eq_y - bar_h), (eq_x + b * 8 + 4, eq_y)],
                fill=(56, 189, 248) if b % 2 == 0 else (96, 165, 250)
            )

        # Thin divider line
        draw.line([(20, 42), (width - 20, 42)], fill=(30, 58, 138), width=1)

        # Lyrics rendering with subtle glowing pulse
        pulse = 0.5 + 0.5 * math.sin(f_idx / total_frames * 2 * math.pi)
        text_color_main = (226, 232, 240) # Slate-200
        highlight_color = (
            int(56 + 40 * pulse),
            int(189 + 40 * pulse),
            int(248)
        )

        y_offset = 54
        line_height = 24
        for l_i, line in enumerate(lyrics_lines):
            # Highlight key punchlines
            if l_i in [0, 3]:
                col = highlight_color
            else:
                col = text_color_main
            draw.text((32, y_offset + l_i * line_height), line, font=font_lyrics, fill=col)

        # Bottom Progress Bar
        bar_y = height - 28
        draw.text((32, bar_y - 2), "01:14", font=font_small, fill=(148, 163, 184))
        
        # Slider track
        slider_start = 78
        slider_end = width - 84
        draw.line([(slider_start, bar_y + 6), (slider_end, bar_y + 6)], fill=(30, 58, 138), width=3)
        
        # Slider fill
        slider_fill_ratio = 0.45 + 0.05 * (f_idx / total_frames)
        fill_x = int(slider_start + (slider_end - slider_start) * slider_fill_ratio)
        draw.line([(slider_start, bar_y + 6), (fill_x, bar_y + 6)], fill=(56, 189, 248), width=3)
        # Knob
        draw.ellipse([(fill_x - 4, bar_y + 2), (fill_x + 4, bar_y + 10)], fill=(241, 245, 249))

        draw.text((width - 70, bar_y - 2), "02:45", font=font_small, fill=(148, 163, 184))

        # Convert to P mode with palette
        p_frame = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
        frames.append(p_frame)

    frames[0].save(
        r"c:\project\surf1k\music_banner.gif",
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        optimize=True
    )
    print("music_banner.gif generated successfully!")

if __name__ == "__main__":
    generate_music_banner()
