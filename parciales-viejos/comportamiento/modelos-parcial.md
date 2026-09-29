# Modelos de Parcial — Neurociencia y Comportamiento

> **Formato** (igual al simulacro): en el parcial caen **cuatro preguntas**, una por
> cada eje temático. Responder cada una en **entre uno y tres párrafos, no más**.
> Los ejes son: (1) Modelado computacional del comportamiento humano, (2) Aprendizaje,
> (3) Emociones, (4) Genética del comportamiento.
>
> Cada modelo trae las preguntas y, debajo, una **respuesta posible** a modo de guía.

---

## MODELO 1

### 1. Modelado computacional del comportamiento humano
En el artículo de Nature sobre profundidad de planificación en *Four-in-a-Row*, el modelo
predice tres tipos de datos observables en los humanos. ¿Cuáles son y qué componente del
modelo permite predecir cada uno?

**Respuesta posible.** El modelo predice tres cosas. Primero, las **elecciones** (jugadas)
de las personas: validado con validación cruzada 5-fold en partidas humano vs. humano,
predice las jugadas muy por encima del azar, gracias a la función de valor y al algoritmo de
búsqueda que arman la variación principal. Segundo, los **tiempos de respuesta**: el tamaño
del árbol de decisión construido por el algoritmo de búsqueda es predictor del tiempo de
respuesta observado (árboles más grandes, más tiempo). Tercero, los **movimientos
oculares**: la distribución de casillas que visita el algoritmo de búsqueda correlaciona con
la distribución de la atención visual de los jugadores (ρ ≈ 0,54). La conclusión central es
que los jugadores más fuertes planifican más profundamente y tienen menos lapsus
atencionales, sin evidencia de que mejore la calidad de la heurística (los pesos de las
features).

### 2. Aprendizaje
¿Cuáles son las tres condiciones que, según Darwin, deben cumplirse para que ocurra la
selección natural? Explique además por qué la teoría de Lamarck no requiere una de ellas.

**Respuesta posible.** Para que ocurra selección natural deben darse tres condiciones:
**variabilidad** (existen diferencias entre los rasgos de los individuos de una población),
**heredabilidad** (esas variaciones se heredan de padres a hijos) y **adaptabilidad**
(algunas de esas variaciones se adaptan mejor al ambiente, por lo que los individuos que las
poseen sobreviven y se reproducen más, dejando más descendencia). Sin variaciones previas
en la población, el proceso de selección no tiene sobre qué operar.

En la teoría de **Lamarck** los rasgos *adquiridos* durante la vida del individuo se
heredan a la descendencia; por eso no se necesita que existan variaciones previas en la
población al comienzo del proceso: la variación se genera durante la vida y se transmite. En
la de **Darwin**, en cambio, los rasgos adquiridos no se heredan, y las variaciones
preexistentes (y heredables) son la materia prima imprescindible de la selección natural.

### 3. Emociones
Mencionamos cuatro afirmaciones sobre las emociones en las que la psicología evolutiva sí
está de acuerdo. Enumérelas y explique brevemente la que vincula las emociones con la
interocepción.

**Respuesta posible.** Las cuatro afirmaciones son: (1) las emociones son el resultado del
**perfeccionamiento de dispositivos de supervivencia** a lo largo de la evolución de las
especies; (2) esos dispositivos usan las **mismas estructuras cerebrales y los mismos
neurotransmisores en todos los mamíferos**, incluido el ser humano; (3) esas estructuras
están vinculadas a **funciones básicas de regulación del equilibrio interno**, necesario para
la supervivencia; y (4) las emociones están íntimamente arraigadas en fenómenos sensitivos
viscerales corporales que llamamos **interocepción**.

Sobre la cuarta: la interocepción es la percepción de los estados viscerales del organismo
(pulsaciones, respiración, tensión, estado del estómago, etc.). Las emociones no son ajenas
al cuerpo, sino que están enraizadas en esas señales corporales. En la formulación extrema
de William James, "los cambios físicos que experimentamos ante una situación *son* las
emociones": la emoción no antecede a la reacción corporal, sino que en buena medida
consiste en ella.

