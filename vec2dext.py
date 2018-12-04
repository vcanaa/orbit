from pymunk.vec2d import Vec2d

def tupleV(v):
  return (v.x, v.y)


def copyV(v):
  return Vec2d(v.x, v.y)


def multV(v, r):
  return Vec2d(v.x * r, v.y * r)


setattr(Vec2d, "tuple", tupleV)
setattr(Vec2d, "copy", copyV)
setattr(Vec2d, "mult", multV)