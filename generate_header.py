import math
from PIL import Image, ImageDraw, ImageFont, ImageSequence

def create_header_gif():
    # Load wave.gif
    wave_im = Image.open(r"c:\project\surf1k\wave.gif")
    wave_frames = [frame.copy().convert("RGBA") for frame in ImageSequence.Iterator(wave_im)]
    num_wave = len(wave_frames)

    # Canvas dimensions
    width = 720
    height = 96
    
    # Fonts
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 44)
    except:
        font = ImageFont.load_default()

    full_text = "Hi there, I'm ym1co "
    prefix = "Hi there, I'm "
    name = "ym1co"
    
    # Timing
    total_frames = 64
    typing_frames = 20
    typing_len = len(full_text)
    
    wave_size = 46 # scale wave hand to 46x46
    
    frames = []
    
    for i in range(total_frames):
        # Solid dark navy background #0A192F for flawless crisp edges
        img = Image.new("RGB", (width, height), (10, 25, 47)) # #0A192F
        draw = ImageDraw.Draw(img)
        
        # Rounded card border in #1E3A8A with fill #0B132B
        draw.rounded_rectangle(
            [(3, 3), (width - 4, height - 4)],
            radius=16,
            fill=(11, 19, 43), # #0B132B
            outline=(30, 58, 138), # #1E3A8A
            width=2
        )
        
        # Stylish terminal dots (cyan, blue, indigo)
        draw.ellipse([(22, 22), (32, 32)], fill=(56, 189, 248)) # #38BDF8 cyan
        draw.ellipse([(38, 22), (48, 32)], fill=(96, 165, 250)) # #60A5FA blue
        draw.ellipse([(54, 22), (64, 32)], fill=(30, 58, 138))  # #1E3A8A navy
        
        # Typing logic:
        if i < typing_frames:
            chars_to_show = int((i + 1) / typing_frames * typing_len)
            current_text = full_text[:chars_to_show]
            show_hand = (chars_to_show >= typing_len)
            cursor = "|" if (i % 4 < 2) else " "
        else:
            current_text = full_text
            show_hand = True
            cursor = "|" if ((i // 6) % 2 == 0) else " "
        
        # Render text
        text_x = 84
        text_y = 22
        
        if len(current_text) <= len(prefix):
            draw.text((text_x, text_y), current_text + cursor, font=font, fill=(241, 245, 249))
            current_x = text_x + draw.textlength(current_text, font=font)
        else:
            draw.text((text_x, text_y), prefix, font=font, fill=(241, 245, 249))
            prefix_w = draw.textlength(prefix, font=font)
            name_part = current_text[len(prefix):]
            draw.text((text_x + prefix_w, text_y), name_part + cursor, font=font, fill=(56, 189, 248))
            current_x = text_x + prefix_w + draw.textlength(name_part, font=font)
            
        # Draw waving hand
        if show_hand:
            wave_frame_idx = ((i - typing_frames) * 2) % num_wave
            wave_f = wave_frames[wave_frame_idx].resize((wave_size, wave_size), Image.Resampling.LANCZOS)
            hand_x = int(text_x + draw.textlength(prefix + name, font=font) + 12)
            hand_y = text_y + 2
            
            # Alpha composite wave_f onto img
            img.paste(wave_f, (hand_x, hand_y), wave_f)
            
        # Convert to P mode for GIF
        p_frame = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
        frames.append(p_frame)
        
    frames[0].save(
        r"c:\project\surf1k\header.gif",
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        optimize=True
    )
    print("Updated header.gif generated successfully!")

if __name__ == "__main__":
    create_header_gif()
