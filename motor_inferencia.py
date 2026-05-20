import unicodedata
import re
from base_conocimiento import METODOLOGIAS, PALABRAS_CLAVE, REGLAS_INTENCION


def clasificar_entrada_usuario(texto_usuario):
    texto = normalizar_texto(texto_usuario)

    saludos = [
        "hola", "buenas", "buenos dias", "buenas tardes",
        "buenas noches", "hey", "que tal", "saludos", "keloke", 
        "holi", "holis", "holaa", "holaaa", "hi", "hello"
    ]

    despedidas = [
        "adios", "bye", "hasta luego", "nos vemos", "gracias", 
        "muchas gracias", "gracias por tu ayuda", "gracias por la ayuda", "gracias por tu asesoría",
    ]

    ayuda = [
        "ayuda", "ejemplo", "ejemplos", "como escribo",
        "que pongo", "que debo poner", "no se que poner"
    ]

    if texto in saludos or any(texto.startswith(saludo) for saludo in saludos):
        return "saludo"

    if texto in despedidas or any(texto.startswith(despedida) for despedida in despedidas):
        return "despedida"

    if any(palabra in texto for palabra in ayuda):
        return "ayuda"

    palabras = texto.split()

    if len(palabras) < 6:
        return "insuficiente"

    return "descripcion"

def responder_modo_libre(texto_usuario):

    tipo = clasificar_entrada_usuario(texto_usuario)

    if tipo == "saludo":
        return {
            "tipo": "mensaje",
            "respuesta": (
                "¡Hola! Soy tu asistente experto en metodologías de desarrollo. "
                "Descríbeme tu proyecto y te ayudaré a elegir una metodología adecuada."
            )
        }

    if tipo == "despedida":
        return {
            "tipo": "mensaje",
            "respuesta": (
                "Cuando quieras puedes describirme otro proyecto "
                "y volveré a analizarlo, Hasta Luego!!"
            )
        }

    if tipo == "ayuda":
        return {
            "tipo": "mensaje",
            "respuesta": (
                "Puedes describir tu proyecto mencionando aspectos como:\n\n"
                "• Tamaño del proyecto\n"
                "• Si los requisitos pueden cambiar\n"
                "• Participación del cliente\n"
                "• Tiempo de entrega\n"
                "• Nivel de riesgo\n"
                "• Necesidad de documentación\n"
                "• Calidad del código o pruebas\n\n"
                "Ejemplo:\n"
                "Estoy desarrollando una app pequeña, el cliente quiere ver avances, "
                "puede haber cambios y necesitamos entregas rápidas."
            )
        }

    if tipo == "insuficiente":
        return {
            "tipo": "mensaje",
            "respuesta": (
                "Necesito un poco más de información para darte una recomendación. "
                "Por ejemplo, dime si el proyecto es grande o pequeño, si habrá cambios, "
                "si el cliente participará, si hay poco tiempo o si requiere documentación."
            )
        }

    contradicciones = detectar_contradicciones(texto_usuario)

    if contradicciones:
        texto_contradicciones = "Detecté información contradictoria en tu descripción.\n\n"
        texto_contradicciones += "Antes de recomendar una metodología, aclara lo siguiente:\n\n"

        for contradiccion in contradicciones:
            texto_contradicciones += f"• {contradiccion}\n"

        texto_contradicciones += (
            "\nPuedes volver a escribir la descripción del proyecto corrigiendo esos puntos."
        )

        return {
            "tipo": "mensaje",
            "respuesta": texto_contradicciones
        }

    resultado = recomendar_por_texto(texto_usuario)
    return {
        "tipo": "resultado",
        "resultado": resultado
    }

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def detectar_contradicciones(texto_usuario):
    texto = normalizar_texto(texto_usuario)

    contradicciones = []

    reglas_contradiccion = {
        "participacion_cliente": {
            "positivas": [
                "cliente participa",
                "cliente participara",
                "cliente involucrado",
                "cliente activo",
                "cliente revisa",
                "cliente quiere revisar",
                "ver avances",
                "retroalimentacion",
                "feedback"
            ],
            "negativas": [
                "cliente no participa",
                "cliente no participara",
                "sin participacion del cliente",
                "sin que el cliente participe",
                "poca participacion del cliente",
                "el cliente no estara involucrado"
            ],
            "mensaje": "Aclarar si el cliente participará activamente o no en el proyecto."
        },

        "cambios_requisitos": {
            "positivas": [
                "requisitos pueden cambiar",
                "pueden cambiar",
                "cambios frecuentes",
                "cambiar requisitos",
                "modificar requisitos",
                "cliente puede pedir cambios",
                "ajustes durante el desarrollo"
            ],
            "negativas": [
                "no habra cambios",
                "no hay cambios",
                "sin cambios",
                "requisitos estables",
                "requisitos definidos",
                "requisitos no cambian"
            ],
            "mensaje": "Aclarar si los requisitos pueden cambiar o si permanecerán estables."
        },

        "documentacion": {
            "positivas": [
                "documentacion formal",
                "documentacion extensa",
                "documentar todo",
                "mucha documentacion",
                "manuales",
                "reportes",
                "evidencia"
            ],
            "negativas": [
                "sin documentacion",
                "no necesito documentacion",
                "no se necesita documentacion",
                "poca documentacion",
                "no quiero documentar",
                "no documentar"
            ],
            "mensaje": "Aclarar si el proyecto requiere documentación formal o no."
        },

        "riesgo": {
            "positivas": [
                "alto riesgo",
                "riesgo tecnico",
                "tecnologia nueva",
                "incertidumbre",
                "falta de experiencia",
                "no dominamos",
                "dificultad tecnica"
            ],
            "negativas": [
                "sin riesgo",
                "no hay riesgo",
                "bajo riesgo",
                "poco riesgo",
                "tecnologia conocida",
                "tenemos experiencia"
            ],
            "mensaje": "Aclarar si el proyecto presenta riesgo técnico o si el riesgo es bajo."
        },

        "rapidez": {
            "positivas": [
                "rapido",
                "urgente",
                "poco tiempo",
                "entregas rapidas",
                "tiempo limitado",
                "fecha estricta",
                "entregar pronto"
            ],
            "negativas": [
                "no es urgente",
                "sin prisa",
                "no necesitamos rapidez",
                "tenemos tiempo",
                "fecha flexible",
                "sin limite de tiempo"
            ],
            "mensaje": "Aclarar si el proyecto requiere entregas rápidas o si el tiempo es flexible."
        },

        "tamano_proyecto": {
            "positivas": [
                "proyecto grande",
                "sistema grande",
                "gran escala",
                "empresa grande",
                "muchos usuarios",
                "complejo"
            ],
            "negativas": [
                "proyecto pequeno",
                "app pequena",
                "sistema pequeno",
                "simple",
                "sencillo",
                "poco alcance"
            ],
            "mensaje": "Aclarar si el proyecto es grande/complexo o pequeño/sencillo."
        }
    }

    for categoria, regla in reglas_contradiccion.items():
        hay_positiva = any(frase in texto for frase in regla["positivas"])
        hay_negativa = any(frase in texto for frase in regla["negativas"])

        if hay_positiva and hay_negativa:
            contradicciones.append(regla["mensaje"])

    return contradicciones