### 4. Genética del comportamiento
Explique el método clásico de comparación entre gemelos y mellizos para estimar el
componente genético de un rasgo. ¿Qué lógica lo sustenta y cuál es su principal supuesto?

**Respuesta posible.** Los gemelos (monocigóticos) comparten prácticamente el 100 % de
sus alelos, mientras que los mellizos (dicigóticos) comparten en promedio la mitad. El
método compara la **correlación** de un rasgo entre pares de gemelos con la correlación
entre pares de mellizos (criados juntos y del mismo sexo). Si la similitud entre gemelos es
mayor que entre mellizos, se sospecha que el rasgo tiene un componente genético, porque la
única diferencia sistemática entre ambos tipos de pares es cuántos alelos comparten. En
fórmula: C_G = 2 × [Corr(gemelos) − Corr(mellizos)]; el componente del ambiente
compartido es C_AC = Corr(gemelos) − C_G, y el del ambiente no compartido es
C_ANC = 1 − C_G − C_AC.

El **supuesto clave** es que los ambientes que generan similitudes son los mismos para
gemelos que para mellizos ("equal environments assumption"). Si se viola, hay sesgos: si los
gemelos comparten ambientes más parecidos que los mellizos (por ejemplo por tener a
alguien idéntico en el mundo), el método **sobreestima** el componente genético; si los
ambientes intrauterinos son más similares entre mellizos que entre gemelos, lo
**subestima**.

---

## MODELO 2

### 1. Modelado computacional del comportamiento humano
Describa los tres componentes del modelo cognitivo del artículo de *Four-in-a-Row* y explique
cómo es la función de valor de los estados.

**Respuesta posible.** Los tres componentes son una **función de valor de los estados**, un
**algoritmo de búsqueda** y un **mecanismo de atención**. La función de valor asigna un
valor a cada estado del tablero como una **suma ponderada de atributos** (features): centro,
dos-en-línea conectado, dos-en-línea no conectado, tres-en-línea y cuatro-en-línea. Se
computa restando el valor de las features del oponente al de las features propias, y los pesos
del jugador que va a mover se multiplican por una constante de escala, para capturar que el
valor de una posición depende de quién juegue (un tres-en-línea puede ser victoria inmediata
o no según a quién le toque).

El **algoritmo de búsqueda** asume que ambos jugadores eligen la jugada que lleva al estado
de mayor valor; expande el árbol, evalúa las posiciones con la función de valor y **poda** las
ramas cuyo valor está por debajo del mejor menos un umbral, deteniéndose con cierta
probabilidad en cada iteración (distribución geométrica). El **mecanismo de atención**
modela la atención selectiva descartando aleatoriamente algunas features antes de construir el
árbol, agrega ruido gaussiano a los valores y contempla una tasa de lapsus (probabilidad de
jugar al azar). El resultado: los expertos planifican más profundo y tienen menos lapsus.

### 2. Aprendizaje
Distinga los conceptos de **rasgo adaptativo** y **subproducto**, y dé al menos un ejemplo de
cada uno (puede ser fisiológico o comportamental). ¿Qué es, además, el "ruido" en este
esquema?

**Respuesta posible.** Un **rasgo adaptativo (adaptación)** es un rasgo que aumentó el éxito
reproductivo del individuo, es decir, que fue una ventaja para la supervivencia y la
reproducción y por eso fue seleccionado. Un **subproducto (byproduct)** es una consecuencia
de un rasgo adaptativo que no aportó ventaja evolutiva propia: "viene de arrastre" con otro
rasgo que sí fue seleccionado.

Ejemplos fisiológicos: la **hemoglobina** (adaptación, porque permite transportar oxígeno) y
el **color rojo de la sangre** (subproducto, es sólo consecuencia del color de la hemoglobina);
también el cordón umbilical como adaptación y el ombligo como subproducto. Ejemplos
comportamentales: el **gusto por el azúcar**, el impulso sexual o el apego paterno-materno son
adaptaciones, mientras que las adicciones, el gusto por el fútbol o el sexo con anticonceptivos
son subproductos. El **ruido** es el tercer fruto de un proceso evolutivo: variación aleatoria
que no cumple ninguna función y que simplemente aparece sin haber sido seleccionada.

