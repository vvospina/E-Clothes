import httpClient from "../../../shared/services/httpClient.js";
import { env } from "../../../config/env.js";
import { createMockResource } from "../../../shared/mocks/mockClient.js";
import { prendasSeed } from "../../../shared/mocks/fixtures/prendas.js";

// Ruta estable del contrato: POST/GET /api/v1/prendas, PUT/DELETE /api/v1/prendas/{id}
const PRENDAS_ENDPOINT = "/prendas/";

const mockResource = createMockResource(prendasSeed);

/**
 * Lista las prendas publicadas.
 */
export async function listPrendas({ signal } = {}) {
  if (env.mocks.prendas) {
    return mockResource.list();
  }
  const response = await httpClient.get(PRENDAS_ENDPOINT, { signal });
  return response.data;
}

/**
 * Crea una nueva prenda.
 */
export async function createPrenda(prenda) {
  if (env.mocks.prendas) {
    return mockResource.create(prenda);
  }
  const response = await httpClient.post(PRENDAS_ENDPOINT, prenda);
  return response.data;
}

/**
 * Edita los campos modificables de una prenda.
 */
export async function updatePrenda(id, prenda) {
  if (env.mocks.prendas) {
    return mockResource.update(id, prenda);
  }
  const response = await httpClient.put(`${PRENDAS_ENDPOINT}${id}/`, prenda);
  return response.data;
}

/**
 * Elimina una prenda publicada.
 */
export async function deletePrenda(id) {
  if (env.mocks.prendas) {
    return mockResource.remove(id);
  }
  await httpClient.delete(`${PRENDAS_ENDPOINT}${id}/`);
}
