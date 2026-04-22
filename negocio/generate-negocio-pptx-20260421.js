const path = require("path");
const PptxGenJS = require("pptxgenjs");

const pptx = new PptxGenJS();

pptx.layout = "LAYOUT_16x9";
pptx.author = "GitHub Copilot";
pptx.company = "REORI CORP S.A.C.";
pptx.subject = "Resumen ejecutivo para reunion con Gerencia";
pptx.title = "Pachamama - Costos y Escalamiento Cloud";
pptx.lang = "es-PE";

const theme = {
  forest: "2C5F2D",
  moss: "97BC62",
  cream: "F7F4EA",
  sand: "E7E2D3",
  charcoal: "243127",
  clay: "B85042",
  gold: "C99700",
  white: "FFFFFF",
  mist: "EEF2EA",
  muted: "6A7367",
  line: "D8D2C1",
};

function addFooter(slide, text, dark = false) {
  slide.addText(text, {
    x: 0.55,
    y: 5.18,
    w: 8.9,
    h: 0.18,
    fontFace: "Calibri",
    fontSize: 9,
    color: dark ? "DDE5D8" : theme.muted,
    margin: 0,
    align: "left",
  });
}

function addTitle(slide, title, subtitle = "", dark = false) {
  slide.addText(title, {
    x: 0.55,
    y: 0.35,
    w: 6.8,
    h: 0.55,
    fontFace: "Georgia",
    fontSize: 28,
    bold: true,
    color: dark ? theme.white : theme.charcoal,
    margin: 0,
  });

  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.55,
      y: 0.93,
      w: 7.2,
      h: 0.24,
      fontFace: "Calibri",
      fontSize: 10,
      color: dark ? "DDE5D8" : theme.muted,
      margin: 0,
    });
  }
}

function addPill(slide, text, x, y, w, fill, color) {
  slide.addShape("roundRect", {
    x,
    y,
    w,
    h: 0.28,
    rectRadius: 0.08,
    line: { color: fill, transparency: 100 },
    fill: { color: fill },
  });

  slide.addText(text, {
    x: x + 0.08,
    y: y + 0.04,
    w: w - 0.16,
    h: 0.16,
    fontFace: "Calibri",
    fontSize: 9,
    bold: true,
    color,
    margin: 0,
    align: "center",
  });
}

function addCard(slide, options) {
  slide.addShape("roundRect", {
    x: options.x,
    y: options.y,
    w: options.w,
    h: options.h,
    rectRadius: 0.06,
    line: { color: options.line || theme.line, width: 1 },
    fill: { color: options.fill || theme.white },
    shadow: { type: "outer", color: "000000", blur: 2, offset: 1, angle: 45, opacity: 0.12 },
  });
}

function addBulletList(slide, items, box) {
  const runs = [];
  items.forEach((item, index) => {
    runs.push({
      text: item,
      options: { bullet: true, breakLine: index < items.length - 1 },
    });
  });
  slide.addText(runs, {
    x: box.x,
    y: box.y,
    w: box.w,
    h: box.h,
    fontFace: "Calibri",
    fontSize: 12,
    color: box.color || theme.charcoal,
    breakLine: true,
    margin: 0,
    paraSpaceAfterPt: 6,
    valign: "top",
  });
}

function addStageCard(slide, stage) {
  addCard(slide, {
    x: stage.x,
    y: stage.y,
    w: stage.w,
    h: stage.h,
    fill: theme.white,
  });

  slide.addShape("rect", {
    x: stage.x,
    y: stage.y,
    w: stage.w,
    h: 0.16,
    line: { color: stage.color, transparency: 100 },
    fill: { color: stage.color },
  });

  slide.addText(stage.title, {
    x: stage.x + 0.18,
    y: stage.y + 0.28,
    w: stage.w - 0.36,
    h: 0.22,
    fontFace: "Georgia",
    fontSize: 16,
    bold: true,
    color: theme.charcoal,
    margin: 0,
    align: "left",
  });

  slide.addText(stage.band, {
    x: stage.x + 0.18,
    y: stage.y + 0.62,
    w: stage.w - 0.36,
    h: 0.55,
    fontFace: "Calibri",
    fontSize: 20,
    bold: true,
    color: stage.color,
    margin: 0,
  });

  slide.addText(stage.years, {
    x: stage.x + 0.18,
    y: stage.y + 1.18,
    w: stage.w - 0.36,
    h: 0.2,
    fontFace: "Calibri",
    fontSize: 10,
    color: theme.muted,
    margin: 0,
  });

  slide.addText(stage.summary, {
    x: stage.x + 0.18,
    y: stage.y + 1.47,
    w: stage.w - 0.36,
    h: 0.44,
    fontFace: "Calibri",
    fontSize: 11,
    color: theme.charcoal,
    margin: 0,
    fit: "shrink",
  });

  addPill(slide, stage.tag, stage.x + 0.18, stage.y + 2.02, stage.w - 0.36, stage.pillFill, stage.pillText);
}