### 3. Emociones
¿Por qué a algunas emociones se las llama **básicas** (o primarias)? Dé dos ejemplos y
explique qué ventaja de supervivencia o reproducción se les atribuye.

**Respuesta posible.** Se las considera básicas por tres razones: aparecen desde **edades muy
tempranas** en todos los humanos (incluso en personas con ceguera y sordera congénitas), son
**universales** (se observan en todas las culturas, idea que ya proponía Darwin) y las podemos
**reconocer a partir de expresiones faciales universales**, comunes a todas las culturas e
independientes del aprendizaje cultural. Ejemplos de emociones básicas son el miedo, el asco,
la ira, la tristeza, la alegría y la sorpresa.

Dos ejemplos con su ventaja evolutiva: el **asco** nos protege de ingerir sustancias
potencialmente tóxicas o en mal estado (venenos, comida podrida), reduciendo el riesgo de
intoxicación; el **miedo** activa el organismo para pelear o huir ante una amenaza (respuesta
de lucha o huida), preparando al cuerpo para responder a situaciones peligrosas. En ambos
casos son "dispositivos de supervivencia" que aumentaron la probabilidad de sobrevivir y
dejar descendencia.

### 4. Genética del comportamiento
Defina el **componente genético** de un rasgo de manera rigurosa. Al estudiar el componente
ambiental, ¿en qué dos grandes grupos se dividen las variables y cómo se distingue uno de
otro?

**Respuesta posible.** El **componente genético (C_G)** de un rasgo es la proporción de la
variación total del rasgo entre individuos que se explica por las variaciones en sus genes:
C_G = V_G / (V_G + V_A) = V_G / V_T, donde V_G es la varianza genética y V_A la ambiental.
El componente ambiental es el porcentaje de la variación total explicado por los ambientes de
desarrollo; por definición, componente genético más componente ambiental suman 100 %. Es
crucial recordar que el componente genético **vale para una población dada en un momento
dado del tiempo**: no es una propiedad fija del rasgo.

Al estudiar el componente ambiental se dividen las variables en dos grupos. Las **variables
del ambiente compartido** son todo lo que no es genético y hace que los miembros de una
familia se parezcan: lo que comparten dos hermanos criados juntos pero no dos separados al
nacer (clase social, estilo parental, barrio de crianza). Las **variables del ambiente no
compartido** son todo lo que no es genético ni se comparte entre miembros de una familia,
ligado a la experiencia particular de cada individuo. En fórmula: V_A = V_AC + V_ANC.

---

## MODELO 3

### 1. Modelado computacional del comportamiento humano
Según el artículo, ¿en qué se diferencian los expertos de los novatos? Discuta la relación
entre "planificar más profundo" y la idea de velocidad de procesamiento / reconocimiento de
patrones.

**Respuesta posible.** El hallazgo central es que los jugadores más fuertes **planifican más
profundamente** (exploran más pasos a futuro en el árbol de decisión) y cometen **menos
lapsus atencionales** (menos jugadas al azar y menos features olvidadas). En cambio, **no**
hay evidencia de que mejore la calidad de la heurística: los pesos que asignan a las distintas
features del tablero son similares entre expertos y novatos. Es decir, lo que distingue al
experto no es "valorar mejor" cada posición, sino buscar más lejos y con menos ruido.

La literatura suele explicar la superioridad del experto por mejor **reconocimiento de
patrones** y/o búsqueda más profunda. Los autores vinculan "planificar más profundo" con
mayor **velocidad de procesamiento**: los expertos afinan su representación de las features
relevantes, lo que les permite hacer más evaluaciones por unidad de tiempo y por lo tanto
explorar el árbol más profundamente en el mismo lapso. Esto es consistente con un mejor
reconocimiento de patrones (representaciones más eficientes), pero pone el foco en un factor
frecuentemente subestimado: la velocidad de procesamiento.

