# para la guía 2

import re
from itertools import product

N = 10  # longitud máxima a verificar

EJERCICIO_1 = {
    "a) longitud par": (
        r"([01][01])*",
        lambda s: len(s) % 2 == 0,
    ),
    "b) cantidad par de ceros": (
        r"1*(01*01*)*",
        lambda s: s.count("0") % 2 == 0,
    ),
    "c) par de ceros e impar de unos": (
        r"(00|11|(01|10)(00|11)*(01|10))*(1|(01|10)(00|11)*0)",
        lambda s: s.count("0") % 2 == 0 and s.count("1") % 2 == 1,
    ),
    "d) comienza con 00": (
        r"00[01]*",
        lambda s: s.startswith("00"),
    ),
    "e) termina con 00": (
        r"[01]*00",
        lambda s: s.endswith("00"),
    ),
    "f) comienza y/o termina con 00": (
        r"00[01]*|[01]*00",
        lambda s: s.startswith("00") or s.endswith("00"),
    ),
    "g) no contiene 00": (
        r"(1|01)*0?",
        lambda s: "00" not in s,
    ),
    "h) contiene 00": (
        r"[01]*00[01]*",
        lambda s: "00" in s,
    ),
}

TEXTO_C = "Hay 12 gatos, 7 perros y 105 peces."


def todas_las_cadenas(max_len):
    """Genera todas las cadenas sobre {0,1} de longitud 0..max_len (incluye ε = '')."""
    for n in range(max_len + 1):
        for t in product("01", repeat=n):
            yield "".join(t)


def verificar(patron, pertenece, max_len=N):
    """Devuelve la lista de cadenas donde la regex y la definición no coinciden."""
    errores = []
    for s in todas_las_cadenas(max_len):
        acepta = re.fullmatch(patron, s) is not None
        if acepta != pertenece(s):
            errores.append((s or "ε", acepta))
    return errores


def ejercicio_a():
    print(re.fullmatch(r"(00|1)*", "1001"))
    print(re.fullmatch(r"(00|1)*", "1010"))
    print(re.search(r"00", "1010011"))
    print(re.fullmatch(r"0*1?0*", "0010"))
    print(re.fullmatch(r"[01]*00", "1100"))


def ejercicio_b():
    for nombre, (patron, pertenece) in EJERCICIO_1.items():
        errores = verificar(patron, pertenece)
        estado = "OK" if not errores else f"FALLA en {errores[:5]}"
        print(f"{nombre:35} {patron:55} {estado}")

    # Ejemplos sueltos, para probar a mano
    print()
    for s in ["", "0", "00", "010", "1001", "0110"]:
        print(repr(s), "-> (g) no contiene 00:", bool(re.fullmatch(r"(1|01)*0?", s)))


def ejercicio_c(t=TEXTO_C):
    # 1) Todos los números enteros.
    #    \d  = un dígito (equivale a [0-9])
    #    +   = uno o más
    numeros = re.findall(r"\d+", t)
    print(numeros)                       # ['12', '7', '105']  (strings)
    print([int(n) for n in numeros])     # [12, 7, 105]        (enteros)

    # 2) Todas las palabras que terminan en s.
    #    \w  = un carácter de palabra (letra, dígito o _)
    #    \w* = cero o más de esos, y después la 's'
    #    \b  = borde de palabra: obliga a que la 's' sea la última letra
    palabras_s = re.findall(r"\b\w*s\b", t)
    print(palabras_s)                    # ['gatos', 'perros', 'peces']


if __name__ == "__main__":
    ejercicio_a()
    print()
    ejercicio_b()
    print()
    ejercicio_c()