def detectar_condiciones(texto_usuario):
    texto = normalizar_texto(texto_usuario)

    condiciones = {
        "requisitos_cambian": "no",
        "requisitos_estables": "no",
        "cliente_participa": "no",
        "entregas_rapidas": "no",
        "flujo_continuo": "no",
        "alta_calidad": "no",
        "proyecto_grande": "no",
        "proyecto_pequeno": "no",
        "alto_riesgo": "no",
        "documentacion": "no",
        "tiempo_estricto": "no",
        "optimizacion": "no",
        "modularidad": "no",
        "prototipo": "no",
        "varios_equipos": "no",
        "escala_empresarial": "no",
    }

    condiciones_detectadas = []

    frases_negativas_por_condicion = {
        "cliente_participa": [
            "cliente no participa",
            "cliente no participara",
            "sin que el cliente participe",
            "sin participacion del cliente",
            "poca participacion del cliente"
        ],
        "requisitos_cambian": [
            "no habra cambios",
            "no hay cambios",
            "sin cambios",
            "requisitos no cambian"
        ],
        "documentacion": [
            "no necesita documentacion",
            "no se necesita documentacion",
            "sin documentacion",
            "poca documentacion"
        ],
        "alto_riesgo": [
            "no hay riesgo",
            "sin riesgo",
            "bajo riesgo",
            "poco riesgo"
        ],
        "entregas_rapidas": [
            "no es urgente",
            "sin prisa",
            "no necesitamos rapidez"
        ]
    }

    # Primero detecta negaciones claras
    for condicion, frases in frases_negativas_por_condicion.items():
        for frase in frases:
            if frase in texto:
                condiciones[condicion] = "no"

    # Luego detecta palabras clave positivas
    for condicion, palabras in PALABRAS_CLAVE.items():
        negada = False

        if condicion in frases_negativas_por_condicion:
            for frase in frases_negativas_por_condicion[condicion]:
                if frase in texto:
                    negada = True
                    break

        if negada:
            continue

        for palabra in palabras:
            palabra_normalizada = normalizar_texto(palabra)

            if palabra_normalizada in texto:
                condiciones[condicion] = "si"
                if condicion not in condiciones_detectadas:
                    condiciones_detectadas.append(condicion)
                break

    # Detección por intención: busca combinaciones de palabras relacionadas
    for condicion, grupos in REGLAS_INTENCION.items():
        if condiciones.get(condicion) == "si":
            continue

        for grupo in grupos:
            if all(palabra in texto for palabra in grupo):
                condiciones[condicion] = "si"
                if condicion not in condiciones_detectadas:
                    condiciones_detectadas.append(condicion)
                break

    return condiciones, condiciones_detectadas

def evaluar_condiciones(datos):
    puntajes = {metodologia: 0 for metodologia in METODOLOGIAS}
    razones = {metodologia: [] for metodologia in METODOLOGIAS}

    def sumar(metodologia, puntos, razon):
        puntajes[metodologia] += puntos
        razones[metodologia].append(razon)

    if datos["requisitos_cambian"] == "si":
        sumar("Scrum", 2, "los requisitos pueden cambiar durante el desarrollo")
        sumar("XP", 2, "los requisitos pueden cambiar durante el desarrollo")
        sumar("Espiral", 1, "puede requerirse analizar cambios por ciclos")
    else:
     if datos.get("requisitos_estables") == "si":
        sumar("Cascada", 3, "los requisitos son estables")
        sumar("Kanban", 1, "el trabajo puede organizarse sin tantos cambios")
    
    if datos.get("requisitos_estables") == "si":
        sumar("Cascada", 2, "los requisitos son claros o estables")
        sumar("Kanban", 1, "el proyecto puede organizarse con requisitos definidos")

    if datos["cliente_participa"] == "si":
        sumar("Scrum", 2, "el cliente participará revisando avances")
        sumar("XP", 2, "el cliente participará revisando avances")
    else:
        sumar("Cascada", 1, "la participación del cliente no será constante")
        sumar("Kanban", 1, "puede funcionar con participación moderada del cliente")

    if datos["entregas_rapidas"] == "si":
        sumar("Scrum", 2, "se necesitan entregas funcionales en poco tiempo")
        sumar("XP", 1, "se necesitan entregas funcionales en poco tiempo")
        sumar("Lean", 2, "se busca entregar valor rápidamente")
    else:
        pass

    if datos["flujo_continuo"] == "si":
        sumar("Kanban", 3, "el trabajo será constante o continuo")
        sumar("Lean", 2, "el flujo continuo permite mejorar el proceso")
    else:
        sumar("Scrum", 1, "el trabajo puede organizarse por iteraciones")
        sumar("Cascada", 1, "el trabajo puede organizarse por fases")

    if datos["alta_calidad"] == "si":
        sumar("XP", 4, "se requiere alta calidad en el código")
        sumar("Scrum", 1, "las revisiones frecuentes ayudan a mejorar el producto")
        sumar("Lean", 1, "se busca mejorar la calidad eliminando desperdicios")
    else:
        sumar("Kanban", 1, "la calidad técnica no es el factor principal")

    if datos["proyecto_grande"] == "si":
        sumar("Espiral", 3, "el proyecto es grande o complejo")
        sumar("Cascada", 1, "los proyectos grandes pueden requerir fases formales")
    else:
        sumar("Scrum", 1, "funciona bien en proyectos pequeños o medianos")
        sumar("XP", 1, "funciona bien en proyectos pequeños o medianos")

    if datos.get("proyecto_pequeno") == "si":
        sumar("Scrum", 2, "el proyecto es pequeño y puede manejarse por iteraciones")
        sumar("XP", 1, "el proyecto pequeño permite aplicar buenas prácticas técnicas")
        sumar("Kanban", 1, "el proyecto pequeño puede gestionarse con flujo visual")

    if datos["alto_riesgo"] == "si":
        sumar("Espiral", 4, "existen riesgos técnicos importantes")
    else:
        sumar("Kanban", 1, "el riesgo técnico es bajo")
        sumar("Lean", 1, "el riesgo técnico bajo permite optimizar el proceso")

    if datos["documentacion"] == "si":
        sumar("Cascada", 3, "se requiere documentación formal")
        sumar("Espiral", 1, "el control del proyecto puede requerir documentación")
    else:
        sumar("Scrum", 1, "no se requiere documentación excesiva")
        sumar("XP", 1, "se prioriza el desarrollo sobre la documentación extensa")

    if datos["tiempo_estricto"] == "si":
        sumar("Scrum", 1, "la fecha de entrega es estricta")
        sumar("Lean", 2, "se busca reducir tiempos y desperdicios")
        sumar("Kanban", 1, "ayuda a controlar el avance del trabajo")
    else:
        pass

    if datos["optimizacion"] == "si":
        sumar("Lean", 4, "se busca optimizar recursos")
        sumar("Kanban", 1, "ayuda a visualizar y limitar el trabajo en proceso")
    else:
        sumar("Scrum", 1, "puede priorizarse la organización por sprints")

