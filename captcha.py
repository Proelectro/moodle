from PIL import Image
import requests
import pytesseract
from collections import defaultdict
from dsu import DSU
image_path = "captcha.png"
image_url = "https://oauth.iitd.ac.in/securimage/securimage_show.php?94c6ececadc7647e583b9b80304be93b"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
with open(image_path, "wb") as f:
    f.write(requests.get(image_url).content)

captcha_image = Image.open(image_path)

captcha_image = captcha_image.convert("RGB")

image_width, image_height = captcha_image.size

pixels = captcha_image.load()

hmm = []
for i in range(-300, 300):
    for j in range(-300, 300):
        hmm.append((i, j))
hmm.sort(key=lambda x: x[0]*x[0] + x[1]*x[1])
line = [[False] * image_height for _ in range(image_width)]

for i in range(image_width):
    for j in range(image_height):
        if pixels[i, j] != (140, 140, 140):
            if pixels[i, j] != (255, 255, 255):
                pixels[i, j] = (255, 255, 255)
                line[i][j] = True
        else:
            pixels[i, j] = (0, 0, 0)

old_pixels = [[0] * image_height for _ in range(image_width)]

def nearest_fill():
    for i in range(image_width):
        for j in range(image_height):
            old_pixels[i][j] = pixels[i, j]
    
    for i in range(image_width):
        for j in range(image_height):
            if line[i][j] == True:
                for k1, l1 in hmm:
                    k, l = i + k1, j + l1
                    if k >= 0 and k < image_width and l >= 0 and l < image_height:
                        if line[k][l] == False:
                            pixels[i, j] = old_pixels[k][l]
                            break
                    

def thin():
    for i in range(image_width):
        for j in range(image_height):
            old_pixels[i][j] = pixels[i, j]
    for i in range(image_width):
        for j in range(image_height):
            for k in range(i-1, i+2):
                for l in range(j-1, j+2):
                    if k >= 0 and k < image_width and l >= 0 and l < image_height:
                        if old_pixels[k][l] == (255, 255, 255):
                            pixels[i, j] = (255, 255, 255)
                            

def thick():
    for i in range(image_width):
        for j in range(image_height):
            old_pixels[i][j] = pixels[i, j]

    for i in range(image_width):
        for j in range(image_height):
            if old_pixels[i][j] != (255, 255, 255):
                for k in range(i-1, i+2):
                    for l in range(j-1, j+2):
                        if k >= 0 and k < image_width and l >= 0 and l < image_height:
                            pixels[k, l] = old_pixels[i][j]


nearest_fill()
thin()
thick()

dsu = DSU(image_width * image_height)

for i in range(image_width):
    for j in range(image_height):
        if pixels[i, j] == (0, 0, 0):
            for k in range(i, i+2):
                for l in range(j, j+2):
                    if k - i + l - j == 1:
                        if k >= 0 and k < image_width and l >= 0 and l < image_height:
                            if pixels[k, l] == (0, 0, 0):
                                dsu.union(i*image_height + j, k*image_height + l)
clusters = defaultdict(list)
cluster_center = defaultdict(int)

for i in range(image_width):
    for j in range(image_height):
        if pixels[i, j] == (0, 0, 0):
            rank = dsu.get_rank(i*image_height + j)
            if rank > 20:
                p = dsu.find(i*image_height + j)
                clusters[p].append((i, j))
                cluster_center[p] += i
for i in clusters:
    cluster_center[i] /= len(clusters[i])

center_number = list(zip(cluster_center.values(), cluster_center.keys()))
center_number.sort()

for k, (_, i) in enumerate(center_number):
    margin = 10
    min_x, min_y = image_width, image_height
    max_x, max_y = 0, 0
    for x, y in clusters[i]:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    image_i = Image.new("RGB", (max_x - min_x + 1 + margin, max_y - min_y + 1 + margin), (255, 255, 255))
    for x, y in clusters[i]:
        image_i.putpixel((x - min_x + margin // 2, y - min_y + margin // 2), (0, 0, 0))
    
    # image_i = Image.new("RGB", (image_width, image_height), (255, 255, 255))
    # for x, y in clusters[i]:
    #     image_i.putpixel((x, y), (0, 0, 0))
    
    image_i.save(f"captcha_{k}.png")
    
    text = pytesseract.image_to_string(image_i, lang='eng')
    print(text)

captcha_image.save("captcha_modified.png")
text = pytesseract.image_to_string(captcha_image, lang='eng')
print(text)