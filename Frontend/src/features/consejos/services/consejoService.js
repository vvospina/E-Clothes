import httpClient from "../../../shared/services/httpClient.js";
import { env } from "../../../config/env.js";
import { createMockResource } from "../../../shared/mocks/mockClient.js";
import { consejosSeed } from "../../../shared/mocks/fixtures/consejos.js";

// Ruta estable del contrato: POST/GET /api/v1/consejos (con ?categoria= opcional)
const CONSEJOS_ENDPOINT = "/consejos/";

const mockResource = createMockResource(consejosSeed, {
  matchesFilters: (item, { categoria } = {}) =>
    !categoria || item.categoria.toLowerCase() === categoria.toLowerCase(),
});

/**
 * Lista los consejos de cuidado ambiental. Acepta un filtro opcional por
 * categoría, igual que el query parameter del contrato (?categoria=).
 */
export async function listConsejos({ categoria, signal } = {}) {
  if (env.mocks.consejos) {
    return mockResource.list({ categoria });
  }

  const response = await httpClient.get(CONSEJOS_ENDPOINT, {
    signal,
    params: categoria ? { categoria } : undefined,
  });
  return response.data;
}

/**
 * Consulta un consejo específico.
 */
export async function getConsejo(id) {
  if (env.mocks.consejos) {
    return mockResource.getById(id);
  }
  const response = await httpClient.get(`${CONSEJOS_ENDPOINT}${id}/`);
  return response.data;
}

/**
 * Crea un nuevo consejo ambiental.
 */
export async function createConsejo(consejo) {
  if (env.mocks.consejos) {
    return mockResource.create(consejo);
  }
  const response = await httpClient.post(CONSEJOS_ENDPOINT, consejo);
  return response.data;
}