# MODELO INCREMENTAL
    
    # MODELO INCREMENTAL
    if datos.get("modularidad") == "si":
        sumar("Incremental", 6, "el proyecto puede dividirse en módulos o entregas parciales")
        sumar("Scrum", 1, "el trabajo puede organizarse por avances")
        sumar("Kanban", 1, "las tareas pueden gestionarse visualmente por partes")

    if datos.get("modularidad") == "si" and datos.get("requisitos_estables") == "si":
        sumar("Incremental", 2, "los módulos pueden planearse de forma progresiva con requisitos claros")

    if datos.get("modularidad") == "si" and datos.get("entregas_rapidas") == "si    ":
        sumar("Incremental", 3, "se pueden entregar funcionalidades por etapas")

    if datos.get("modularidad") == "si" and datos.get("proyecto_pequeno") == "si":
        sumar("Incremental", 2, "el proyecto puede crecer progresivamente por partes")      


# RAD

    if datos.get("prototipo") == "si":
        sumar("RAD", 7, "se requiere crear prototipos o validar una idea rápidamente")
        sumar("Scrum", 1, "la retroalimentación rápida puede organizarse por iteraciones")
        sumar("Lean", 1, "la validación rápida ayuda a evitar desperdicios")

    if datos.get("prototipo") == "si" and datos.get("entregas_rapidas") == "si":
        sumar("RAD", 4, "el proyecto requiere desarrollo rápido y validación temprana")

    if datos.get("prototipo") == "si" and datos.get("cliente_participa") == "si":
        sumar("RAD", 3, "el cliente puede validar prototipos durante el desarrollo")

    if datos.get("prototipo") == "si" and datos.get("proyecto_pequeno") == "si":
        sumar("RAD", 2, "un proyecto pequeño permite crear prototipos con rapidez")


# SAFE
    if datos.get("varios_equipos") == "si":
        sumar("SAFe", 4, "existen varios equipos o áreas que deben coordinarse")
        sumar("Scrum", 1, "los equipos pueden trabajar con prácticas ágiles")

    if datos.get("escala_empresarial") == "si":
        sumar("SAFe", 4, "el proyecto tiene un contexto empresarial o de gran escala")
        sumar("Espiral", 1, "los proyectos grandes pueden requerir control adicional")

    if datos.get("proyecto_grande") == "si" and datos.get("varios_equipos") == "si":
        sumar("SAFe", 3, "el proyecto es grande y requiere coordinación entre equipos")

    if datos.get("proyecto_grande") == "si" and datos.get("escala_empresarial") == "si":
        sumar("SAFe", 3, "el proyecto tiene características de escalamiento ágil empresarial")
        
    ordenadas = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)

    return ordenadas, razones


