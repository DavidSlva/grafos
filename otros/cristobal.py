import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Configura tu API Key de OpenAI
openai_api_key = ''

# Inicializa el modelo con GPT-4o
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o")

puntos_Fuerte_predeterminados = [
    "Personalización y conexión emocional: El vendedor establece una conexión emocional con el cliente y personaliza la oferta según sus necesidades.",
    "Escucha activa: La escucha activa se enfoca en comprender y responder adecuadamente a diversas preocupaciones. Estas incluyen la asequibilidad del seguro, la necesidad percibida del mismo, comparaciones con ofertas competitivas, dudas sobre terminos y condiciones,",
    "Claridad en la información del producto: Explica claramente los beneficios y coberturas del seguro, asegurando la comprensión del cliente.",
    "Cierre efectivo: El vendedor utiliza técnicas de cierre efectivas para concretar la venta.",
    "Empatía y conexión: Comunicación personalizada que resulta en una interacción única y significativa.",
    "Ejemplos concretos: El vendedor proporciona ejemplos concretos de casos de uso del seguro, facilitando la comprensión del cliente.",
    "Transparencia: Se explican claramente las exclusiones en el contrato del seguro, generando confianza en el cliente.",
    "Explicación clara: Se detallan claramente los beneficios adicionales del seguro, ayudando a la toma de decisiones del cliente.",
    "Claro conocimiento del vendedor: El vendedor responde con precisión a preguntas sobre los beneficios del seguro, demostrando dominio del producto.",
    "Adaptabilidad y Flexibilidad: El vendedor ajusta la dinámica de la llamada y el enfoque de comunicación según las reacciones y necesidades del cliente."
]

puntos_debiles_predeterminados = [
    "Falta de personalización y conexión emocional: El vendedor no establece una conexión emocional con el cliente y no personaliza la oferta según sus necesidades.",
    "Falta de escucha activa: El vendedor no demuestra estar escuchando activamente al cliente, lo que afecta la calidad de la interacción.",
    "Exceso de información técnica: El vendedor proporciona demasiada información técnica sin contexto, confundiéndo al cliente.",
    "Falta de claridad en la información del producto: No explica claramente los beneficios y coberturas del seguro.",
    "Falta de cierre efectivo: El vendedor no utiliza técnicas de cierre efectivas para concretar la venta.",
    "Falta de empatía y conexión: Comunicación no personalizada, resultando en una interacción genérica y poco significativa.",
    "Falta de ejemplos concretos: El vendedor no proporciona ejemplos concretos de casos de uso del seguro, dificultando la comprensión del cliente.",
    "Falta de transparencia: No se explican claramente las exclusiones en el contrato del seguro, generando desconfianza en el cliente.",
    "Explicación confusa: No se detallan claramente los beneficios adicionales del seguro, complicando la toma de decisiones del cliente.",
    "Falta de conocimiento del vendedor: El vendedor no responde adecuadamente a preguntas sobre los beneficios del seguro, demostrando un conocimiento limitado.",
    "Falta de adaptabilidad y Flexibilidad: El vendedor falla en ajustar la dinámica de la llamada y el enfoque de comunicación según las reacciones y necesidades del cliente."
]

