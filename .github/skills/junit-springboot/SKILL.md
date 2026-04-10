---
name: junit-springboot
description: "Skill para generar pruebas unitarias con JUnit 5 y Mockito para proyectos Spring Boot. Usar cuando el usuario solicite: crear tests unitarios para un servicio, repositorio o controlador Spring Boot, generar casos de prueba para un método específico, escribir pruebas con @Mock y @InjectMocks, testear excepciones, validar comportamiento con verify(), o cubrir flujos happy path y error path. Produce clases de test Java completas listas para compilar."
argument-hint: "Pega o describe la clase Java que quieres testear (Service, Controller, Repository, Component)"
---

# JUnit 5 + Mockito — Spring Boot Test Generator

## Principios de Operación

1. **JUnit 5 por defecto** — usar `@ExtendWith(MockitoExtension.class)`, nunca JUnit 4.
2. **Mockito puro para unit tests** — no levantar contexto Spring (`@SpringBootTest` solo si el usuario lo pide explícitamente).
3. **AAA siempre** — cada test sigue el patrón **Arrange → Act → Assert**.
4. **Cobertura mínima** — generar al menos: happy path, caso nulo/vacío, y al menos un error/excepción esperado.
5. **Nombres descriptivos** — método: `should<Resultado>_when<Condicion>()` en camelCase.
6. **Sin lógica en tests** — los tests no deben contener `if`, `for` ni lógica de negocio.

---

## Flujo de Trabajo

### Paso 1 — Analizar la clase objetivo

Al recibir una clase Java, identificar:

| Elemento | Acción |
|----------|--------|
| Tipo de clase | Service / Controller / Repository / Component / Util |
| Dependencias inyectadas | Listar para crear `@Mock` por cada una |
| Métodos públicos | Generar al menos 2–3 tests por método |
| Excepciones declaradas | Generar test con `assertThrows` |
| Anotaciones Spring | `@Transactional`, `@Cacheable`, etc. — documentar impacto en test |

### Paso 2 — Seleccionar estrategia de test

```
SI la clase es @Service o @Component → usar MockitoExtension (puro unitario)
SI la clase es @RestController → usar MockitoExtension + MockMvc manual (sin contexto)
SI la clase usa @Repository (JPA) → usar @DataJpaTest con H2 (integración ligera)
SI el usuario pide @SpringBootTest → generar test de integración completo
SI hay métodos estáticos → mencionar PowerMock o refactoring como alternativa
```

### Paso 3 — Generar la clase de test

Usar la siguiente estructura base:

```java
@ExtendWith(MockitoExtension.class)
class <ClassName>Test {

    @Mock
    private <Dependency> dependency;

    @InjectMocks
    private <ClassName> subject;

    @BeforeEach
    void setUp() {
        // inicialización opcional
    }

    // --- Tests por método ---

    @Test
    @DisplayName("should <resultado> when <condición>")
    void should<Result>_when<Condition>() {
        // Arrange
        // Act
        // Assert
    }
}
```

### Paso 4 — Patrones por escenario

#### Service con dependencia de repositorio
```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderService orderService;

    @Test
    @DisplayName("should return order when valid id is provided")
    void shouldReturnOrder_whenValidIdProvided() {
        // Arrange
        Long orderId = 1L;
        Order mockOrder = new Order(orderId, "PENDING");
        when(orderRepository.findById(orderId)).thenReturn(Optional.of(mockOrder));

        // Act
        Order result = orderService.findById(orderId);

        // Assert
        assertNotNull(result);
        assertEquals(orderId, result.getId());
        verify(orderRepository, times(1)).findById(orderId);
    }

    @Test
    @DisplayName("should throw NotFoundException when order does not exist")
    void shouldThrowNotFoundException_whenOrderDoesNotExist() {
        // Arrange
        Long orderId = 99L;
        when(orderRepository.findById(orderId)).thenReturn(Optional.empty());

        // Act & Assert
        assertThrows(NotFoundException.class, () -> orderService.findById(orderId));
        verify(orderRepository, times(1)).findById(orderId);
    }
}
```