def generar_justificacion(metodologia, razones):
    razones_metodologia = razones[metodologia][:4]

    if not razones_metodologia:
        razones_texto = ""
    elif len(razones_metodologia) == 1:
        razones_texto = razones_metodologia[0]
    elif len(razones_metodologia) == 2:
        razones_texto = razones_metodologia[0] + " y " + razones_metodologia[1]
    else:
        razones_texto = ", ".join(razones_metodologia[:-1]) + " y " + razones_metodologia[-1]

    explicaciones = {
        "Scrum": {
            "encaje": "Scrum encaja porque permite trabajar mediante sprints, entregar avances funcionales en periodos cortos y adaptar el desarrollo conforme aparecen cambios o nuevas necesidades.",
            "recomendacion": "Se recomienda definir un Product Backlog, organizar el trabajo en sprints cortos y realizar revisiones frecuentes con el cliente o usuario final.",
            "cuidado": "Debe cuidarse que el equipo mantenga comunicación constante, porque si no hay seguimiento del cliente, Scrum puede perder efectividad."
        },
         "Kanban": {
            "encaje": "Kanban encaja porque permite administrar un flujo continuo de tareas sin depender de iteraciones fijas, lo cual es útil cuando el trabajo llega de manera constante.",
            "recomendacion": "Se recomienda usar un tablero visual con columnas como pendiente, en proceso y terminado, además de limitar la cantidad de tareas activas para evitar saturación.",
            "cuidado": "Debe cuidarse que las tareas estén bien priorizadas, porque si todo entra al mismo tiempo sin control, el flujo puede volverse desordenado."
        },

        "Cascada": {
            "encaje": "El Modelo en Cascada encaja porque permite organizar el proyecto en fases secuenciales, como análisis, diseño, implementación, pruebas y entrega.",
            "recomendacion": "Se recomienda documentar claramente los requisitos desde el inicio, validar el alcance antes de programar y mantener evidencia de cada fase del desarrollo.",
            "cuidado": "Debe cuidarse que los requisitos no cambien demasiado, porque Cascada es poco flexible ante modificaciones importantes durante el desarrollo."
        },

        "XP": {
            "encaje": "Extreme Programming encaja porque se enfoca en la calidad técnica del software mediante pruebas frecuentes, integración continua y mejora constante del código.",
            "recomendacion": "Se recomienda aplicar pruebas unitarias, revisiones de código, integración continua y prácticas como programación en pareja si el equipo puede hacerlo.",
            "cuidado": "Debe cuidarse que el equipo tenga disciplina técnica, porque XP depende mucho de buenas prácticas de programación y pruebas constantes."
        },

        "Lean": {
            "encaje": "Lean Software Development encaja porque busca entregar valor reduciendo desperdicios, optimizando recursos y evitando actividades que no aportan directamente al producto.",
            "recomendacion": "Se recomienda identificar tareas innecesarias, reducir tiempos de espera, priorizar funciones de mayor valor y mejorar el proceso de forma continua.",
            "cuidado": "Debe cuidarse no confundir rapidez con falta de calidad; Lean busca eficiencia, pero sin descuidar el valor entregado al usuario."
        },

        "Espiral": {
            "encaje": "El Modelo en Espiral encaja porque permite desarrollar el proyecto por ciclos, evaluando riesgos técnicos y tomando decisiones antes de avanzar a la siguiente etapa.",
            "recomendacion": "Se recomienda identificar riesgos desde el inicio, crear prototipos cuando sea necesario y revisar cada ciclo antes de continuar con el desarrollo.",
            "cuidado": "Debe cuidarse que el análisis de riesgos no vuelva el proceso demasiado lento, especialmente si el proyecto tiene tiempos de entrega muy cortos."
        },

        "Incremental": {
            "encaje": "El Modelo Incremental encaja porque permite desarrollar el sistema por módulos o partes funcionales, entregando avances progresivos sin esperar a que todo el producto esté terminado.",
            "recomendacion": "Se recomienda dividir el proyecto en módulos principales, priorizar las funcionalidades más importantes y planear entregas parciales que puedan probarse y mejorarse con el tiempo.",
            "cuidado": "Debe cuidarse que cada incremento esté bien integrado con los anteriores, ya que una mala planificación puede generar problemas de compatibilidad o retrabajo."
        },

        "RAD": {
            "encaje": "RAD encaja porque permite construir prototipos rápidamente, validar ideas con el usuario y ajustar el sistema en poco tiempo antes de desarrollar una versión más completa.",
            "recomendacion": "Se recomienda comenzar con un prototipo funcional, mostrarlo al cliente o usuario, recopilar retroalimentación y mejorar el sistema mediante ciclos cortos de desarrollo.",
            "cuidado": "Debe cuidarse que la rapidez no afecte la calidad final del sistema, ya que RAD puede generar soluciones poco robustas si no se controlan bien los cambios."
        },

        "SAFe": {
            "encaje": "SAFe encaja porque permite coordinar prácticas ágiles en proyectos grandes, especialmente cuando participan varios equipos, áreas o departamentos dentro de una organización.",
            "recomendacion": "Se recomienda definir equipos de trabajo, establecer objetivos comunes, coordinar entregas entre áreas y mantener una planificación general que permita alinear los avances de todos los equipos.",
            "cuidado": "Debe cuidarse que la estructura no se vuelva demasiado pesada, ya que SAFe requiere coordinación constante y puede ser excesivo para proyectos pequeños."
        }
    
    }

    info = explicaciones[metodologia]

    introducciones = {
        "Scrum": "Se recomienda utilizar Scrum porque el proyecto requiere flexibilidad y adaptación constante durante el desarrollo.",
        "Kanban": "Se recomienda utilizar Kanban porque el proyecto se beneficia de un flujo de trabajo continuo y organizado.",
        "Cascada": "Se recomienda utilizar el modelo en Cascada porque el proyecto puede planearse de manera estructurada y secuencial.",
        "XP": "Se recomienda utilizar Extreme Programming porque el proyecto requiere alta calidad técnica y capacidad de adaptación.",
        "Lean": "Se recomienda utilizar Lean Software Development porque el proyecto busca eficiencia y optimización de recursos.",
        "Espiral": "Se recomienda utilizar el modelo en Espiral porque el proyecto implica riesgos o complejidad que deben evaluarse constantemente.",
        "Incremental": "Se recomienda utilizar el Modelo Incremental porque el proyecto puede construirse por módulos o entregas parciales.",
        "RAD": "Se recomienda utilizar RAD porque el proyecto requiere rapidez, prototipos y validación temprana con el usuario.",
        "SAFe": "Se recomienda utilizar SAFe porque el proyecto se desarrolla en un contexto grande o empresarial donde se requiere coordinación entre equipos."
    }

    introduccion = introducciones.get(metodologia, f"Se recomienda {metodologia}.")

    detalle = ""
    if razones_texto:
        detalle = " Esto se debe principalmente a que " + razones_texto + "."

    return (
        f"{introduccion}{detalle}\n\n"
        f"{info['encaje']}\n\n"
        f"Recomendación práctica: {info['recomendacion']}\n\n"
        f"Aspecto a considerar: {info['cuidado']}"
    )
    
def calcular_confianza(ordenadas):
    principal, puntaje_principal = ordenadas[0]
    alternativa, puntaje_alternativa = ordenadas[1]

    diferencia = puntaje_principal - puntaje_alternativa

    if puntaje_principal == 0:
        nivel = "Baja"
        detalle = "El sistema no encontró suficientes coincidencias fuertes para una recomendación confiable."
    elif diferencia >= 4:
        nivel = "Alta"
        detalle = (
            f"La recomendación tiene confianza alta porque {principal} supera claramente "
            f"a la alternativa {alternativa} por {diferencia} puntos."
        )
    elif diferencia >= 2:
        nivel = "Media"
        detalle = (
            f"La recomendación tiene confianza media porque {principal} supera a "
            f"{alternativa}, aunque ambas metodologías podrían ser viables."
        )
    else:
        nivel = "Baja"
        detalle = (
            f"La recomendación tiene confianza baja porque {principal} y {alternativa} "
            f"tienen puntajes muy cercanos. Conviene revisar ambas opciones antes de decidir."
        )

    return nivel, detalle

def recomendar_por_datos(datos):
    ordenadas, razones = evaluar_condiciones(datos)

    principal = ordenadas[0][0]
    alternativa = ordenadas[1][0]

    confianza_nivel, confianza_detalle = calcular_confianza(ordenadas)

    resultado = {
        "principal": principal,
        "alternativa": alternativa,
        "puntajes": ordenadas,
        "confianza_nivel": confianza_nivel,
        "confianza_detalle": confianza_detalle,
        "justificacion_principal": generar_justificacion(principal, razones),
        "justificacion_alternativa": generar_justificacion(alternativa, razones)
    }

    return resultado


def recomendar_por_texto(texto_usuario):
    datos, condiciones_detectadas = detectar_condiciones(texto_usuario)
    resultado = recomendar_por_datos(datos)
    resultado["condiciones_detectadas"] = condiciones_detectadas
    resultado["datos_detectados"] = datos

    return resultado

