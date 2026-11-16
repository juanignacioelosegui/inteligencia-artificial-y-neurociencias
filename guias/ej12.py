import nltk


def parsear(gramatica, cadena, mostrar=True):
    """Parsea `cadena` (un string; cada carácter es un terminal) y devuelve la lista de árboles.

    Si la cadena tiene un símbolo que no es terminal de la gramática,
    NLTK lanza ValueError: lo atrapamos y devolvemos [] (no hay árbol).
    """
    parser = nltk.ChartParser(gramatica)
    try:
        arboles = list(parser.parse(list(cadena)))
    except ValueError as e:
        print(f"  {cadena!r}: símbolo fuera del alfabeto -> {e}")
        return []
    print(f"  {cadena!r}: {len(arboles)} árbol(es)")
    if mostrar:
        for arbol in arboles:
            print("   ", arbol)          # forma con paréntesis: más fácil de leer
            arbol.pretty_print()
    return arboles


# ---------------------------------------------------------------- (a)
print("=== 12(a) ===")
G_a = nltk.CFG.fromstring("""
    S -> 'a' S 'b' | 'a' 'b'
""")
for c in ["aaabbb", "aabbb", "aacbb"]:
    parsear(G_a, c)


# ---------------------------------------------------------------- (b)
print("=== 12(b) gramática ambigua ===")
G_amb = nltk.CFG.fromstring("""
    E -> E '+' E | E '*' E | '(' E ')' | 'x'
""")
parsear(G_amb, "x+x*x")
# Un árbol tiene el '+' en la raíz      -> corresponde a x+(x*x)
# El otro tiene el '*' en la raíz       -> corresponde a (x+x)*x

print("=== 12(b) gramática no ambigua (E, T, F) ===")
# E: sumas, T: productos (términos), F: factores (x o paréntesis).
# '*' queda más abajo en el árbol que '+', así que se evalúa antes.
G_prec = nltk.CFG.fromstring("""
    E -> E '+' T | T
    T -> T '*' F | F
    F -> '(' E ')' | 'x'
""")
parsear(G_prec, "x+x*x")       # un único árbol, con '+' en la raíz
parsear(G_prec, "(x+x)*x")     # con paréntesis, el '*' queda en la raíz


# ---------------------------------------------------------------- (c)
print("=== 12(c) lógica proposicional (gramática del Ej. 10) ===")
# 'F' (entre comillas) es el terminal Falso; el no terminal se llama S.
G_logica = nltk.CFG.fromstring("""
    S -> 'V' | 'F' | 'p' | 'q' | 'r' | 's'
    S -> '¬' S
    S -> '(' S '∧' S ')' | '(' S '∨' S ')'
""")

print("Válidas:")
for c in ["p", "¬(p∧q)", "((p∨q)∧¬V)"]:
    parsear(G_logica, c)

print("Inválidas:")
for c in [
    "p∧q",   # falta el paréntesis: ∧ solo aparece dentro de '(' S '∧' S ')'
    "(p)",   # ninguna regla pone paréntesis alrededor de una fórmula sola
    "p¬",    # '¬' siempre va ANTES de la fórmula, nunca después
]:
    parsear(G_logica, c)


# ---------------------------------------------------------------- (d) opcional
print("=== 12(d) S -> S S | 'a' ===")
G_d = nltk.CFG.fromstring("""
    S -> S S | 'a'
""")
parser_d = nltk.ChartParser(G_d)
cantidades = [len(list(parser_d.parse(list("a" * k)))) for k in range(1, 8)]
print("  árboles para a^1 ... a^7:", cantidades)   # números de Catalan