#### Controller con MockMvc manual (sin contexto Spring)
```java
@ExtendWith(MockitoExtension.class)
class OrderControllerTest {

    @Mock
    private OrderService orderService;

    @InjectMocks
    private OrderController orderController;

    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(orderController).build();
    }

    @Test
    @DisplayName("should return 200 and order when GET /orders/{id} is called with valid id")
    void shouldReturn200_whenGetOrderByValidId() throws Exception {
        // Arrange
        OrderDTO dto = new OrderDTO(1L, "PENDING");
        when(orderService.findById(1L)).thenReturn(dto);

        // Act & Assert
        mockMvc.perform(get("/orders/1"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.id").value(1L))
               .andExpect(jsonPath("$.status").value("PENDING"));
    }

    @Test
    @DisplayName("should return 404 when order is not found")
    void shouldReturn404_whenOrderNotFound() throws Exception {
        // Arrange
        when(orderService.findById(99L)).thenThrow(new NotFoundException("Not found"));

        // Act & Assert
        mockMvc.perform(get("/orders/99"))
               .andExpect(status().isNotFound());
    }
}
```

#### Repository con @DataJpaTest
```java
@DataJpaTest
class OrderRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private OrderRepository orderRepository;

    @Test
    @DisplayName("should find order by status")
    void shouldFindOrderByStatus() {
        // Arrange
        Order order = new Order(null, "PENDING");
        entityManager.persistAndFlush(order);

        // Act
        List<Order> results = orderRepository.findByStatus("PENDING");

        // Assert
        assertFalse(results.isEmpty());
        assertEquals("PENDING", results.get(0).getStatus());
    }
}
```

#### Verificaciones con Mockito
```java
// Verificar número exacto de llamadas
verify(repository, times(1)).save(any(Order.class));

// Verificar que nunca se llamó
verify(emailService, never()).sendEmail(anyString());

// Verificar orden de llamadas
InOrder inOrder = inOrder(repositoryA, repositoryB);
inOrder.verify(repositoryA).save(any());
inOrder.verify(repositoryB).update(any());

// Capturar argumento
ArgumentCaptor<Order> captor = ArgumentCaptor.forClass(Order.class);
verify(repository).save(captor.capture());
assertEquals("PENDING", captor.getValue().getStatus());

// Simular excepción en void
doThrow(new RuntimeException("DB error")).when(repository).delete(any());

// Simular llamada void exitosa
doNothing().when(repository).delete(any());
```

---

### Paso 5 — Imports estándar

Siempre incluir al inicio de la clase de test:

```java
// JUnit 5
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.*;

// Mockito
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.mockito.ArgumentMatchers.*;
import org.mockito.ArgumentCaptor;

// Spring MockMvc (solo para Controllers)
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
```

---

### Paso 6 — Dependencias Maven requeridas

Si el usuario necesita agregar dependencias, incluir en `pom.xml`:

```xml
<!-- Spring Boot Test (incluye JUnit 5 + Mockito automáticamente) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- H2 para @DataJpaTest -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>
```

---

## Casos de Prueba a Generar (por defecto)

Para cada método público, generar:

| Escenario | Descripción |
|-----------|-------------|
| **Happy Path** | Entrada válida → resultado esperado |
| **Null / Empty** | Entrada nula o colección vacía |
| **Not Found** | Recurso inexistente → excepción |
| **Invalid Input** | Validaciones fallidas → excepción o error |
| **Side Effects** | Verificar llamadas a dependencias con `verify()` |

---

## Nomenclatura de Archivos

- La clase de test va en: `src/test/java/<mismo-paquete-que-la-clase>/`
- Nombre: `<ClaseOriginal>Test.java`
- Ejemplo: `OrderService.java` → `OrderServiceTest.java`

---

## Reglas de Calidad

```
NO usar @SpringBootTest para tests unitarios puros
NO usar Thread.sleep() en tests
NO compartir estado mutable entre tests (cada @Test es independiente)
SIEMPRE usar @DisplayName con descripción legible
SIEMPRE hacer assert específico (NO solo assertTrue(result != null))
SI el método retorna void → verificar con verify() y/o assertThrows()
SI hay más de 5 parámetros similares → usar @ParameterizedTest con @MethodSource
```

---

## Formato de Salida

1. Bloque de código Java completo con la clase de test
2. Sección de imports (si no están en el bloque principal)
3. Dependencias Maven a agregar (si aplica)
4. Notas de cobertura: qué escenarios están cubiertos y cuáles se podrían agregar
