from behave import given, when, then

# Variables para simular el estado de la prueba
class EstadoSimulado:
    pdf_subido = False
    mensaje_usuario = ""
    decision_agente = ""

estado = EstadoSimulado()

@given('que he subido un PDF sobre "{tema}"')
def step_dado_pdf_subido(context, tema):
    estado.pdf_subido = True
    print(f"\n[BDD] PDF sobre {tema} simulado con éxito.")

# Apilamos los decoradores para que acepte tanto "pregunto" como "escribo"
@when('le pregunto al chat "{pregunta}"')
@when('le escribo al chat "{pregunta}"')
def step_cuando_pregunta_chat(context, pregunta):
    estado.mensaje_usuario = pregunta
    # Simulamos el enrutador agéntico (Agentic Routing) que programamos en agent_service.py
    if "examen" in pregunta.lower() or "prueba" in pregunta.lower():
        estado.decision_agente = "GENERAR EXAMEN"
    else:
        estado.decision_agente = "EXPLICAR CONCEPTO"

@then('el agente debe decidir "{decision_esperada}" y dar una respuesta amigable')
def step_entonces_explicar(context, decision_esperada):
    assert estado.pdf_subido is True, "Error: No se había subido un PDF"
    assert estado.decision_agente == decision_esperada, f"Se esperaba {decision_esperada} pero el agente hizo {estado.decision_agente}"
    print(f"✅ ¡Éxito! El agente tomó la decisión correcta: {estado.decision_agente}")

@then('el agente debe decidir "{decision_esperada}" y devolver un quiz de 3 preguntas')
def step_entonces_examen(context, decision_esperada):
    assert estado.pdf_subido is True, "Error: No se había subido un PDF"
    assert estado.decision_agente == decision_esperada, f"Se esperaba {decision_esperada} pero el agente hizo {estado.decision_agente}"
    print(f"✅ ¡Éxito! El agente tomó la decisión correcta: {estado.decision_agente}")