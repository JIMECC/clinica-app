import anthropic

client = anthropic.Anthropic(api_key="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")


def analizar_citas_por_medico(medicos, totales):
    texto = ""
    for medico, total in zip(medicos, totales):
        texto += f" {medico}: {total} citas "

    prompt = f"""
        Eres un analista de datos médicos experto. Analiza los siguientes datos de citas por médico: {texto}

        Proporciona un análisis estructurado que incluya:
        1. Análisis de la carga de trabajo de cada médico.
        2. Identificación del médico con mayor y menor demanda.
        3. Pronóstico de demanda para el próximo período.
        4. Posibles razones que expliquen las diferencias de carga.
        5. Recomendaciones concretas para optimizar la distribución de citas.

        Sé claro, objetivo y profesional. Responde en español.
        Si los datos son insuficientes para un análisis completo, indícalo.
    """

    mensaje = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return mensaje.content[0].text


def analizar_pacientes_por_genero(generos, totales):
    texto = ""
    for genero, total in zip(generos, totales):
        texto += f" {genero or 'No especificado'}: {total} pacientes "

    prompt = f"""
        Eres un analista de datos de salud. Analiza la siguiente distribución de pacientes por género: {texto}

        Proporciona un análisis que incluya:
        1. Descripción de la distribución demográfica por género.
        2. Porcentaje aproximado de cada grupo respecto al total.
        3. Implicaciones clínicas de esta distribución.
        4. Recomendaciones para adaptar los servicios según la demografía.
        5. Pronóstico sobre tendencias futuras de atención.

        Sé claro, objetivo y profesional. Responde en español.
    """

    mensaje = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return mensaje.content[0].text


def analizar_medicamentos_frecuentes(medicamentos, totales):
    texto = ""
    for medicamento, total in zip(medicamentos, totales):
        texto += f" {medicamento}: {total} veces recetado "

    prompt = f"""
        Eres un farmacéutico y analista clínico experto. Analiza los siguientes datos de medicamentos más recetados: {texto}

        Proporciona un análisis que incluya:
        1. Identificación de los medicamentos más y menos frecuentes.
        2. Análisis de qué condiciones o enfermedades podrían estar predominando.
        3. Patrones relevantes en las prescripciones.
        4. Recomendaciones para la gestión del stock de medicamentos.
        5. Pronóstico de demanda y posibles variaciones estacionales.

        Sé claro, objetivo y profesional. Responde en español.
    """

    mensaje = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return mensaje.content[0].text