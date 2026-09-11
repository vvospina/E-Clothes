/**
 * Semilla del mock de Sostenibilidad e impacto ambiental.
 * Atributos según la ficha del contrato: titulo, contenido, categoria.
 * El backend de Sara ya cumple el contrato (/api/v1/consejos), por lo que
 * este mock solo se usa si VITE_MOCK_CONSEJOS=true (por ejemplo, si el
 * microservicio no está corriendo localmente).
 */
export const consejosSeed = [
  {
    id: "con-001",
    titulo: "Lava tus prendas con agua fría",
    contenido:
      "Lavar con agua fría reduce el consumo energético y prolonga la vida de las fibras textiles.",
    categoria: "Cuidado de prendas",
  },
  {
    id: "con-002",
    titulo: "Dona antes de desechar",
    contenido:
      "Antes de botar una prenda en buen estado, considera donarla o venderla de segunda mano.",
    categoria: "Reutilización",
  },
  {
    id: "con-003",
    titulo: "Separa los textiles del resto de residuos",
    contenido:
      "Los textiles no deben mezclarse con la basura común; muchas ciudades tienen puntos de reciclaje textil.",
    categoria: "Reciclaje textil",
  },
];