def generar_guia_metodologia(metodologia):
    guias = {
        "Scrum": (
            "Para aplicar Scrum correctamente, puedes seguir estos pasos:\n\n"
            "1. Define el Product Backlog, es decir, la lista de funciones o tareas principales del proyecto.\n"
            "2. Divide el trabajo en sprints cortos, por ejemplo de una o dos semanas.\n"
            "3. Al inicio de cada sprint, selecciona las tareas más importantes.\n"
            "4. Durante el sprint, el equipo trabaja en esas tareas y revisa avances constantemente.\n"
            "5. Al terminar el sprint, presenta un avance funcional al cliente o usuario.\n"
            "6. Recibe retroalimentación y ajusta el siguiente sprint.\n\n"
            "Scrum es útil cuando el proyecto puede cambiar y el cliente participa con frecuencia."
        ),

        "Kanban": (
            "Para aplicar Kanban correctamente, puedes seguir estos pasos:\n\n"
            "1. Crea un tablero visual con columnas como: Pendiente, En proceso, En revisión y Terminado.\n"
            "2. Coloca cada tarea del proyecto en una tarjeta.\n"
            "3. Mueve las tarjetas conforme avanzan en el proceso.\n"
            "4. Limita la cantidad de tareas que pueden estar en proceso al mismo tiempo.\n"
            "5. Revisa constantemente el flujo para detectar retrasos o acumulación de trabajo.\n\n"
            "Kanban es útil cuando el trabajo es continuo, como soporte, mantenimiento o mejoras constantes."
        ),

        "Cascada": (
            "Para aplicar el modelo en Cascada correctamente, puedes seguir estos pasos:\n\n"
            "1. Define claramente todos los requisitos desde el inicio.\n"
            "2. Documenta el alcance del proyecto antes de comenzar el desarrollo.\n"
            "3. Realiza el análisis del sistema.\n"
            "4. Diseña la arquitectura, pantallas, base de datos o diagramas necesarios.\n"
            "5. Implementa el sistema con base en el diseño aprobado.\n"
            "6. Realiza pruebas al finalizar el desarrollo.\n"
            "7. Entrega el producto final junto con su documentación.\n\n"
            "Cascada funciona mejor cuando los requisitos son estables y se necesita documentación formal."
        ),

        "XP": (
            "Para aplicar Extreme Programming correctamente, puedes seguir estos pasos:\n\n"
            "1. Define historias de usuario pequeñas y claras.\n"
            "2. Trabaja en entregas cortas y frecuentes.\n"
            "3. Aplica pruebas unitarias constantemente.\n"
            "4. Revisa y mejora el código de forma continua.\n"
            "5. Si es posible, aplica programación en pareja para reducir errores.\n"
            "6. Integra los cambios frecuentemente para detectar fallas temprano.\n\n"
            "XP es útil cuando se requiere alta calidad técnica, muchas pruebas y adaptación a cambios."
        ),

        "Lean": (
            "Para aplicar Lean Software Development correctamente, puedes seguir estos pasos:\n\n"
            "1. Identifica las actividades que no aportan valor al proyecto.\n"
            "2. Elimina desperdicios como tareas innecesarias, esperas largas o documentación excesiva.\n"
            "3. Prioriza las funciones que aportan más valor al usuario.\n"
            "4. Reduce tiempos de entrega dividiendo el trabajo en partes pequeñas.\n"
            "5. Mide el avance y mejora el proceso continuamente.\n\n"
            "Lean es útil cuando se busca optimizar recursos, ahorrar tiempo y entregar valor rápidamente."
        ),

        "Espiral": (
            "Para aplicar el modelo en Espiral correctamente, puedes seguir estos pasos:\n\n"
            "1. Identifica los objetivos principales del proyecto.\n"
            "2. Detecta los riesgos técnicos, de tiempo, costos o experiencia del equipo.\n"
            "3. Planea una primera versión o prototipo.\n"
            "4. Evalúa los riesgos antes de avanzar a la siguiente etapa.\n"
            "5. Desarrolla el sistema por ciclos, revisando resultados en cada vuelta.\n"
            "6. Ajusta el proyecto según los riesgos encontrados.\n\n"
            "Espiral es útil para proyectos grandes, complejos o con alto riesgo técnico."
        ),
        "Incremental": (
            "Para aplicar el Modelo Incremental correctamente, puedes seguir estos pasos:\n\n"
            "1. Divide el sistema en módulos o funcionalidades principales.\n"
            "2. Prioriza los módulos más importantes para el usuario.\n"
            "3. Desarrolla una primera versión funcional con las características básicas.\n"
            "4. Entrega cada incremento para revisión o prueba.\n"
            "5. Integra los nuevos módulos con los anteriores.\n"
            "6. Mejora el sistema progresivamente hasta completar el producto.\n\n"
            "El Modelo Incremental es útil cuando el proyecto puede entregarse por partes y se desea mostrar avances funcionales."
        ),

        "RAD": (
            "Para aplicar RAD correctamente, puedes seguir estos pasos:\n\n"
            "1. Identifica rápidamente los requisitos principales del sistema.\n"
            "2. Crea un prototipo inicial de la aplicación o interfaz.\n"
            "3. Presenta el prototipo al usuario o cliente.\n"
            "4. Recibe retroalimentación inmediata.\n"
            "5. Ajusta el prototipo y mejora sus funcionalidades.\n"
            "6. Repite el proceso hasta obtener una versión funcional aceptada.\n\n"
            "RAD es útil cuando se necesita desarrollar rápido, validar ideas y construir prototipos funcionales."
        ),

        "SAFe": (
            "Para aplicar SAFe correctamente, puedes seguir estos pasos:\n\n"
            "1. Identifica los equipos, áreas o departamentos que participarán en el proyecto.\n"
            "2. Define objetivos generales compartidos.\n"
            "3. Organiza el trabajo en incrementos de programa o entregas coordinadas.\n"
            "4. Mantén comunicación constante entre equipos.\n"
            "5. Coordina dependencias entre módulos, áreas o funcionalidades.\n"
            "6. Revisa avances de forma periódica para asegurar alineación.\n\n"
            "SAFe es útil en proyectos grandes o empresariales donde varios equipos deben trabajar de manera coordinada."
        )
    }

    return guias.get(
        metodologia,
        "No tengo una guía disponible para esa metodología."
    )

def es_pregunta_de_guia(texto_usuario):
    texto = normalizar_texto(texto_usuario)

    frases = [
        "como puedo usar",
        "como se usa",
        "como uso",
        "como aplicar",
        "como aplico",
        "como implementar",
        "como implemento",
        "que pasos sigo",
        "pasos para usar",
        "guia",
        "dame una guia",
        "explicame como usar",
        "como puedo trabajar con",
        "como se aplica"
        "como",
        "que hago",
        "que hago para usar",
        "que hago para aplicar",
        "como la aplico",
        
    ]

    return any(frase in texto for frase in frases)

