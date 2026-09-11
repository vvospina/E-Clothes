import httpClient from "../../../shared/services/httpClient.js";
import { env } from "../../../config/env.js";
import { createMockResource } from "../../../shared/mocks/mockClient.js";
import { materialesMercadoSeed } from "../../../shared/mocks/fixtures/materialesMercado.js";

// Ruta estable del contrato: GET /api/v1/materiales-mercado (con ?nombre= opcional)
const MATERIALES_MERCADO_ENDPOINT = "/materiales-mercado/";

const mockResource = createMockResource(materialesMercadoSeed, {
  matchesFilters: (item, { nombre } = {}) =>
    !nombre || item.nombre.toLowerCase().includes(nombre.toLowerCase()),
});

/**
 * Lista los materiales disponibles en el mercado. Acepta un filtro opcional
 * por nombre, igual que el query parameter del contrato (?nombre=).
 */
export async function listMaterialesMercado({ nombre, signal } = {}) {
  if (env.mocks.materialesMercado) {
    return mockResource.list({ nombre });
  }

  const response = await httpClient.get(MATERIALES_MERCADO_ENDPOINT, {
    signal,
    params: nombre ? { nombre } : undefined,
  });
  return response.data;
}

/**
 * Consulta la información de un material específico.
 */
export async function getMaterialMercado(id) {
  if (env.mocks.materialesMercado) {
    return mockResource.getById(id);
  }
  const response = await httpClient.get(`${MATERIALES_MERCADO_ENDPOINT}${id}/`);
  return response.data;
}
