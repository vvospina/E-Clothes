import httpClient from "../../../shared/services/httpClient.js";
import { env } from "../../../config/env.js";
import { createMockResource } from "../../../shared/mocks/mockClient.js";
import { insumosSeed } from "../../../shared/mocks/fixtures/insumos.js";

// Ruta estable del contrato: POST/GET /api/v1/insumos, GET/PUT/DELETE /api/v1/insumos/{id}
const INSUMOS_ENDPOINT = "/insumos/";

const mockResource = createMockResource(insumosSeed);

/**
 * Lista los insumos publicados.
 */
export async function listInsumos({ signal } = {}) {
  if (env.mocks.insumos) {
    return mockResource.list();
  }
  const response = await httpClient.get(INSUMOS_ENDPOINT, { signal });
  return response.data;
}

/**
 * Consulta un insumo específico.
 */
export async function getInsumo(id) {
  if (env.mocks.insumos) {
    return mockResource.getById(id);
  }
  const response = await httpClient.get(`${INSUMOS_ENDPOINT}${id}/`);
  return response.data;
}

/**
 * Crea un nuevo insumo.
 */
export async function createInsumo(insumo) {
  if (env.mocks.insumos) {
    return mockResource.create(insumo);
  }
  const response = await httpClient.post(INSUMOS_ENDPOINT, insumo);
  return response.data;
}

/**
 * Edita los campos modificables de un insumo.
 */
export async function updateInsumo(id, insumo) {
  if (env.mocks.insumos) {
    return mockResource.update(id, insumo);
  }
  const response = await httpClient.put(`${INSUMOS_ENDPOINT}${id}/`, insumo);
  return response.data;
}

/**
 * Elimina un insumo publicado.
 */
export async function deleteInsumo(id) {
  if (env.mocks.insumos) {
    return mockResource.remove(id);
  }
  await httpClient.delete(`${INSUMOS_ENDPOINT}${id}/`);
}