def detectar_intencion_seguimiento(texto_usuario):
    texto = normalizar_texto(texto_usuario)

    intenciones = {
        "por_que": [
            "por que", "porque", "por qué", "razon", "razón",
            "por que me recomendaste", "por que elegiste",
            "por que esa", "por que me diste"
        ],

        "diferencia": [
            "diferencia", "comparar", "comparacion", "comparación",
            "en que se diferencia", "diferencia con la alternativa",
            "cual es mejor", "cuál es mejor"
        ],

        "desventajas": [
            "desventajas", "riesgos", "problemas", "limitaciones",
            "puntos malos", "que debo cuidar", "que puede fallar"
            "aspectos negativos", "contras", "devilidades"
        ],

        "ventajas": [
            "ventajas", "beneficios", "que tiene de bueno",
            "por que conviene", "por qué conviene",
            "puntos buenos", "aspectos positivos", "pros", "fortalezas"
        ],

        "ejemplo": [
            "ejemplo", "caso practico", "caso práctico",
            "aplicado a mi proyecto", "como se veria",
            "cómo se vería", "dame un ejemplo"
        ],

        "herramientas": [
            "herramientas", "software", "apps", "programas",
            "que herramientas", "qué herramientas", "que puedo usar"
        ],

        "roles": [
            "roles", "equipo", "quienes participan",
            "quiénes participan", "personas necesarias",
            "integrantes", "responsables"
        ],

        "documentos": [
            "documentos", "evidencias", "entregables",
            "que documentos", "qué documentos",
            "que debo entregar", "documentacion necesaria"
        ],

        "cuando_no": [
            "cuando no", "cuándo no", "no deberia usar",
            "no debería usar", "cuando no conviene",
            "cuándo no conviene", "en que caso no"
        ]
    }

    for intencion, frases in intenciones.items():
        for frase in frases:
            if frase in texto:
                return intencion

    return None

def es_consulta_de_seguimiento(texto_usuario):
    texto = normalizar_texto(texto_usuario).strip()

    indicadores = [
        "que ", "qué ", "cual ", "cuál ", "como ", "cómo ",
        "por que", "por qué", "cuando ", "cuándo ",
        "dame", "explica", "explicame", "explícame",
        "ventajas", "desventajas", "diferencia",
        "herramientas", "roles", "documentos",
        "ejemplo", "cuando no", "guia", "guía"
    ]

    if "?" in texto or "¿" in texto:
        return True

    return any(texto.startswith(indicador) for indicador in indicadores)