def leer_transcripcion(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as file:
        transcripcion = file.read()
    return transcripcion

def limpiar_transcripcion(transcripcion):
    transcripcion = re.sub(r'\s+', ' ', transcripcion)
    transcripcion = re.sub(r'[^\w\s.,!?]', '', transcripcion)
    return transcripcion

def analizar_transcripcion_pf(transcripcion):
    prompt = f"""
    Analiza la siguiente transcripción y proporciona un análisis detallado de los puntos fuertes del vendedor, utilizando únicamente los siguientes puntos predeterminados junto con sus explicaciones:
    {', '.join(puntos_Fuerte_predeterminados)}. Para que un punto sea considera punto fuerte, este debe ser los suficientemente significativo en el dialogo, es decir, debe ser algo recurrente, no se debe colocar un punto fuerte por la mas minima señal de que es un punto fuerte, debe ser claro.
    
    Incluye ejemplos específicos del texto en el formato:
    
    punto Fuerte: explicación del punto fuerte - 'ejemplo del punto fuerte directo de la transcripción'
    
    Asegúrate de proporcionar explicaciones breves,detalladas y contextuales para cada punto fuerte identificado ( no debes copiar la explicacion de puntos_Fuerte_predeterminados) si un punto fuerte no es claro segun su explicacion en la transcripcion, no lo debes poner.

    Transcripción:
    {transcripcion}
    """
    response = llm.invoke([SystemMessage(content="Eres un asistente experto en analizar transcripciones de llamadas entre vendedores y clientes. Tu objetivo es identificar los puntos fuertes del vendedor al llevar a cabo la venta en la transcripción para potenciar el rendimiento del vendedor."),
                           HumanMessage(content=prompt)])
    return response.content.strip()

def analizar_transcripcion_pd(transcripcion):
    # Define el prompt detallado
    prompt = f"""
    Analiza la siguiente transcripción y proporciona un análisis detallado de los puntos débiles del vendedor, utilizando únicamente los siguientes puntos predeterminados:
    {', '.join(puntos_debiles_predeterminados)}.  Para que un punto sea considera punto debil, este debe ser los suficientemente significativo en el dialogo, es decir, debe ser algo recurrente, no se debe colocar un punto debil por la mas minima señal de que es un punto debil, debe ser claro.
    
    Incluye ejemplos específicos del texto en el formato:
    
    punto débil: explicación del punto débil - 'ejemplo del punto débil directo de la transcripción'
    
    Asegúrate de proporcionar explicaciones breves,detalladas y contextuales para cada punto debil identificado ( no debes copiar la explicacion de puntos_debiles_predeterminados)si un punto debil no es claro segun su explicacion en la transcripcion, no lo debes poner.

    Transcripción:
    {transcripcion}
    """
    
    response = llm.invoke([SystemMessage(content="Eres un asistente experto en analizar transcripciones de llamadas entre vendedores y clientes. Tu objetivo es identificar los puntos debiles del vendedor al llevar a cabo la venta en la transcripción para potenciar el rendimiento del vendedor."),
                           HumanMessage(content=prompt)])
    return response.content.strip()

def analizar_transcripcion_obj(transcripcion):
    # Define el prompt detallado
    prompt = f"""
    Analiza la siguiente transcripción y proporciona un análisis detallado de las objeciones presentadas. Incluye ejemplos específicos del texto en el formato:
    
    Objeción: explicación de la objeción - 'ejemplo de la objeción directo de la transcripción'
    
    Asegúrate de proporcionar explicaciones detalladas y contextuales para cada objeción identificado. (mínimo 500 tokens)
    
    Transcripción:
    {transcripcion}
    """
    response = llm.invoke([SystemMessage(content="Eres un asistente experto en analizar transcripciones de llamadas entre vendedores y clientes. Tu objetivo es identificar las objeciones del cliente y como fueron manejadas por el vendedor en la transcripción para mejorar el rendimiento del vendedor."),
                           HumanMessage(content=prompt)])
    return response.content.strip()

def reconciliar_resultados(transcripcion,objeciones, puntos_fuertes, puntos_debiles):
    
    """Revisa y elimina cualquier contradicción entre los puntos fuertes y débiles."""
    prompt = f"""
    Revisa los siguientes análisis de puntos fuertes y débiles para una misma transcripción. Debes identificar puntos que se repitan entre categorias, no puede existir el mismo punto en las 2 categorias ( por ejemplo: escucha activa no puede estar en puntos fuertes y puntos debiles y asi para cualquier punto) si algun punto esta en 2 categorias debes revisar la transcripcion a la cual se le realizo el analisis y eliminar el punto menos significativo ( por ejemplo: si escucha activa esta en ambas categorias debes revisar la transcripcion y decidir si es un punto fuerte o debil segun el dialogo)(no siempre sera tan explicito los duplicados debes analizarlo bien).

    Transcripción:
    {transcripcion}

    Puntos Fuertes:
    {puntos_fuertes}

    Puntos Débiles:
    {puntos_debiles}

    Proporciona una lista final de puntos fuertes y débiles sin contradicciones con su respectiva explicacion y detalle.

    Proporciona una lista de cuales son los puntos importantes que el ejecutivo debe mejorar y como mejorarlos respecto al analisis de puntos debiles y fuertes

    Finalmente proporciona una explicacion de porque la venta no se llevo a cabo (esta debe tener sentido con los puntos debiles, fuertes y objeciones).
    """
    response = llm.invoke([SystemMessage(content="Eres un asistente experto en reconciliar análisis de puntos fuertes y débiles en transcripciones de llamadas, con el fin de eliminar duplicados ya que estos suelen ser una contradiccion ya que no tiene sentido que un punto fuerte del vendedor tambien sea un punto debil del vendedor."),
                           HumanMessage(content=prompt)])
    return response.content.strip()

def guardar_resultados_html(resultados):
    ruta_archivo, objeciones, puntos_fuertes, puntos_debiles, resultados_reconciliados = resultados
    nombre_archivo_transcripcion = os.path.basename(ruta_archivo)
    nombre_archivo_resultados = os.path.splitext(nombre_archivo_transcripcion)[0] + '_analisis.html'

    with open(nombre_archivo_resultados, 'w', encoding='utf-8') as file:
        file.write("""
         <html>
            <head>
                <title>Resultados de Análisis</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        background-color: #f4f4f9;
                    }
                    h2 {
                        color: #333;
                        border-bottom: 2px solid #ddd;
                        padding-bottom: 10px;
                    }
                    h3 {
                        color: #555;
                        margin-top: 30px;
                    }
                    p {
                        background: #fff;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        margin-top: 10px;
                        line-height: 1.6;
                    }
                    .section {
                        margin-bottom: 40px;
                    }
                    .highlight {
                        background-color: #e7f3fe;
                        border-left: 6px solid #2196F3;
                        padding: 10px 15px;
                        margin-bottom: 10px;
                    }
                    .negrita {
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
            """)
        file.write(f"<h2>Resultados para {nombre_archivo_transcripcion}:</h2>")
        file.write("<div class='section'>")
        file.write("<h3>Objeciones:</h3>")
        file.write(f"<p class='highlight'>{objeciones.replace('#### ', '<span class=\"negrita\">').replace('\n#### ', '</span><br>').replace('\n', '<br>')}</p>")
        file.write("</div>")
        file.write("<div class='section'>")
        file.write("<h3>Puntos Fuertes y Débiles:</h3>")
        file.write(f"<p class='highlight'>{resultados_reconciliados.replace('#### ', '<span class=\"negrita\">').replace('\n#### ', '</span><br>').replace('\n', '<br>')}</p>")
        file.write("</div>")
        file.write("</body></html>")

        print(f"Resultados guardados en {nombre_archivo_resultados}")

def ejecutar_analisis(ruta_archivo):
    transcripcion = leer_transcripcion(ruta_archivo)
    transcripcion_limpia = limpiar_transcripcion(transcripcion)

    objeciones = analizar_transcripcion_obj(transcripcion_limpia)
    puntos_fuertes = analizar_transcripcion_pf(transcripcion_limpia)
    puntos_debiles = analizar_transcripcion_pd(transcripcion_limpia)

    resultados_reconciliados = reconciliar_resultados(transcripcion_limpia, objeciones, puntos_fuertes, puntos_debiles)

    return ruta_archivo, objeciones, puntos_fuertes, puntos_debiles, resultados_reconciliados

def listar_transcripciones(ruta_directorio):
    archivos = [f for f in os.listdir(ruta_directorio) if f.endswith('.txt')]
    print("Archivos disponibles para análisis:")
    for idx, archivo in enumerate(archivos):
        print(f"{idx + 1}. {archivo}")
    return archivos

def seleccionar_transcripciones(archivos):
    seleccionados = []
    while True:
        try:
            eleccion = int(input("Ingrese el número del archivo que desea analizar: "))
            if 1 <= eleccion <= len(archivos) and archivos[eleccion - 1] not in seleccionados:
                seleccionados.append(archivos[eleccion - 1])
            else:
                print("Por favor, ingrese un número válido o uno que no haya sido seleccionado.")
            
            otra = input("¿Desea analizar otra transcripción? (s/n): ").strip().lower()
            if otra != 's':
                break
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")
    return seleccionados

def main():
    ruta_directorio = r'C:\Users\crist\Desktop\transcripciones api gpt 4o\transcripciones'
    archivos = listar_transcripciones(ruta_directorio)
    archivos_seleccionados = seleccionar_transcripciones(archivos)

    resultados = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futuros = {executor.submit(ejecutar_analisis, os.path.join(ruta_directorio, archivo)): archivo for archivo in archivos_seleccionados}
        for futuro in as_completed(futuros):
            resultados.append(futuro.result())

    for resultado in resultados:
        guardar_resultados_html(resultado)

if _name_ == "_main_":
    main()