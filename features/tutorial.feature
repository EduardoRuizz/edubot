# language: es

Característica: Interacción inteligente con EduBot
  Como alumno del curso
  Quiero chatear con EduBot tras subir un PDF
  Para resolver mis dudas o evaluar mis conocimientos de forma automática

  Escenario: El agente decide explicar un concepto cuando el usuario hace una pregunta
    Dado que he subido un PDF sobre "Arquitectura Software"
    Cuando le pregunto al chat "Explícame qué es la arquitectura hexagonal"
    Entonces el agente debe decidir "EXPLICAR CONCEPTO" y dar una respuesta amigable

  Escenario: El agente decide generar un examen cuando el usuario pide una prueba
    Dado que he subido un PDF sobre "Arquitectura Software"
    Cuando le escribo al chat "Ponme a prueba con un examen corto"
    Entonces el agente debe decidir "GENERAR EXAMEN" y devolver un quiz de 3 preguntas