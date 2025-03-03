from ctypes import Structure, c_int, c_float
from ctypes import POINTER as _P
from .dll import _bind, SDLFunc, AttributeDict
from .stdinc import SDL_bool

__all__ = [
    # Structs
    "SDL_Point", "SDL_FPoint", "SDL_Rect", "SDL_FRect",

    # Macro Functions
    "SDL_PointInRect", "SDL_RectEmpty", "SDL_RectEquals",
]


# Struct definitions

class SDL_Point(Structure):
    _fields_ = [("x", c_int), ("y", c_int)]

    def __init__(self, x=0, y=0):
        super(SDL_Point, self).__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        return "SDL_Point(x=%d, y=%d)" % (self.x, self.y)

    def __copy__(self):
        return SDL_Point(self.x, self.y)

    def __deepcopy__(self, memo):
        return SDL_Point(self.x, self.y)

    def __eq__(self, pt):
        return self.x == pt.x and self.y == pt.y

    def __ne__(self, pt):
        return self.x != pt.x or self.y != pt.y


class SDL_FPoint(Structure):
    _fields_ = [("x", c_float), ("y", c_float)]

    def __init__(self, x=0.0, y=0.0):
        super(SDL_FPoint, self).__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        return "SDL_FPoint(x=%.3f, y=%.3f)" % (self.x, self.y)

    def __copy__(self):
        return SDL_FPoint(self.x, self.y)

    def __deepcopy__(self, memo):
        return SDL_FPoint(self.x, self.y)

    def __eq__(self, pt):
        return self.x == pt.x and self.y == pt.y

    def __ne__(self, pt):
        return self.x != pt.x or self.y != pt.y


class SDL_Rect(Structure):
    _fields_ = [
        ("x", c_int),
        ("y", c_int),
        ("w", c_int),
        ("h", c_int)
    ]

    def __init__(self, x=0, y=0, w=0, h=0):
        super(SDL_Rect, self).__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return "SDL_Rect(x=%d, y=%d, w=%d, h=%d)" % (self.x, self.y, self.w,
                                                     self.h)

    def __copy__(self):
        return SDL_Rect(self.x, self.y, self.w, self.h)

    def __deepcopy__(self, memo):
        return SDL_Rect(self.x, self.y, self.w, self.h)

    def __eq__(self, rt):
        origin_equal = self.x == rt.x and self.y == rt.y
        size_equal = self.w == rt.w and self.h == rt.h
        return origin_equal and size_equal

    def __ne__(self, rt):
        origin_equal = self.x == rt.x and self.y == rt.y
        size_equal = self.w == rt.w and self.h == rt.h
        return not (origin_equal and size_equal)


class SDL_FRect(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("w", c_float),
        ("h", c_float)
    ]

    def __init__(self, x=0.0, y=0.0, w=0.0, h=0.0):
        super(SDL_FRect, self).__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        dims = (self.x, self.y, self.w, self.h)
        return "SDL_FRect(x=%.3f, y=%.3f, w=%.3f, h=%.3f)" % dims

    def __copy__(self):
        return SDL_FRect(self.x, self.y, self.w, self.h)

    def __deepcopy__(self, memo):
        return SDL_FRect(self.x, self.y, self.w, self.h)

    def __eq__(self, rt):
        origin_equal = self.x == rt.x and self.y == rt.y
        size_equal = self.w == rt.w and self.h == rt.h
        return origin_equal and size_equal

    def __ne__(self, rt):
        origin_equal = self.x == rt.x and self.y == rt.y
        size_equal = self.w == rt.w and self.h == rt.h
        return not (origin_equal and size_equal)


# Macro & inline functions

def SDL_RectEmpty(x):
    return (not x) or (x.w <= 0) or (x.h <= 0)

def SDL_RectEquals(a, b):
    return (a.x == b.x) and (a.y == b.y) and (a.w == b.w) and (a.h == b.h)

def SDL_PointInRect(p, r):
    return (p.x >= r.x) and (p.x < (r.x+r.w)) and (p.y >= r.y) and (p.y < (r.y+r.h))


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("SDL_HasIntersection", [_P(SDL_Rect), _P(SDL_Rect)], SDL_bool),
    SDLFunc("SDL_IntersectRect", [_P(SDL_Rect), _P(SDL_Rect), _P(SDL_Rect)], SDL_bool),
    SDLFunc("SDL_UnionRect", [_P(SDL_Rect), _P(SDL_Rect), _P(SDL_Rect)]),
    SDLFunc("SDL_EnclosePoints", [_P(SDL_Point), c_int, _P(SDL_Rect), _P(SDL_Rect)], SDL_bool),
    SDLFunc("SDL_IntersectRectAndLine",
        [_P(SDL_Rect), _P(c_int), _P(c_int), _P(c_int), _P(c_int)],
        returns = SDL_bool
    ),
]
_ctypes = AttributeDict()
for f in _funcdefs:
    _ctypes[f.name] = _bind(f.name, f.args, f.returns, f.added)
    __all__.append(f.name) # Add all bound functions to module namespace


# Aliases for ctypes bindings

SDL_HasIntersection = _ctypes["SDL_HasIntersection"]
SDL_IntersectRect = _ctypes["SDL_IntersectRect"]
SDL_UnionRect = _ctypes["SDL_UnionRect"]
SDL_EnclosePoints = _ctypes["SDL_EnclosePoints"]
SDL_IntersectRectAndLine = _ctypes["SDL_IntersectRectAndLine"]
