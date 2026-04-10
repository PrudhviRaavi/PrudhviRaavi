import io
import requests
from PIL import Image

url = "https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif"
response = requests.get(url)
img = Image.open(io.BytesIO(response.content))

frames = []
for frame_idx in range(0, img.n_frames):
    img.seek(frame_idx)
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    
    # The original is a red fading line.
    # Map high Red to high Green & Blue to create Skyblue (Cyan-ish)
    # White centers will stay white because new_r=(b+g)/2 which is high when white.
    new_r = b
    new_g = r.point(lambda p: int(p * 0.95)) # Slight green shift for skyblue
    new_b = r 
    
    rgba_out = Image.merge("RGBA", (new_r, new_g, new_b, a))
    frames.append(rgba_out)

# Get exactly the same duration and loop settings
duration = img.info.get('duration', 50)
frames[0].save('blue_divider.gif', save_all=True, append_images=frames[1:], duration=duration, loop=0, disposal=2)
print("Successfully generated blue_divider.gif")