### 2. Aprendizaje
En clase vimos experimentos con bebés (y fetos) humanos que muestran la existencia de
*priors* que llevan a comportamientos instintivos. Relate dos de esos experimentos e indique
qué prior demuestra cada uno. ¿Para qué sirven estos priors?

**Respuesta posible.** Un experimento iluminó el vientre de embarazadas con **tres puntos de
luz (láseres)**. Cuando la disposición se parecía a un rostro —dos puntos arriba como ojos y
uno abajo como nariz—, los fetos giraban la cabeza hacia la luz con más frecuencia que
cuando la disposición estaba invertida. Esto muestra un **prior de preferencia por las caras**,
presente incluso antes de nacer. En otro tipo de experimentos, bebés de pocos meses miran
más tiempo (muestran sorpresa) ante **eventos físicamente imposibles**, como una caja que
parece flotar en el aire, lo que evidencia un prior que les hace inferir leyes básicas de la
naturaleza (los objetos no flotan, caen).

Otros priors vistos: detección rápida de amenazas (encontramos víboras más rápido que
flores), intuición numérica y probabilística, y razonamiento lógico pre-verbal. Estos
comportamientos son **instintivos**: aparecen en humanos típicos con desarrollo típico, fueron
seleccionados a lo largo de la evolución y sirven de **andamiaje para aprendizajes más
complejos** (por ejemplo, la atención innata al habla facilita el aprendizaje del lenguaje). El
cerebro no es una *tabula rasa*: lo innato y lo adquirido se combinan.

### 3. Emociones
Desde la neurociencia de la regulación emocional, explique el rol del **sistema nervioso
autónomo** (simpático y parasimpático) y en qué consiste la "receta" para una vida larga y
buena según ese enfoque.

**Respuesta posible.** El sistema nervioso autónomo (la parte "reptiliana", involuntaria) tiene
dos ramas. La rama **simpática (SNS)** prepara al cuerpo para la acción: estrés, atención,
lucha o huida (dilata pupilas, acelera pulsaciones, libera glucosa). La rama **parasimpática
(PNS)** se encarga del descanso, la relajación, la digestión y la recuperación, y **calma** la
activación del SNS y del eje hipotalámico-hipofisario-adrenal (HPAA). El sufrimiento
crónico se asocia a una **sobreactivación del simpático**, donde sensaciones corporales y
pensamientos negativos se retroalimentan (los "segundos dardos": los pensamientos que
agregamos a un dolor inevitable). En el marco de las terapias cognitivo-conductuales,
Dolor → Sufrimiento está mediado por el pensamiento "terribilizador".

La **receta** con mejores probabilidades para una vida larga y buena es mantener una
activación basal predominantemente **parasimpática**, con una leve activación simpática para
la vitalidad, y sólo **picos ocasionales** del simpático ante grandes oportunidades o
amenazas reales. La regulación emocional se entiende entonces como la técnica de "mantener
a raya" el sistema autónomo: cada vez que uno calma el ANS estimulando el parasimpático,
orienta cuerpo y mente hacia el bienestar y, con la repetición, construye estructura neuronal
(como plantea Sapolsky en *¿Por qué las cebras no tienen úlcera?*, el estrés psicológico
crónico, exclusivo de los humanos, genera enfermedad).

### 4. Genética del comportamiento
¿Qué es una **correlación genotipo-ambiente**? Describa sus tres tipos (pasiva, evocativa y
activa) con un ejemplo de cada uno, y explique por qué esto complica la interpretación causal
de estudios que correlacionan ambientes con rasgos.

**Respuesta posible.** Una **correlación genotipo-ambiente** ocurre porque los **genes
influyen sobre los ambientes** a los que un individuo queda expuesto: no sólo genes y
ambientes influyen sobre los rasgos, sino que los genes moldean el propio ambiente. Hay tres
tipos. **Pasiva**: el niño recibe de sus padres genes que correlacionan con el ambiente que
esos mismos padres crean (p. ej., si unos alelos predisponen a la lectura, es probable que los
padres tengan esos alelos y por eso haya más libros en la casa). **Evocativa**: el niño es
tratado según sus propensiones genéticas (un chico con facilidad para los números recibe más
regalos con números). **Activa**: el niño busca y crea activamente ambientes acordes a sus
propensiones (ese mismo chico elige juguetes con números).