def responder_seguimiento(texto_usuario, metodologia, alternativa, resultado, descripcion_proyecto="", seguimiento_iniciado=False):
    intencion = detectar_intencion_seguimiento(texto_usuario)

    if intencion is None:
        return None

    if resultado is None:
        return (
            "Aún no tengo una metodología recomendada para responder esa pregunta. "
            "Primero descríbeme tu proyecto y después podré darte una explicación más específica."
        )

    # Seguridad extra: si la interfaz no manda metodología o alternativa,
    # se toman directamente del último resultado generado.
    if metodologia is None:
        metodologia = resultado.get("principal")

    if alternativa is None:
        alternativa = resultado.get("alternativa")

    contexto = ""


    if descripcion_proyecto and not seguimiento_iniciado:
        contexto = (
            f"Tomando en cuenta la descripción de tu proyecto:\n"
            f"“{descripcion_proyecto}”\n\n"
        )
        
    datos_metodologias = {
        "Scrum": {
            "ventajas": "Scrum permite organizar el trabajo en sprints, recibir retroalimentación frecuente del cliente y adaptarse a cambios durante el desarrollo.",
            "desventajas": "Puede perder efectividad si el cliente no participa o si el equipo no mantiene comunicación constante.",
            "herramientas": "Puedes usar Jira, Trello, ClickUp, Notion o GitHub Projects para gestionar el backlog y los sprints.",
            "roles": "Los roles principales son Product Owner, Scrum Master y equipo de desarrollo.",
            "documentos": "Product Backlog, Sprint Backlog, actas de revisión, historias de usuario y registro de avances.",
            "cuando_no": "No conviene cuando los requisitos son totalmente fijos, el cliente no participará o el proyecto requiere una documentación muy rígida desde el inicio."
        },

        "Kanban": {
            "ventajas": "Kanban facilita visualizar el flujo de trabajo, controlar tareas en proceso y mejorar la organización de actividades continuas.",
            "desventajas": "Puede volverse desordenado si no se limitan las tareas activas o si no hay una priorización clara.",
            "herramientas": "Puedes usar Trello, Jira, ClickUp, Asana, Notion o GitHub Projects.",
            "roles": "No exige roles estrictos, pero conviene tener responsables de priorización, ejecución y revisión de tareas.",
            "documentos": "Tablero Kanban, lista de tareas, registro de avances y métricas de flujo.",
            "cuando_no": "No conviene si el proyecto necesita ciclos muy definidos, entregas por sprint o una planeación formal por etapas."
        },

        "Cascada": {
            "ventajas": "Cascada permite trabajar por fases claras, documentar bien el proceso y controlar el avance de manera ordenada.",
            "desventajas": "Es poco flexible si los requisitos cambian durante el desarrollo.",
            "herramientas": "Puedes usar Word, Excel, Project, Draw.io, Lucidchart, Jira o cualquier herramienta de documentación y planificación.",
            "roles": "Analista, diseñador, desarrollador, tester, líder de proyecto y responsable de documentación.",
            "documentos": "Documento de requisitos, diseño del sistema, diagramas, plan de pruebas, manuales y reporte final.",
            "cuando_no": "No conviene si el cliente cambia constantemente de opinión o si el proyecto necesita entregas rápidas y ajustes frecuentes."
        },

        "XP": {
            "ventajas": "XP mejora la calidad del código mediante pruebas constantes, integración continua, revisión frecuente y buenas prácticas de programación.",
            "desventajas": "Requiere mucha disciplina técnica y puede ser difícil si el equipo no está acostumbrado a pruebas o programación colaborativa.",
            "herramientas": "Puedes usar GitHub, GitLab, Jenkins, GitHub Actions, SonarQube, VS Code, PyTest, JUnit o herramientas de testing.",
            "roles": "Desarrolladores, cliente o usuario representante, tester y responsable técnico.",
            "documentos": "Historias de usuario, pruebas unitarias, registro de integración, reporte de errores y bitácora de cambios.",
            "cuando_no": "No conviene si el equipo no tiene experiencia técnica suficiente o si no se realizarán pruebas frecuentes."
        },

        "Lean": {
            "ventajas": "Lean ayuda a reducir desperdicios, optimizar recursos, ahorrar tiempo y concentrarse en lo que realmente aporta valor.",
            "desventajas": "Puede confundirse con hacer todo rápido sin control, por lo que se debe cuidar la calidad.",
            "herramientas": "Puedes usar tableros Kanban, Trello, Jira, Notion, diagramas de flujo y herramientas de mejora continua.",
            "roles": "Equipo de desarrollo, responsable de mejora de procesos, líder de proyecto y usuario o cliente clave.",
            "documentos": "Mapa de proceso, lista de desperdicios, backlog priorizado, métricas de mejora y registro de decisiones.",
            "cuando_no": "No conviene si el proyecto necesita una estructura muy formal o si no hay claridad sobre qué actividades aportan valor."
        },

        "Espiral": {
            "ventajas": "Espiral permite analizar riesgos en cada ciclo y avanzar de forma controlada en proyectos grandes o complejos.",
            "desventajas": "Puede ser más lento y costoso si se abusa del análisis de riesgos.",
            "herramientas": "Puedes usar matrices de riesgos, Project, Jira, Excel, herramientas de prototipado y documentación.",
            "roles": "Líder de proyecto, analista de riesgos, desarrolladores, testers, cliente y responsables técnicos.",
            "documentos": "Matriz de riesgos, prototipos, reportes por ciclo, plan de pruebas y documentación de decisiones.",
            "cuando_no": "No conviene para proyectos pequeños, simples o con bajo riesgo técnico."
        },

        "Incremental": {
            "ventajas": "Incremental permite entregar el sistema por módulos o versiones, mostrando avances funcionales sin esperar a terminar todo el producto.",
            "desventajas": "Puede generar problemas de integración si los módulos no se planean correctamente.",
            "herramientas": "Puedes usar Jira, Trello, GitHub Projects, Git, Notion y herramientas de control de versiones.",
            "roles": "Líder de proyecto, desarrolladores por módulo, tester y responsable de integración.",
            "documentos": "Lista de módulos, plan de incrementos, registro de versiones, pruebas por módulo y documentación de integración.",
            "cuando_no": "No conviene si el sistema no puede dividirse en partes funcionales o si todas las funciones dependen entre sí desde el inicio."
        },

        "RAD": {
            "ventajas": "RAD permite crear prototipos rápidos, validar ideas con el usuario y ajustar el sistema antes de desarrollar una versión completa.",
            "desventajas": "Puede generar soluciones poco robustas si se prioriza demasiado la rapidez y no se controla la calidad.",
            "herramientas": "Puedes usar Figma, Balsamiq, Flutter, Tkinter, herramientas low-code, Trello, Notion o GitHub.",
            "roles": "Diseñador de prototipos, desarrollador, usuario evaluador, líder de proyecto y tester.",
            "documentos": "Prototipos, retroalimentación del usuario, registro de cambios, validaciones y versiones de prueba.",
            "cuando_no": "No conviene cuando el sistema requiere alta seguridad, arquitectura compleja o documentación muy formal desde el inicio."
        },

        "SAFe": {
            "ventajas": "SAFe permite coordinar varios equipos en proyectos grandes o empresariales, manteniendo alineación entre áreas.",
            "desventajas": "Puede ser demasiado pesado para proyectos pequeños o equipos reducidos.",
            "herramientas": "Puedes usar Jira Align, Azure DevOps, Jira, Confluence, Miro, Notion y herramientas de planeación empresarial.",
            "roles": "Equipos ágiles, Product Manager, Release Train Engineer, Scrum Masters, Product Owners y responsables de área.",
            "documentos": "Roadmap, backlog de programa, objetivos por incremento, dependencias entre equipos y reportes de avance.",
            "cuando_no": "No conviene para proyectos pequeños, de un solo equipo o con baja necesidad de coordinación empresarial."
        }
    }

    info = datos_metodologias.get(metodologia, {})

    if intencion == "por_que":
        return (
            contexto +
            resultado.get(
                "justificacion_principal",
                f"Te recomendé {metodologia} porque fue la opción con mayor compatibilidad según las condiciones detectadas."
            )
        )
    if intencion == "diferencia":
        return (
            contexto +
            comparar_metodologias(metodologia, alternativa) +
            f"\n\nEn este caso, {metodologia} queda como opción principal porque se adapta mejor a las características detectadas en tu proyecto, mientras que {alternativa} queda como una opción secundaria viable."
        )

    if intencion == "ventajas":
        return (
            contexto +
            f"Ventajas de {metodologia} para este proyecto:\n\n"
            f"{info.get('ventajas', 'No tengo ventajas registradas para esta metodología.')}\n\n"
            f"En tu caso, estas ventajas pueden ayudar a manejar mejor las condiciones detectadas y a organizar el desarrollo de forma más adecuada."
        )

    if intencion == "desventajas":
        return (
            contexto +
            f"Desventajas o aspectos a cuidar de {metodologia} en este proyecto:\n\n"
            f"{info.get('desventajas', 'No tengo desventajas registradas para esta metodología.')}\n\n"
            f"Para tu proyecto, conviene revisar estos puntos antes de aplicarla, especialmente si las condiciones cambian durante el desarrollo."
        )

    if intencion == "herramientas":
        return (
            contexto +
            f"Herramientas recomendadas para aplicar {metodologia} en este proyecto:\n\n"
            f"{info.get('herramientas', 'No tengo herramientas registradas para esta metodología.')}\n\n"
            f"Lo ideal es elegir herramientas que permitan dar seguimiento a las tareas, registrar avances y mantener comunicación con el equipo."
        )

    if intencion == "roles":
        return (
            contexto +
            f"Roles sugeridos para aplicar {metodologia} en este proyecto:\n\n"
            f"{info.get('roles', 'No tengo roles registrados para esta metodología.')}\n\n"
            f"Estos roles pueden ajustarse al tamaño del equipo y a los recursos disponibles."
        )

    if intencion == "documentos":
        return (
            contexto +
            f"Documentos o evidencias útiles para {metodologia} en este proyecto:\n\n"
            f"{info.get('documentos', 'No tengo documentos registrados para esta metodología.')}\n\n"
            f"Estos documentos sirven para dejar evidencia del avance, justificar decisiones y facilitar la entrega del proyecto."
        )

    if intencion == "cuando_no":
        return (
            contexto +
            f"Cuándo NO conviene usar {metodologia}:\n\n"
            f"{info.get('cuando_no', 'No tengo registrada una restricción específica para esta metodología.')}\n\n"
            f"Si alguna de estas condiciones aparece en tu proyecto, convendría reconsiderar la metodología o usar la alternativa recomendada: {alternativa}."
        )

    if intencion == "ejemplo":
        return (
            contexto +
            generar_ejemplo_aplicado(metodologia) +
            f"\n\nAplicándolo a tu caso, puedes adaptar ese ejemplo a las características que mencionaste en la descripción del proyecto."
        )

    return None