function addYearNode(slide, node) {
  slide.addShape("ellipse", {
    x: node.x,
    y: 1.9,
    w: 0.34,
    h: 0.34,
    line: { color: node.color, width: 2 },
    fill: { color: theme.white },
  });

  slide.addShape("line", {
    x: node.x + 0.34,
    y: 2.07,
    w: 1.28,
    h: 0,
    line: { color: theme.line, width: 1.5 },
  });

  slide.addText(node.year, {
    x: node.x - 0.08,
    y: 1.5,
    w: 0.54,
    h: 0.2,
    fontFace: "Georgia",
    fontSize: 12,
    bold: true,
    color: theme.charcoal,
    margin: 0,
    align: "center",
  });

  addCard(slide, {
    x: node.x - 0.22,
    y: 2.42,
    w: 1.36,
    h: 1.5,
    fill: node.fill,
    line: node.line,
  });

  slide.addText(node.clients, {
    x: node.x - 0.08,
    y: 2.66,
    w: 1.08,
    h: 0.32,
    fontFace: "Calibri",
    fontSize: 18,
    bold: true,
    color: node.color,
    margin: 0,
    align: "center",
  });

  slide.addText("clientes", {
    x: node.x - 0.08,
    y: 2.97,
    w: 1.08,
    h: 0.18,
    fontFace: "Calibri",
    fontSize: 9,
    color: theme.muted,
    margin: 0,
    align: "center",
  });

  slide.addText(node.collectors, {
    x: node.x - 0.08,
    y: 3.25,
    w: 1.08,
    h: 0.3,
    fontFace: "Calibri",
    fontSize: 15,
    bold: true,
    color: theme.charcoal,
    margin: 0,
    align: "center",
  });

  slide.addText("recolectores", {
    x: node.x - 0.08,
    y: 3.53,
    w: 1.08,
    h: 0.18,
    fontFace: "Calibri",
    fontSize: 9,
    color: theme.muted,
    margin: 0,
    align: "center",
  });
}

function addRiskCard(slide, risk) {
  addCard(slide, {
    x: risk.x,
    y: risk.y,
    w: risk.w,
    h: risk.h,
    fill: theme.white,
  });

  slide.addText(risk.title, {
    x: risk.x + 0.16,
    y: risk.y + 0.14,
    w: risk.w - 0.32,
    h: 0.28,
    fontFace: "Georgia",
    fontSize: 13,
    bold: true,
    color: theme.charcoal,
    margin: 0,
  });

  slide.addText(risk.body, {
    x: risk.x + 0.16,
    y: risk.y + 0.48,
    w: risk.w - 0.32,
    h: 0.7,
    fontFace: "Calibri",
    fontSize: 10,
    color: theme.charcoal,
    margin: 0,
    fit: "shrink",
  });

  addPill(slide, risk.tag, risk.x + 0.16, risk.y + 1.25, risk.w - 0.32, risk.fill, risk.textColor);
}

