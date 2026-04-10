---
name: evaluacion_backend_java
description: Skill para evaluar candidatos backend Java (Senior, Mid o Junior) a partir de un CV (PDF o Word). Soporta posicionamiento automático de nivel, evaluación contra un perfil específico, y evaluación masiva. Siempre genera un archivo markdown con los resultados y un timestamp.
---

## Objetivo
Analizar experiencia, stack técnico y profundidad real del candidato para:
1. **Posicionar su nivel** (Senior / Mid / Junior) cuando no se indica perfil objetivo.
2. **Validar aptitud** para un perfil específico (Senior / Mid / Junior) cuando se indica.
3. En ambos casos, clasificar la decisión como **PASA / PASA CON DUDA / NO PASA** y generar feedback estructurado.

---

## Escenarios de uso

### Escenario A – Evaluación libre (sin perfil indicado)
El usuario adjunta uno o más CVs sin especificar nivel.
- Determinar el nivel que mejor representa al candidato: **Senior / Mid / Junior**.
- Generar el informe completo con decisión y feedback.

### Escenario B – Evaluación contra perfil (con perfil indicado)
El usuario adjunta uno o más CVs e indica el nivel objetivo (Senior, Mid o Junior).
- Evaluar si el candidato cumple los requisitos de ese nivel.
- Generar el informe completo con decisión y feedback.

### Escenario C – Evaluación masiva (múltiples CVs)
El usuario adjunta más de un CV (con o sin perfil indicado).
- Evaluar cada candidato individualmente con el formato completo de feedback.
- Al final, incluir un **Resumen Ejecutivo** comparando todos los candidatos en una tabla.
- Generar un único archivo markdown con todos los resultados.

---

## Inputs
- CV en formato PDF o Word (uno o varios)
- Nivel objetivo (opcional): Senior / Mid / Junior

---

## Evaluación por Nivel

### 1. Backend – Senior

#### 1.1 Stack Tecnológico Principal
- Java 17+ (obligatorio)
- Conocimiento avanzado de:
  - Programación Reactiva
  - Streams API
  - Concurrencia y multithreading
- Ecosistema Spring:
  - Spring Boot
  - Spring Security
  - Spring Cloud
  - Spring Data
- Microservicios:
  - REST (mínimo)
  - gRPC o GraphQL (deseable)
- Persistencia:
  - SQL Server (optimización de queries)
  - NoSQL (CosmosDB o similar)
- Caching:
  - Redis o Memcached

#### 1.2 Arquitectura y Diseño
- Principios SOLID y Clean Code
- Patrones de diseño: Creacionales, Estructurales, Comportamiento
- Arquitectura Hexagonal / Onion
- Event-driven: Kafka, RabbitMQ u otros

---

### 2. Backend – Mid (Regular)

#### 2.1 Stack Tecnológico
- Java 17 (mínimo)
- Streams, Optional, Lambdas
- Spring Boot: MVC, Data, Security
- Bases de datos: SQL Server
- APIs: RESTful, Swagger/OpenAPI
- Testing: JUnit, Mockito

#### 2.2 Arquitectura
- SOLID y Clean Code (nivel básico/intermedio)
- Arquitectura en capas o hexagonal (básico)
- Control de versiones: Azure DevOps / Pipelines

---

### 3. Backend – Junior

#### 3.1 Stack Tecnológico
- Java 8+ (mínimo funcional)
- Spring Boot básico (controllers, services, repositories)
- APIs REST básicas
- Bases de datos relacionales (consultas simples)
- Git básico

#### 3.2 Arquitectura
- MVC o arquitectura en capas básica
- Sin necesidad de patrones avanzados
- Testing básico (JUnit sin Mockito es aceptable)

---

## Reglas de Evaluación

### Senior
- Debe cumplir al menos 70–80% del stack
- Debe demostrar experiencia REAL en sistemas productivos complejos
- Mínimo 4–5 años de experiencia backend Java efectiva

### Mid
- Debe cumplir al menos 60–70% del stack
- Puede tener gaps, pero debe ser funcional en backend
- Mínimo 2–3 años de experiencia

### Junior
- Debe cumplir al menos 50% del stack básico
- Puede basarse en proyectos académicos o prácticas
- Hasta 2 años de experiencia (incluyendo prácticas)

---

## Output esperado

### Estructura por candidato (Escenarios A y B)

```
# Evaluación: [Nombre del Candidato]
Fecha: [YYYY-MM-DD HH:MM]  
Nivel postulado: [Senior / Mid / Junior / No especificado]

---

## 1. Resumen del perfil
- **Años de experiencia:** X años
- **Stack principal:** ...
- **Tipo de proyectos:** ...

## 2. Posicionamiento de nivel  ← solo en Escenario A
> Nivel detectado: **[Senior / Mid / Junior]**

## 3. Evaluación técnica
| Criterio       | Nivel              |
|----------------|--------------------|
| Stack          | Alto / Medio / Bajo |
| Arquitectura   | Alto / Medio / Bajo |
| Backend real   | Sí / Parcial / No  |

## 4. Fortalezas
- ...
- ...

## 5. Puntos de mejora
- ...
- ...

## 6. Alertas
- ...

## 7. Decisión final
> **[PASA / PASA CON DUDA / NO PASA]**
```

### Estructura para evaluación masiva (Escenario C)

Cada candidato usa la estructura anterior, luego al final:

```
---

# Resumen Ejecutivo

| Candidato | Nivel Evaluado | Stack | Arquitectura | Backend Real | Decisión |
|-----------|---------------|-------|-------------|-------------|---------|
| ...       | ...            | ...   | ...          | ...          | ...      |
```

---

## Reglas de generación del archivo markdown

1. **Nombre del archivo:**
   - Un candidato: `[NombreCandidato]_[YYYYMMDD].md` (sin espacios, sin tildes)
   - Múltiples candidatos: `Evaluacion_[YYYYMMDD_HHmm].md`
2. **Ubicación:** Guardar en la carpeta `cvs/resultados/` relativa al workspace actual. Crear la carpeta si no existe.
3. **Timestamp:** Siempre incluir en el encabezado del archivo: `Generado el: [YYYY-MM-DD HH:MM:SS]`
4. Usar la herramienta `create_file` para crear el archivo con el contenido generado.

---

## Notas generales
- Priorizar experiencia real sobre buzzwords
- Penalizar perfiles muy fullstack para roles backend puros
- Validar profundidad técnica en entrevista para decisiones "PASA CON DUDA"
- El nivel Junior se asigna cuando la experiencia es insuficiente para Mid pero hay potencial técnico visible
