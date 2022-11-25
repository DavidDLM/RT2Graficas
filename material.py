# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso

white = (1, 1, 1)
black = (0, 0, 0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Material(object):
    def __init__(this, diffuse=white, spec=1.0, ior=1.0, texture=None, matType=OPAQUE):
        this.diffuse = diffuse
        this.spec = spec
        this.ior = ior
        this.texture = texture
        this.matType = matType