Esto complica la interpretación causal porque una correlación observada entre un ambiente y
un rasgo puede estar **mediada por la genética** y no ser causal. Ejemplo del curso: se observa
que en familias donde los padres incentivan la curiosidad los hijos son más curiosos; pero
esto **no es evidencia causal**, porque puede tratarse de una correlación pasiva (los hijos
heredan las propensiones de los padres y a la vez los padres moldean el ambiente). Un caso
real: la asociación entre abandono paterno / tabaquismo materno en el embarazo y depresión
de los hijos desaparece al controlar por el puntaje poligénico de los padres, lo que sugiere
una correlación genotipo-ambiente pasiva y no una relación causal directa.

---

## BANCO DE PREGUNTAS EXTRA (para practicar)

**Modelado computacional**
- ¿Por qué *Four-in-a-Row* es un buen juego para medir profundidad de planificación y el
  ajedrez no? (tratabilidad computacional, reglas simples, novedad, complejidad suficiente
  para distinguir expertos de novatos).
- ¿Qué es la "variación principal" en el árbol de decisión y cómo funciona la poda?
- Hipótesis de implementación neural del modelo: ¿qué región se asocia a cada componente?
  (función de valor → corteza orbitofrontal; búsqueda → prefrontal, cíngulo, hipocampo;
  atención → red frontoparietal).

**Aprendizaje**
- ¿Qué es la **teoría de la carga cognitiva** y qué nos hace expertos según ella? (la memoria
  de trabajo es un cuello de botella por su baja capacidad y durabilidad; la memoria de largo
  plazo, de capacidad casi ilimitada, es la que nos hace pensar mejor y no puede sustituirse
  por el acceso rápido a información externa como Google o una IA).
- Las tres etapas de todo aprendizaje: adquisición, fluidez y generalización (más
  mantenimiento). Describa cada una.
- Los cuatro pilares del aprendizaje de Dehaene: atención, feedback (¡y regresión a la
  media!), motivación (intrínseca vs. extrínseca) y consolidación.
- Explique la **regresión a la media** y por qué genera la ilusión de que castigar mejora y
  premiar empeora.
- ¿Qué relación hay entre la estructura del cerebro (hiperparámetros) seleccionada por
  evolución y el *fine tuning* durante la vida?

**Emociones**
- Diferencia entre **emoción** y **sentimiento** (los sentimientos se asocian más a lo
  cognitivo y duran más en el tiempo).
- ¿Qué son los "segundos dardos" y cómo se relacionan Dolor y Sufrimiento?
- ¿Por qué "las cebras no tienen úlcera"? (el estrés animal es agudo y puntual; el humano
  inventa estresores psicológicos crónicos que enferman).

**Genética del comportamiento**
- Diferencia entre las dos definiciones de "rasgo genético": la de la psicología evolutiva (lo
  que todos tenemos en común, p. ej. aprender un lenguaje) y la de la genética del
  comportamiento (lo que nos hace diferentes, las variaciones individuales).
- Método clásico con **hijos adoptivos**: comparar correlación padres-hijos biológicos vs.
  padres-hijos adoptivos. ¿Qué estima cada comparación? Problemas: colocación selectiva,
  ambiente intrauterino, generalización.
- ¿Qué es un **puntaje poligénico** y qué es la **heredabilidad faltante**?
- ¿Qué es la **interacción genotipo-ambiente** (distinta de la correlación)? Ejemplo del
  estudio de maltrato infantil y TDAH: las rectas paralelas indican que **no** hay interacción
  (el maltrato aumenta síntomas independientemente del puntaje poligénico).
- Componente genético de rasgos concretos: autismo ~80 %, esquizofrenia ~50 %, depresión
  ~37–48 %, IMC ~40–80 %, zurdera ~25 %, extroversión ~37 %.