def comparar_metodologias(principal, alternativa):
    comparaciones = {
        ("Scrum", "XP"): (
            "Scrum y XP son metodologías ágiles, pero tienen enfoques distintos.\n\n"
            "Scrum se enfoca más en la organización del trabajo mediante sprints, backlog y revisiones con el cliente.\n"
            "XP se enfoca más en la calidad técnica del software, usando pruebas constantes, integración continua y buenas prácticas de programación.\n\n"
            "Si tu prioridad es organización y entregas frecuentes, Scrum es más adecuado. "
            "Si tu prioridad es calidad del código y pruebas, XP puede ser mejor."
        ),

        ("RAD", "Scrum"): (
            "RAD y Scrum permiten trabajar rápido, pero RAD se enfoca más en crear prototipos y validar ideas rápidamente, "
            "mientras que Scrum organiza el desarrollo en sprints con entregas frecuentes.\n\n"
            "RAD conviene si necesitas una demo o prototipo inicial. Scrum conviene si ya tienes una idea más clara y quieres avanzar por iteraciones."
        ),

        ("SAFe", "Espiral"): (
            "SAFe y Espiral pueden aplicarse en proyectos grandes, pero SAFe se enfoca en coordinar varios equipos dentro de una organización, "
            "mientras que Espiral se enfoca en analizar riesgos técnicos durante ciclos de desarrollo.\n\n"
            "SAFe conviene más cuando hay varias áreas o equipos. Espiral conviene más cuando el riesgo técnico es el factor principal."
        ),

        ("Incremental", "Scrum"): (
            "Incremental y Scrum permiten avanzar por partes, pero Incremental se enfoca en construir módulos o versiones del sistema, "
            "mientras que Scrum organiza el trabajo en sprints con revisión constante.\n\n"
            "Incremental conviene si el sistema puede dividirse claramente en módulos. Scrum conviene si el cliente participará y habrá cambios frecuentes."
        ),

        ("Lean", "Kanban"): (
            "Lean y Kanban se relacionan bastante, pero Lean se enfoca en eliminar desperdicios y optimizar recursos, "
            "mientras que Kanban se enfoca en visualizar el flujo de trabajo y controlar tareas en proceso.\n\n"
            "Lean conviene si buscas eficiencia general. Kanban conviene si necesitas organizar tareas continuas."
        )
    }

    if (principal, alternativa) in comparaciones:
        return comparaciones[(principal, alternativa)]

    if (alternativa, principal) in comparaciones:
        return comparaciones[(alternativa, principal)]

    return (
        f"{principal} fue seleccionada como opción principal porque obtuvo mayor compatibilidad con las condiciones detectadas. "
        f"{alternativa} aparece como alternativa porque también comparte algunas características útiles para el proyecto.\n\n"
        f"En general, conviene revisar cuál de las dos se ajusta mejor al nivel de organización, flexibilidad, documentación, riesgo y participación del cliente que tendrá el proyecto."
    )

def generar_ejemplo_aplicado(metodologia):
    ejemplos = {
        "Scrum": (
            "Ejemplo aplicado con Scrum:\n\n"
            "Podrías crear un Product Backlog con las funciones principales del sistema. "
            "Después divides el trabajo en sprints de una o dos semanas. "
            "Al final de cada sprint presentas un avance funcional al cliente y ajustas el siguiente sprint con base en su retroalimentación."
        ),

        "Kanban": (
            "Ejemplo aplicado con Kanban:\n\n"
            "Puedes crear un tablero con columnas como Pendiente, En proceso, En revisión y Terminado. "
            "Cada tarea del proyecto se coloca como tarjeta y se mueve conforme avanza. "
            "Esto ayuda a visualizar el flujo de trabajo y evitar acumulación de tareas."
        ),

        "Cascada": (
            "Ejemplo aplicado con Cascada:\n\n"
            "Primero documentas todos los requisitos. Después realizas el diseño del sistema, luego la programación, posteriormente pruebas y finalmente la entrega. "
            "Cada fase debe completarse antes de pasar a la siguiente."
        ),

        "XP": (
            "Ejemplo aplicado con XP:\n\n"
            "Puedes trabajar con historias de usuario pequeñas, crear pruebas unitarias antes o durante el desarrollo, revisar código constantemente e integrar cambios con frecuencia. "
            "Esto ayuda a mantener la calidad técnica del sistema."
        ),

        "Lean": (
            "Ejemplo aplicado con Lean:\n\n"
            "Puedes identificar actividades innecesarias, reducir tiempos de espera y priorizar únicamente las funciones que aportan valor al usuario. "
            "El objetivo es entregar valor usando la menor cantidad posible de recursos sin descuidar la calidad."
        ),

        "Espiral": (
            "Ejemplo aplicado con Espiral:\n\n"
            "Primero identificas riesgos técnicos del proyecto. Luego desarrollas un prototipo o módulo inicial, evalúas los riesgos encontrados y decides si avanzar al siguiente ciclo. "
            "Este proceso se repite hasta completar el sistema."
        ),

        "Incremental": (
            "Ejemplo aplicado con Incremental:\n\n"
            "Puedes dividir el sistema en módulos. Primero entregas el módulo de usuarios, después el módulo de reportes, luego configuración y finalmente estadísticas. "
            "Cada incremento agrega valor al sistema."
        ),

        "RAD": (
            "Ejemplo aplicado con RAD:\n\n"
            "Primero construyes una maqueta o prototipo funcional. Luego lo muestras al cliente, recibes comentarios y haces ajustes rápidos. "
            "Después repites el proceso hasta llegar a una versión aceptada."
        ),

        "SAFe": (
            "Ejemplo aplicado con SAFe:\n\n"
            "Puedes dividir el trabajo entre varios equipos, definir objetivos comunes, coordinar entregas entre áreas y revisar avances en conjunto. "
            "Esto permite que varios equipos trabajen alineados dentro de un proyecto empresarial."
        )
    }

    return ejemplos.get(
        metodologia,
        "No tengo un ejemplo aplicado para esta metodología."
    )