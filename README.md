# Inteligencia Artificial y Neurociencias

Materiales, apuntes y trabajos prácticos de la materia **Inteligencia Artificial y Neurociencias** (Universidad Torcuato Di Tella, segundo semestre de 2026).

El curso explora la convergencia entre la Inteligencia Artificial y las Neurociencias, abordando temas como el lenguaje, el comportamiento, la memoria, el razonamiento y el aprendizaje desde perspectivas humana y computacional. Cada tema incluye un análisis histórico, una revisión del estado actual y una mirada prospectiva.

**Profesores:** Agustín Gravano, Andrés Rieznik
**Auxiliares:** Gerardo Del Toro, Antonella Giordano Furchi

## Programa

- Reseña histórica de la IA y la Neurociencia Cognitiva.
- **Aprendizaje por refuerzo:** bandidos de *k* brazos, exploración vs. explotación, procesos de decisión de Markov, métodos Monte Carlo, diferencias temporales (SARSA, Q-Learning), aproximación de funciones de valor, gradiente de políticas.
- **Aprendizaje humano vs. de máquinas:** condicionamiento clásico y operante, plasticidad, reciclaje neuronal, principio de Hebb, algoritmos genéticos, tabla rasa vs. módulos cerebrales.
- **Priors del comportamiento humano:** sesgos que permiten el aprendizaje, sistema de recompensa y motivación.
- **Modelado computacional del comportamiento:** pacientes *split brain*, ceguera a la elección, metacognición, emociones y toma de decisiones.
- **Genética del comportamiento:** componentes ambientales y genéticos, métodos de estimación, correlación e interacción genotipo–ambiente.
- **Teoría de lenguajes:** expresiones regulares, gramáticas regulares y libres de contexto, árboles de *parsing*, jerarquía de Chomsky, gramáticas probabilísticas.
- **Procesamiento del lenguaje natural:** modelos de lenguaje, GLCP, *n*-gramas, LLMs, Transformers, *scaling laws*, *fine tuning* (LoRA), alineación (RLHF), RAG, razonamiento (*chain-of-thought*).
- **Lenguaje humano:** definiciones y componentes, anatomía y desarrollo del lenguaje en el cerebro, genes del lenguaje.
- **Teorías de la conciencia:** espacio global de trabajo, información integrada, teoría estadística.
- **Teorías y axiomas morales:** utilitarismo, deontología, contractualismo, la unificación de Parfit.

## Evaluación

Dos exámenes parciales individuales y entre dos y cuatro trabajos prácticos (individuales y/o grupales). Todas las instancias se puntúan de 0 a 100.

- Se aprueba con **60 o más** en cada parcial. Cada parcial tiene su propio recuperatorio al final del semestre; pueden recuperarse ambos.
- Quien aprobó un parcial y rinde el recuperatorio para mejorar debe saber que **la nota del recuperatorio es la definitiva**.
- Los trabajos prácticos son de entrega y aprobación **opcional** y no tienen recuperatorio.

**Cálculo del puntaje total** (con ambos parciales aprobados):

```
Total = P1 × 0,4 + P2 × 0,4 + TPs × 0,2
```

donde `TPs` es el promedio de los trabajos prácticos (un TP no entregado cuenta como 0).

| Rango numérico | Nota final |
|----------------|:----------:|
| (90, 100]      | A          |
| (80, 90]       | A−         |
| (72, 80]       | B+         |
| (66, 72]       | B          |
| (60, 66]       | B−         |
| (54, 60]       | C+         |
| [48, 54]       | C          |

## Bibliografía

### Libros y textos

- Sutton, R. & Barto, A. (2018). *Reinforcement Learning: An Introduction* (2ª ed.). MIT Press. *(disponible en Biblioteca)*
- Gazzaniga, M. S., Heatherton, T. F. & Halpern, D. F. (2018). *Psychological Science*. W. W. Norton.
- Biswas-Diener, R. & Diener, E. (2016). *Introduction to Psychology: The Full Noba Collection*.
- Plomin, R. (2008). *Behavioral Genetics*. Macmillan.
- Pinker, S. (2012). *La lingüística como una ventana para comprender el cerebro*. Transcripción del video disponible en el campus.
- Dubey, R., Agrawal, P., Pathak, D., Griffiths, T. L. & Efros, A. A. (2018). *Investigating human priors for playing video games*. arXiv:1802.10217.
- Blackmore, S. & Troscianko, E. T. (2024). *Consciousness: An Introduction*. Routledge.
- Hopcroft, J., Motwani, R. & Ullman, J. (2006). *Introduction to Automata Theory, Languages and Computation* (3ª ed.). Pearson. *(disponible en Biblioteca; capítulos 3 y 5 en PDF en Materiales; capítulo 9 de la 1ª edición también disponible)*
- Jurafsky, D. & Martin, J. (2024). *Speech and Language Processing* (3ª ed., borrador). https://web.stanford.edu/~jurafsky/slp3/
- Franco Luque, F. (2021). El lenguaje natural como lenguaje formal. *Anales de Lingüística*, 2(7), 59–87.

### Papers de LLMs

- Vaswani et al. (2017). Attention is all you need. *NeurIPS*, 30. arXiv:1706.03762.
- Devlin et al. (2018). BERT: Pre-training of deep bidirectional transformers for language understanding. arXiv:1810.04805.
- Radford et al. (2018). Improving language understanding by generative pre-training. OpenAI.
- Belkin et al. (2019). Reconciling modern machine-learning practice and the classical bias–variance trade-off. *PNAS*, 116(32).
- Kaplan et al. (2020). Scaling laws for neural language models. arXiv:2001.08361.
- Hoffmann et al. (2022). Training compute-optimal large language models. arXiv:2203.15556.
- Hu et al. (2021). LoRA: Low-rank adaptation of large language models. arXiv:2106.09685. (ICLR 2022).
- Ouyang et al. (2022). Training language models to follow instructions with human feedback. arXiv:2203.02155.
- Wei et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS*, 35. arXiv:2201.11903.
- Lewis et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS*, 33. arXiv:2005.11401.

## Estructura del repositorio

```
.
├── apuntes/        # Notas y resúmenes por unidad
├── practicos/      # Trabajos prácticos
├── material/       # PDFs y recursos del campus
└── README.md
```

> La bibliografía completa está disponible en el campus virtual de la materia.
