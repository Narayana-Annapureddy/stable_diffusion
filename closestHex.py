import pandas as pd
import math

def color_distance(rgb1, rgb2):
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)))

def closest_color(target_rgb, color_list):
    distances = [color_distance(target_rgb, color) for color in color_list]
    return 'monk ' + str(distances.index(min(distances))+1)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

monk_codes = [(246, 237, 228),(243, 231, 219), (247, 234, 208), (234, 218, 186), (215, 189, 150),
              (160, 126, 86), (130, 92, 67), (96, 65, 52), (58, 49, 42), (41, 36, 32)]

df = pd.read_excel('Hex_values.xlsx')

# Assuming the hex values are in a column named 'Hex'
df['Closest Skin Tone'] = df['Avg Hex'].apply(lambda x: closest_color(hex_to_rgb(x), monk_codes))

# Save the updated DataFrame back to an Excel file
output_path = 'closest_monk.xlsx'
df.to_excel(output_path, index=False)

print('done')