// Slide 1
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.forest };

  slide.addShape("rect", {
    x: 6.9,
    y: 0,
    w: 3.1,
    h: 5.625,
    line: { color: theme.moss, transparency: 100 },
    fill: { color: theme.moss },
  });

  slide.addShape("rect", {
    x: 7.25,
    y: 0.4,
    w: 2.4,
    h: 4.82,
    line: { color: theme.cream, transparency: 100 },
    fill: { color: theme.cream },
  });

  slide.addText("Pachamama", {
    x: 0.6,
    y: 0.72,
    w: 4.2,
    h: 0.55,
    fontFace: "Georgia",
    fontSize: 28,
    bold: true,
    color: theme.white,
    margin: 0,
  });

  slide.addText("Costos y escalamiento cloud\npara reunion con Gerencia", {
    x: 0.6,
    y: 1.42,
    w: 5.3,
    h: 1.15,
    fontFace: "Georgia",
    fontSize: 22,
    bold: true,
    color: "E9F2E3",
    margin: 0,
    fit: "shrink",
  });

  slide.addText("Resumen ejecutivo basado en la proyeccion 2026-2030 y en el escenario base con plataforma escalada.", {
    x: 0.6,
    y: 2.82,
    w: 5.45,
    h: 0.72,
    fontFace: "Calibri",
    fontSize: 15,
    color: "DDE5D8",
    margin: 0,
    fit: "shrink",
  });

  addPill(slide, "Decision sugerida: Opcion A ahora, Opcion B en 2028", 0.6, 4.17, 3.92, theme.gold, theme.charcoal);

  slide.addText("21 abril 2026", {
    x: 0.6,
    y: 4.66,
    w: 2.0,
    h: 0.2,
    fontFace: "Calibri",
    fontSize: 10,
    color: "DDE5D8",
    margin: 0,
  });

  const metrics = [
    { y: 0.84, value: "84", label: "clientes al 2030" },
    { y: 2.16, value: "46,800", label: "recolectores al 2030" },
    { y: 3.48, value: "USD 2,327", label: "referencia mensual 2030" },
  ];

  metrics.forEach((metric) => {
    slide.addText(metric.value, {
      x: 7.55,
      y: metric.y,
      w: 1.8,
      h: 0.38,
      fontFace: "Calibri",
      fontSize: 24,
      bold: true,
      color: theme.forest,
      margin: 0,
      align: "center",
    });
    slide.addText(metric.label, {
      x: 7.55,
      y: metric.y + 0.42,
      w: 1.8,
      h: 0.3,
      fontFace: "Calibri",
      fontSize: 10,
      color: theme.charcoal,
      margin: 0,
      align: "center",
      fit: "shrink",
    });
  });

  addFooter(slide, "Fuente: NEGOCIO-PACHAMAMA-20260421.md", true);
}

// Slide 2
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.cream };
  addTitle(slide, "La decision en una sola lamina", "Tres etapas, una ruta economica clara.");

  const stageCards = [
    {
      x: 0.55,
      y: 1.45,
      w: 2.75,
      h: 2.45,
      title: "Opcion A",
      band: "USD 607 - 855",
      years: "Tramo 2026-2027",
      summary: "Arranque controlado, velocidad y medicion real del negocio antes de encarecer la operacion.",
      tag: "Recomendada ahora",
      color: theme.forest,
      pillFill: "DCEBCF",
      pillText: theme.forest,
    },
    {
      x: 3.62,
      y: 1.45,
      w: 2.75,
      h: 2.45,
      title: "Opcion B",
      band: "USD 1,402 - 1,859",
      years: "Tramo 2028-2029",
      summary: "Mas gobierno y control cuando el crecimiento ya exige disciplina sobre datos, APIs y monitoreo.",
      tag: "Hito formal 2028",
      color: theme.gold,
      pillFill: "F7E8BB",
      pillText: theme.charcoal,
    },
    {
      x: 6.69,
      y: 1.45,
      w: 2.75,
      h: 2.45,
      title: "Opcion C",
      band: "Desde USD 2,327",
      years: "Tramo 2030+",
      summary: "Continuidad reforzada solo si contratos, compliance o riesgo justifican una capa enterprise.",
      tag: "No activar por intuicion",
      color: theme.clay,
      pillFill: "F4D8D3",
      pillText: theme.clay,
    },
  ];

  stageCards.forEach((stage) => addStageCard(slide, stage));

  addCard(slide, { x: 0.55, y: 4.23, w: 8.9, h: 0.62, fill: theme.mist, line: "D7E2D0" });
  slide.addText("Mensaje para Gerencia: no estamos aprobando una plataforma cara desde el inicio; estamos aprobando una ruta para invertir solo cuando el negocio lo pague o el riesgo lo exija.", {
    x: 0.78,
    y: 4.41,
    w: 8.45,
    h: 0.22,
    fontFace: "Calibri",
    fontSize: 12,
    bold: true,
    color: theme.charcoal,
    margin: 0,
    align: "center",
    fit: "shrink",
  });

  addFooter(slide, "Bandas de referencia: escenario base con plataforma escalada.");
}

