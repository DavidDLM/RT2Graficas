# Raytracing
# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso
import math
import conversions as conv
import struct
from intersect import *
from lights import *
from material import *
from sphere import *
from collections import namedtuple
import matMath as mt
from obj import *
from math import cos, sin, tan, pi

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

STEPS = 1
MAX_REC_DEPTH = 4


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=l', d)


def _color_(r, g, b):
    return bytes([int(b*255),
                  int(g*255),
                  int(r*255)])


# Colores default
white = _color_(1, 1, 1)
black = _color_(0, 0, 0)


def baryCoords(A, B, C, P):

    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        # PBC / ABC
        u = areaPBC / areaABC
        # PAC / ABC
        v = areaPAC / areaABC
        # 1 - u - v
        w = 1 - u - v
    except:
        return -1, -1, -1
    else:
        return u, v, w


class Raytracer(object):
    def __init__(this, width, height):
        this.width = width
        this.height = height
        this.fov = 60
        this.camPosition = V3(0, 0, 0)
        this.nearPlane = 0.1
        this.scene = []
        this.lights = []
        this.envMap = None
        this.clearColor = black
        this.currColor = white
        this.glViewPort(0, 0, this.width, this.height)
        this.glClear()

    # Utiliza las coordenadas
    def glViewPort(this, x, y, width, height):
        this.viewportX = x
        this.viewportY = y
        this.viewportWidth = width
        this.viewportHeight = height

    # Limpia los pixeles de la pantalla poniendolos en blanco o negro
    def glClear(this):
        this.framebuffer = [[this.clearColor for y in range(this.height)]
                            for x in range(this.width)]

    # Coloca color de fondo
    def glClearColor(this, r, g, b):
        this.clearColor = _color_(r, g, b)

    def glPoint(this, x, y, color=None):
        # Coordenadas de la ventana
        if (0 <= x < this.width) and (0 <= y < this.height):
            this.framebuffer[x][y] = color or this.currColor

    # Se establece el color de dibujo, si no tiene nada se dibuja blanco
    def glColor(this, r, g, b):
        this.currColor = _color_(r, g, b)

    def glClearViewPort(this, color=None):
        for x in range(this.viewportX, this.viewportX + this.viewportWidth):
            for y in range(this.viewportY, this.viewportY + this.viewportHeight):
                this.glPoint(x, y, color)

    def scene_intersect(this, orig, direction, sceneObj):
        depth = float('inf')
        intersect = None

        for obj in this.scene:
            hit = obj.ray_intersect(orig, direction)
            if hit != None:
                if sceneObj != hit.sceneObj:
                    if hit.distance < depth:
                        intersect = hit
                        depth = hit.distance

        return intersect

    def cast_ray(this, orig, direction, sceneObj=None, recursion=0):
        intersect = this.scene_intersect(orig, direction, sceneObj)

        if intersect == None or recursion >= MAX_REC_DEPTH:
            if this.envMap:
                return this.envMap.getEnvColor(direction)
            else:
                return (this.clearColor[0] / 255,
                        this.clearColor[1] / 255,
                        this.clearColor[2] / 255)

        material = intersect.sceneObj.material

        finalColor = [0, 0, 0]
        objectColor = [material.diffuse[0],
                       material.diffuse[1],
                       material.diffuse[2]]

        if material.matType == OPAQUE:
            for light in this.lights:
                diffuseColor = light.getDiffuseColor(intersect, this)
                specColor = light.getSpecColor(intersect, this)
                shadowIntensity = light.getShadowIntensity(intersect, this)

                lightColor = (mt.addVectors(
                    diffuseColor, specColor)) * (1 - shadowIntensity)
                finalColor = mt.addVectors(finalColor, lightColor)

        elif material.matType == REFLECTIVE:
            reflect = reflectVector(
                intersect.normal, [d * -1 for d in direction])
            reflectColor = this.cast_ray(
                intersect.point, reflect, intersect.sceneObj, recursion + 1)
            reflectColor = reflectColor

            specColor = [0, 0, 0]
            for light in this.lights:
                specColor = mt.addVectors(
                    specColor, light.getSpecColor(intersect, this))

            finalColor = mt.addVectors(reflectColor, specColor)

        elif material.matType == TRANSPARENT:
            outside = mt.dotMatrix(direction, intersect.normal) < 0
            bias = [x * 0.001 for x in intersect.normal]

            specColor = [0, 0, 0]
            for light in this.lights:
                specColor = mt.addVectors(
                    specColor, light.getSpecColor(intersect, this))

            reflect = reflectVector(
                intersect.normal, [d * -1 for d in direction])
            reflectOrig = mt.addVectors(
                intersect.point, bias) if outside else mt.subtractVectors(intersect.point, bias)
            reflectColor = this.cast_ray(
                reflectOrig, reflect, None, recursion + 1)
            reflectColor = reflectColor

            kr = fresnel(intersect.normal, direction, material.ior)

            refractColor = [0, 0, 0]
            if kr < 1:
                refract = refractVector(
                    intersect.normal, direction, material.ior)
                refractOrig = mt.subtractVectors(
                    intersect.point, bias) if outside else mt.addVectors(intersect.point, bias)
                refractColor = this.cast_ray(
                    refractOrig, refract, None, recursion + 1)
                refractColor = refractColor

            finalColor = mt.addVectors(
                [refC * float(kr) for refC in reflectColor], [rfK * (1 - kr) for rfK in refractColor])
            finalColor = mt.addVectors(finalColor, specColor)

        finalColor = mt.multVectors(finalColor, objectColor)

        if material.texture and intersect.texcoords:
            texColor = material.texture.getColor(
                intersect.texcoords[0], intersect.texcoords[1])
            if texColor is not None:
                finalColor = mt.multVectors(finalColor, texColor)

        r = min(1, finalColor[0])
        g = min(1, finalColor[1])
        b = min(1, finalColor[2])

        return (r, g, b)

    def glRender(this):

        t = math.tan((this.fov * np.pi / 180) / 2) * this.nearPlane
        r = t * this.viewportWidth / this.viewportHeight

        for y in range(this.viewportY, this.viewportY + this.viewportHeight + 1, STEPS):
            for x in range(this.viewportX, this.viewportX + this.viewportWidth + 1, STEPS):
                # Pasar de coordenadas de ventana a
                # coordenadas NDC (-1 a 1)
                Px = ((x + 0.5 - this.viewportX) / this.viewportWidth) * 2 - 1
                Py = ((y + 0.5 - this.viewportY) / this.viewportHeight) * 2 - 1
                Px *= r
                Py *= t

                directionection = V3(Px, Py, -this.nearPlane)
                directionection = [
                    d / mt.normL2(directionection) for d in directionection]

                rayColor = this.cast_ray(this.camPosition, directionection)

                if rayColor is not None:
                    rayColor = _color_(rayColor[0], rayColor[1], rayColor[2])
                    this.glPoint(x, y, rayColor)

    # Crea un archivo BMP

    def write(this, filename):
        with open(filename, "bw") as file:
            # pixel header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + this.width * this.height * 3))
            file.write(word(0))
            file.write(word(0))
            file.write(dword(14 + 40))

            # informacion del header
            file.write(dword(40))
            file.write(dword(this.width))
            file.write(dword(this.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(this.width * this.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # pixel data
            for y in range(this.height):
                for x in range(this.width):
                    file.write(this.framebuffer[x][y])
