/**
 * Simulador mínimo de un recurso REST.
 *
 * El Taller de descomposición en microservicios exige que el frontend pueda
 * probarse con mocks mientras las APIs reales no cumplen todavía el contrato
 * aprobado (Fase 1, regla 3). Cada feature crea su propio mock a partir de un
 * arreglo semilla; el estado vive solo en memoria durante la sesión del
 * navegador y se reinicia al recargar la página.
 */

const SIMULATED_LATENCY_MS = 350;

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function cloneAll(items) {
  return items.map((item) => ({ ...item }));
}

function generateId() {
  return typeof crypto !== "undefined" && crypto.randomUUID
    ? crypto.randomUUID()
    : `mock-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

/**
 * Crea un recurso simulado con las operaciones list, getById, create, update
 * y remove. `matchesFilters` permite reutilizar la misma lógica de filtrado
 * que tendría el backend real (por query params).
 */
export function createMockResource(seedData, { matchesFilters } = {}) {
  let store = cloneAll(seedData);

  async function list(params = {}) {
    await wait(SIMULATED_LATENCY_MS);
    if (matchesFilters) {
      return store.filter((item) => matchesFilters(item, params));
    }
    return cloneAll(store);
  }

  async function getById(id) {
    await wait(SIMULATED_LATENCY_MS);
    const found = store.find((item) => String(item.id) === String(id));
    if (!found) {
      const error = new Error("Recurso no encontrado en el mock.");
      error.response = { status: 404, data: { detail: "No encontrado." } };
      throw error;
    }
    return { ...found };
  }

  async function create(payload) {
    await wait(SIMULATED_LATENCY_MS);
    const created = {
      id: generateId(),
      fechaCreacion: new Date().toISOString(),
      ...payload,
    };
    store = [created, ...store];
    return { ...created };
  }

  async function update(id, payload) {
    await wait(SIMULATED_LATENCY_MS);
    let updated = null;
    store = store.map((item) => {
      if (String(item.id) === String(id)) {
        updated = { ...item, ...payload };
        return updated;
      }
      return item;
    });
    if (!updated) {
      const error = new Error("Recurso no encontrado en el mock.");
      error.response = { status: 404, data: { detail: "No encontrado." } };
      throw error;
    }
    return updated;
  }

  async function remove(id) {
    await wait(SIMULATED_LATENCY_MS);
    store = store.filter((item) => String(item.id) !== String(id));
  }

  return { list, getById, create, update, remove };
}