// Slide 3
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.white };
  addTitle(slide, "La escala ya tiene forma", "La proyeccion 2026-2030 permite decidir con tiempo, no con intuicion.");

  const nodes = [
    { year: "2026", x: 0.82, clients: "13", collectors: "7,800", color: theme.forest, fill: theme.white, line: theme.line },
    { year: "2027", x: 2.45, clients: "23", collectors: "15,000", color: theme.forest, fill: theme.white, line: theme.line },
    { year: "2028", x: 4.08, clients: "40", collectors: "24,600", color: theme.gold, fill: "FFF8E4", line: "E8D59D" },
    { year: "2029", x: 5.71, clients: "61", collectors: "35,400", color: theme.gold, fill: "FFF8E4", line: "E8D59D" },
    { year: "2030", x: 7.34, clients: "84", collectors: "46,800", color: theme.clay, fill: "FCEAE6", line: "E7BEB5" },
  ];

  nodes.forEach((node, index) => {
    addYearNode(slide, node);
    if (index === nodes.length - 1) {
      slide.addShape("line", {
        x: node.x + 0.34,
        y: 2.07,
        w: 0.8,
        h: 0,
        line: { color: theme.line, width: 1.5, dash: "dash" },
      });
    }
  });

  addCard(slide, { x: 0.7, y: 4.28, w: 2.65, h: 0.56, fill: theme.mist, line: "D7E2D0" });
  slide.addText("30 recolectores por comunidad se mantiene estable.", {
    x: 0.86,
    y: 4.46,
    w: 2.3,
    h: 0.16,
    fontFace: "Calibri",
    fontSize: 10,
    color: theme.charcoal,
    margin: 0,
    align: "center",
    fit: "shrink",
  });

  addCard(slide, { x: 3.64, y: 4.28, w: 2.65, h: 0.56, fill: "FFF8E4", line: "E8D59D" });
  slide.addText("2028 deja de ser un supuesto: ya es un hito de escala.", {
    x: 3.8,
    y: 4.46,
    w: 2.3,
    h: 0.16,
    fontFace: "Calibri",
    fontSize: 10,
    color: theme.charcoal,
    margin: 0,
    align: "center",
    fit: "shrink",
  });

  addCard(slide, { x: 6.58, y: 4.28, w: 2.65, h: 0.56, fill: "FCEAE6", line: "E7BEB5" });
  slide.addText("2030 es una decision de continuidad, no de moda tecnica.", {
    x: 6.74,
    y: 4.46,
    w: 2.3,
    h: 0.16,
    fontFace: "Calibri",
    fontSize: 10,
    color: theme.charcoal,
    margin: 0,
    align: "center",
    fit: "shrink",
  });

  addFooter(slide, "Fuente: proyeccion comercial 2026-2030.");
}

