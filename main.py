import random
import math
import colorsys
import numpy as np
from PIL import Image, ImageDraw

#########################################
#            TWEAKING VALUES

#image dimensions
w = 512
h = 512

# color [HUE, LIGHTING, SATURATION]

color1 = [0, 0, 100]
color2 = [359, 80, 100]

#perlin noise parameters
octaves = 8
bias = 1.4

#########################################

hueVec1 = []

len = w * h

def interpolate_angle(a, b, n):
	a_rad = math.radians(a)
	b_rad = math.radians(b)

	diff = b_rad - a_rad
	if diff > math.pi:
		diff -= 2 * math.pi
	elif diff < -math.pi:
		diff += 2 * math.pi

	interpolated_rad = a_rad + n * diff

	interpolated_deg = math.degrees(interpolated_rad)

	return (interpolated_deg + 360) % 360

def main():
	global w, h, len

	noiseMap = [None] * len
	perlin = [None] * len

	for i in range(0, len, 1):
		noiseMap[i] = random.uniform(0.0, 1.0)
		perlin[i] = 0.0
	
	octaves = 6
	bias = 1.4

	for y in range(0, h, 1):
		for x in range(0, w, 1):
			distance = math.floor(1 << octaves - 1)

			noise = 0.0
			scaleAcc = 0.0
			scale = 1.0

			for o in range(0, octaves, 1):
				pitch = math.floor(distance >> o)

				sampleX1 = (x // pitch) * pitch
				sampleY1 = (y // pitch) * pitch

				sampleX2 = (sampleX1 + pitch) % w
				sampleY2 = (sampleY1 + pitch) % h

				blendX = float(x - sampleX1) / float(pitch)
				blendY = float(y - sampleY1) / float(pitch)

				sampleT = (1.0 - blendX) * noiseMap[sampleY1 * w + sampleX1] + blendX * noiseMap[sampleY1 * w + sampleX2]
				sampleB = (1.0 - blendX) * noiseMap[sampleY2 * w + sampleX1] + blendX * noiseMap[sampleY2 * w + sampleX2]

				scaleAcc += scale
				noise += (blendY * (sampleB - sampleT) + sampleT) * scale
				scale = scale / bias

			perlin[y * w + x] = noise / scaleAcc

	img = Image.new(mode = "RGB", size = (w, h))

	g = ImageDraw.Draw(img)

	for y2 in range(0, h, 1):
		for x2 in range(0, w, 1):
			finalHue = interpolate_angle(color1[0], color2[0], perlin[y2 * w + x2])
			finalLightness = float(color1[1]) + perlin[y2 * w + x2] * (float(color2[1]) - float(color1[1]))
			finalSaturation = float(color1[2]) + perlin[y2 * w + x2] * (float(color2[2]) - float(color1[2]))

			rgb = colorsys.hls_to_rgb(finalHue / 360.0, finalLightness / 100.0, finalSaturation / 100.0)
			rgb_int = [math.floor(rgb[0] * 256), math.floor(rgb[1] * 256), math.floor(rgb[2] * 256)]

			rgb_int = [rgb_int[0] if rgb_int[0] < 256 else 255, rgb_int[1] if rgb_int[1] < 256 else 255, rgb_int[2] if rgb_int[2] < 256 else 255]

			g.point((x2, y2), (rgb_int[0], rgb_int[1], rgb_int[2]))

	img.save("perlinNoise.png")


if __name__ == "__main__":
	main()
