/**
 * Semilla del mock de Gestión de prendas.
 * Atributos según la ficha del contrato: nombre, descripcion, categoria,
 * cantidad, estado, fechaCreacion.
 */
export const prendasSeed = [
  {
    id: "pre-001",
    nombre: "Camisa de lino blanca",
    descripcion: "Camisa de segunda mano en buen estado, talla M.",
    categoria: "Camisa (Segunda mano)",
    cantidad: 1,
    estado: "activo",
    fechaCreacion: "2026-08-25T12:00:00.000Z",
  },
  {
    id: "pre-002",
    nombre: "Vestido floral",
    descripcion: "Vestido nuevo confeccionado con retazos reciclados.",
    categoria: "Vestido (nuevo)",
    cantidad: 3,
    estado: "activo",
    fechaCreacion: "2026-08-28T08:45:00.000Z",
  },
  {
    id: "pre-003",
    nombre: "Pantalón denim",
    descripcion: "Pantalón restaurado, requiere ajuste de bastilla.",
    categoria: "Pantalón (Segunda mano)",
    cantidad: 2,
    estado: "inactivo",
    fechaCreacion: "2026-08-15T17:20:00.000Z",
  },
];