// Slide 4
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.cream };
  addTitle(slide, "Cuanto cuesta en el escenario base", "Costo total mensual de referencia con plataforma escalada.");

  const values = [606.97, 854.52, 1402.16, 1859.3, 2327.05];
  const years = ["2026", "2027", "2028", "2029", "2030"];
  const colors = [theme.forest, theme.forest, theme.gold, theme.gold, theme.clay];
  const chartBaseY = 4.42;
  const maxHeight = 2.45;
  const maxValue = 2400;
  const startX = 1.02;
  const barW = 0.56;
  const gap = 0.46;

  slide.addShape("rect", {
    x: 0.72,
    y: 1.3,
    w: 5.95,
    h: 3.5,
    line: { color: "E5DED0", width: 1 },
    fill: { color: theme.white },
  });

  slide.addShape("line", {
    x: 1.0,
    y: chartBaseY,
    w: 5.35,
    h: 0,
    line: { color: theme.line, width: 1.2 },
  });

  values.forEach((value, index) => {
    const barH = (value / maxValue) * maxHeight;
    const x = startX + index * (barW + gap);
    const y = chartBaseY - barH;
    slide.addShape("roundRect", {
      x,
      y,
      w: barW,
      h: barH,
      rectRadius: 0.03,
      line: { color: colors[index], transparency: 100 },
      fill: { color: colors[index] },
    });
    slide.addText(`USD ${value.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`, {
      x: x - 0.08,
      y: y - 0.24,
      w: 0.84,
      h: 0.18,
      fontFace: "Calibri",
      fontSize: 9,
      bold: true,
      color: theme.charcoal,
      margin: 0,
      align: "center",
    });
    slide.addText(years[index], {
      x: x - 0.01,
      y: 4.5,
      w: 0.58,
      h: 0.18,
      fontFace: "Calibri",
      fontSize: 10,
      color: theme.muted,
      margin: 0,
      align: "center",
    });
  });

  addCard(slide, { x: 6.92, y: 1.3, w: 2.54, h: 3.5, fill: theme.white, line: theme.line });
  slide.addText("Lo que cambia", {
    x: 7.18,
    y: 1.58,
    w: 1.95,
    h: 0.24,
    fontFace: "Georgia",
    fontSize: 16,
    bold: true,
    color: theme.charcoal,
    margin: 0,
  });

  addBulletList(slide, [
    "2026-2027: banda manejable para iniciar.",
    "2028: el salto obliga a revisar gobierno.",
    "2029-2030: continuidad y riesgo entran en la conversacion.",
  ], { x: 7.18, y: 2.0, w: 1.95, h: 1.15 });

  addPill(slide, "Punto de inflexion: 2028", 7.18, 3.58, 1.95, theme.gold, theme.charcoal);

  slide.addText("La subida no viene solo de almacenar mas archivos. Tambien crecen la base de datos, el procesamiento y el monitoreo.", {
    x: 7.18,
    y: 3.98,
    w: 1.95,
    h: 0.52,
    fontFace: "Calibri",
    fontSize: 10,
    color: theme.charcoal,
    margin: 0,
    fit: "shrink",
  });

  addFooter(slide, "Fuente: escenario base escalado del anexo economico.");
}

// Slide 5
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.white };
  addTitle(slide, "Como se decide A / B / C", "La ruta cambia cuando cambian el costo, el control requerido y el riesgo del negocio.");

  const lanes = [
    {
      title: "Mantener Opcion A",
      subtitle: "Hasta aprox. USD 855 / mes",
      body: "Cuando la prioridad es velocidad, control de margen y medicion real por cliente.",
      y: 1.35,
      fill: "EDF6E7",
      line: "C9DDBA",
      color: theme.forest,
    },
    {
      title: "Activar Opcion B",
      subtitle: "Desde aprox. USD 1,402 / mes",
      body: "Cuando el crecimiento ya exige gobierno de APIs, datos y observabilidad mas fuerte.",
      y: 2.45,
      fill: "FFF8E4",
      line: "E8D59D",
      color: theme.gold,
    },
    {
      title: "Evaluar Opcion C",
      subtitle: "Desde aprox. USD 2,327 / mes",
      body: "Solo si se agregan exigencias de SLA, compliance, continuidad o costo alto de falla.",
      y: 3.55,
      fill: "FCEAE6",
      line: "E7BEB5",
      color: theme.clay,
    },
  ];

  lanes.forEach((lane) => {
    addCard(slide, { x: 0.72, y: lane.y, w: 8.55, h: 0.84, fill: lane.fill, line: lane.line });
    slide.addText(lane.title, {
      x: 0.95,
      y: lane.y + 0.16,
      w: 2.25,
      h: 0.2,
      fontFace: "Georgia",
      fontSize: 15,
      bold: true,
      color: lane.color,
      margin: 0,
    });
    slide.addText(lane.subtitle, {
      x: 3.0,
      y: lane.y + 0.17,
      w: 2.0,
      h: 0.18,
      fontFace: "Calibri",
      fontSize: 11,
      bold: true,
      color: theme.charcoal,
      margin: 0,
      align: "center",
    });
    slide.addText(lane.body, {
      x: 5.15,
      y: lane.y + 0.15,
      w: 3.72,
      h: 0.42,
      fontFace: "Calibri",
      fontSize: 10,
      color: theme.charcoal,
      margin: 0,
      fit: "shrink",
    });
  });

  addCard(slide, { x: 0.72, y: 4.66, w: 8.55, h: 0.44, fill: theme.mist, line: "D7E2D0" });
  slide.addText("Regla de Gerencia: no subir de etapa antes de tiempo, pero tampoco esperar a que el crecimiento encuentre una plataforma subgobernada.", {
    x: 0.95,
    y: 4.82,
    w: 8.1,
    h: 0.14,
    fontFace: "Calibri",
    fontSize: 11,
    bold: true,
    color: theme.charcoal,
    margin: 0,
    align: "center",
    fit: "shrink",
  });

  addFooter(slide, "La arquitectura propuesta es una secuencia de decisiones, no una unica compra inicial.");
}

