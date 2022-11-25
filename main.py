from gl import Raytracer, V3
import math
import conversions as conv
import struct
from intersect import *
from lights import *
from material import *
from sphere import *
from collections import namedtuple
import matMath as mt
from textures import *
from obj import *
from math import cos, sin, tan, pi


width = 1280
height = 720

# Materiales a usar
redBulb = Material(diffuse=(0.9, 0.42, 0.42), spec=64,
                   ior=1.5, matType=TRANSPARENT)
whiteBulb = Material(diffuse=(0.8, 0.8, 0.8), spec=64,
                     ior=1.5, matType=TRANSPARENT)
body1 = Material(diffuse=(1, 0.85, 0.42), spec=64,
                 ior=1.5, matType=TRANSPARENT)
body2 = Material(diffuse=(0.9, 0.7, 0.42), spec=64,
                 ior=1.5, matType=TRANSPARENT)
body3 = Material(diffuse=(0.9, 0.9, 0.9), spec=64,
                 ior=1.5, matType=TRANSPARENT)
eyes = Material(diffuse=(0, 0, 0), spec=64,
                ior=1.5, matType=OPAQUE)
gBow = Material(diffuse=(0.4, 0.9, 0.6), spec=64,
                ior=1.5, matType=TRANSPARENT)
rBow = Material(diffuse=(0.9, 0.42, 0.42), spec=64,
                ior=1.5, matType=TRANSPARENT)

rtc = Raytracer(width, height)

# Fondo
rtc.envMap = Texture("bck.bmp")

# Luces
rtc.lights.append(AmbientLight(intensity=0.1))
rtc.lights.append(DirectionalLight(direction=(0, 0, -1), intensity=0.1))
rtc.lights.append(DirectionalLight(direction=(0, 0, -5), intensity=0.1))

# Oso 1

# Main sphere
rtc.scene.append(Sphere(center=(5, 0, -10), radius=2, material=redBulb))
# Head
rtc.scene.append(Sphere(center=(5, 2.9, -10), radius=1.5, material=body1))
rtc.scene.append(Sphere(center=(3.4, 4.1, -10), radius=0.8, material=body2))
rtc.scene.append(Sphere(center=(6.6, 4.1, -10), radius=0.8, material=body2))
rtc.scene.append(Sphere(center=(4.8, 2.7, -8.3), radius=0.6, material=body2))
# Nose
rtc.scene.append(Sphere(center=(4.8, 2.7, -7.5), radius=0.2, material=eyes))
# Body
rtc.scene.append(Sphere(center=(3.2, -1.6, -9), radius=0.8, material=body1))
rtc.scene.append(Sphere(center=(6.8, -1.6, -9), radius=0.8, material=body1))
rtc.scene.append(Sphere(center=(3, 1, -9), radius=0.8, material=body1))
rtc.scene.append(Sphere(center=(6.8, 1, -9), radius=0.8, material=body1))
# Bow tie
rtc.scene.append(Sphere(center=(5, 1.7, -8.3), radius=0.3, material=gBow))
rtc.scene.append(Sphere(center=(5.6, 1.7, -8.3), radius=0.4, material=gBow))
rtc.scene.append(Sphere(center=(4.5, 1.7, -8.3), radius=0.4, material=gBow))

# Oso 2

# Main sphere
rtc.scene.append(Sphere(center=(-5, 0, -10), radius=2, material=whiteBulb))
# Head
rtc.scene.append(Sphere(center=(-5, 2.9, -10), radius=1.5, material=body3))
rtc.scene.append(Sphere(center=(-3.4, 4.1, -10), radius=0.8, material=body3))
rtc.scene.append(Sphere(center=(-6.6, 4.1, -10), radius=0.8, material=body3))
rtc.scene.append(Sphere(center=(-4.8, 2.7, -8.3), radius=0.6, material=body3))
# Nose
rtc.scene.append(Sphere(center=(-4.8, 2.7, -7.5), radius=0.2, material=eyes))
# Body
rtc.scene.append(Sphere(center=(-3.2, -1.6, -9), radius=0.8, material=body3))
rtc.scene.append(Sphere(center=(-6.8, -1.6, -9), radius=0.8, material=body3))
rtc.scene.append(Sphere(center=(-3, 1, -9), radius=0.8, material=body3))
rtc.scene.append(Sphere(center=(-6.8, 1, -9), radius=0.8, material=body3))
# Bow tie
rtc.scene.append(Sphere(center=(-5, 1.7, -8.3), radius=0.3, material=rBow))
rtc.scene.append(Sphere(center=(-5.6, 1.7, -8.3), radius=0.4, material=rBow))
rtc.scene.append(Sphere(center=(-4.5, 1.7, -8.3), radius=0.4, material=rBow))

rtc.glRender()
rtc.write("output.bmp")
