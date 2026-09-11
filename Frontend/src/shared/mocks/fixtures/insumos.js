/**
 * Semilla del mock de Gestión de insumos.
 * Atributos según la ficha del contrato: nombre, descripcion, categoria,
 * cantidad, unidad, estado, fechaCreacion.
 */
export const insumosSeed = [
  {
    id: "ins-001",
    nombre: "Retazos de algodón",
    descripcion: "Sobrantes de corte de algodón 100% para relleno o patchwork.",
    categoria: "Tela",
    cantidad: 25,
    unidad: "kg",
    estado: "activo",
    fechaCreacion: "2026-08-12T10:00:00.000Z",
  },
  {
    id: "ins-002",
    nombre: "Botones surtidos",
    descripcion: "Lote de botones plásticos y de nácar en distintos tamaños.",
    categoria: "Insumo de confección",
    cantidad: 480,
    unidad: "unidad",
    estado: "activo",
    fechaCreacion: "2026-08-20T15:30:00.000Z",
  },
  {
    id: "ins-003",
    nombre: "Hilo poliéster",
    descripcion: "Conos de hilo poliéster reciclado para costura industrial.",
    categoria: "Hilo",
    cantidad: 12,
    unidad: "kg",
    estado: "inactivo",
    fechaCreacion: "2026-07-30T09:15:00.000Z",
  },
];