// Slide 6
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.cream };
  addTitle(slide, "Que gana el negocio con esta ruta", "Valor economico y control, no solo tecnologia.");

  const benefits = [
    {
      x: 0.72,
      y: 1.45,
      title: "Pricing defendible",
      body: "La conversacion comercial puede pasar a cargo base + consumo variable sin vender por debajo del costo.",
      fill: theme.white,
    },
    {
      x: 5.05,
      y: 1.45,
      title: "Inversion en el momento correcto",
      body: "No se inmoviliza margen en infraestructura enterprise antes de tener contratos o demanda que la paguen.",
      fill: theme.white,
    },
    {
      x: 0.72,
      y: 3.12,
      title: "Visibilidad por cliente",
      body: "Se vuelve posible medir cuanto consume cada cliente y donde se concentran archivos, actividad y retencion.",
      fill: theme.white,
    },
    {
      x: 5.05,
      y: 3.12,
      title: "Ruta para servicios premium",
      body: "La Opcion C queda reservada para ofertas o contratos con continuidad reforzada y mayor valor.",
      fill: theme.white,
    },
  ];

  benefits.forEach((benefit) => {
    addCard(slide, { x: benefit.x, y: benefit.y, w: 3.95, h: 1.3, fill: benefit.fill, line: theme.line });
    slide.addText(benefit.title, {
      x: benefit.x + 0.18,
      y: benefit.y + 0.18,
      w: 3.55,
      h: 0.2,
      fontFace: "Georgia",
      fontSize: 15,
      bold: true,
      color: theme.charcoal,
      margin: 0,
    });
    slide.addText(benefit.body, {
      x: benefit.x + 0.18,
      y: benefit.y + 0.5,
      w: 3.55,
      h: 0.52,
      fontFace: "Calibri",
      fontSize: 11,
      color: theme.charcoal,
      margin: 0,
      fit: "shrink",
    });
  });

  addCard(slide, { x: 1.0, y: 4.72, w: 7.98, h: 0.3, fill: theme.forest, line: theme.forest });
  slide.addText("Resultado esperado: mejor margen, mejor narrativa comercial y una inversion cloud que madura al ritmo del negocio.", {
    x: 1.2,
    y: 4.81,
    w: 7.58,
    h: 0.1,
    fontFace: "Calibri",
    fontSize: 11,
    bold: true,
    color: theme.white,
    margin: 0,
    align: "center",
    fit: "shrink",
  });

  addFooter(slide, "El valor de la ruta propuesta es financiero, comercial y operativo.");
}

// Slide 7
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.white };
  addTitle(slide, "Los riesgos que si importan a Gerencia", "Cinco puntos que mueven margen, reputacion o capacidad de ejecucion.");

  const risks = [
    {
      x: 0.72,
      y: 1.35,
      w: 2.86,
      h: 1.58,
      title: "Pricing por debajo del costo",
      body: "Si no se recupera la retencion y el uso real, el crecimiento comercial puede destruir margen.",
      tag: "Mitigar con cargo base + variable",
      fill: "FCEAE6",
      textColor: theme.clay,
    },
    {
      x: 3.58,
      y: 1.35,
      w: 2.86,
      h: 1.58,
      title: "Enterprise antes de tiempo",
      body: "Activar la capa mas cara demasiado pronto elevaria el costo fijo sin retorno equivalente.",
      tag: "Mantener Opcion C condicionada",
      fill: "FFF8E4",
      textColor: theme.charcoal,
    },
    {
      x: 6.44,
      y: 1.35,
      w: 2.86,
      h: 1.58,
      title: "Retencion mal gobernada",
      body: "Fotos, videos y trazas pueden crecer mas rapido que la base transaccional si no se limpian o mueven de tier.",
      tag: "Definir lifecycle desde el inicio",
      fill: "FCEAE6",
      textColor: theme.clay,
    },
    {
      x: 2.15,
      y: 3.18,
      w: 2.86,
      h: 1.58,
      title: "Crecimiento sin gobierno",
      body: "Mas clientes sin mayor control sobre datos y monitoreo aumentan friccion y probabilidad de errores.",
      tag: "Usar 2028 como hito de gobierno",
      fill: "EDF6E7",
      textColor: theme.forest,
    },
    {
      x: 5.01,
      y: 3.18,
      w: 2.86,
      h: 1.58,
      title: "Medicion insuficiente",
      body: "Sin medidores por cliente y por actividad, las decisiones futuras vuelven a ser opinion y no evidencia.",
      tag: "Instrumentar desde la etapa A",
      fill: "EDF6E7",
      textColor: theme.forest,
    },
  ];

  risks.forEach((risk) => addRiskCard(slide, risk));
  addFooter(slide, "Cada riesgo del deck tiene una respuesta accionable, no solo una alerta.");
}

// Slide 8
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.charcoal };
  addTitle(slide, "Decisiones para esta reunion", "Lo que Gerencia puede aprobar hoy para no volver a discutir desde cero en 6 meses.", true);

  const actions = [
    "Aprobar Opcion A como base 2026-2027.",
    "Aceptar 2028 como hito formal para pasar a Opcion B.",
    "Definir pricing con cargo base y capa variable.",
    "Instrumentar medicion por cliente, recolector, actividad y archivo.",
    "Mantener Opcion C solo para continuidad, compliance o contratos premium.",
  ];

  actions.forEach((action, index) => {
    const y = 1.4 + index * 0.68;
    slide.addShape("ellipse", {
      x: 0.78,
      y: y,
      w: 0.34,
      h: 0.34,
      line: { color: theme.moss, transparency: 100 },
      fill: { color: theme.moss },
    });
    slide.addText(String(index + 1), {
      x: 0.78,
      y: y + 0.06,
      w: 0.34,
      h: 0.14,
      fontFace: "Calibri",
      fontSize: 11,
      bold: true,
      color: theme.charcoal,
      margin: 0,
      align: "center",
    });
    slide.addText(action, {
      x: 1.28,
      y: y + 0.03,
      w: 5.6,
      h: 0.24,
      fontFace: "Calibri",
      fontSize: 15,
      color: theme.white,
      margin: 0,
      fit: "shrink",
    });
  });

  addCard(slide, { x: 7.05, y: 1.28, w: 2.15, h: 2.95, fill: theme.cream, line: theme.cream });
  slide.addText("Mensaje final", {
    x: 7.3,
    y: 1.56,
    w: 1.65,
    h: 0.22,
    fontFace: "Georgia",
    fontSize: 15,
    bold: true,
    color: theme.forest,
    margin: 0,
    align: "center",
  });
  slide.addText("La mejor decision no es comprar la plataforma mas robusta.\n\nLa mejor decision es aprobar una ruta que invierte por etapas y protege margen mientras el negocio crece.", {
    x: 7.28,
    y: 2.02,
    w: 1.7,
    h: 1.34,
    fontFace: "Calibri",
    fontSize: 12,
    color: theme.charcoal,
    margin: 0,
    align: "center",
    fit: "shrink",
  });
  addPill(slide, "A ahora / B en 2028", 7.28, 3.62, 1.7, theme.gold, theme.charcoal);

  addFooter(slide, "Deck ejecutivo generado desde el resumen NEGOCIO-PACHAMAMA-20260421.", true);
}

const outputFile = path.join(__dirname, "NEGOCIO-PACHAMAMA-20260421.pptx");

pptx.writeFile({ fileName: outputFile }).then(() => {
  console.log(`PPTX generado: ${outputFile}`);
}).catch((error) => {
  console.error(error);
  process.exit(1);
});