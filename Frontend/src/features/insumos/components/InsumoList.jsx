/**
 * Lista presentacional de insumos publicados.
 */
export default function InsumoList({ items, onEdit, onDelete }) {
  if (items.length === 0) {
    return <p className="text-muted mb-0">No hay insumos registrados todavía.</p>;
  }

  return (
    <div className="list-group list-group-flush">
      {items.map((item) => (
        <article key={item.id} className="list-group-item px-0 py-3">
          <div className="d-flex justify-content-between gap-3 flex-wrap">
            <div>
              <h3 className="h6 mb-1">{item.nombre}</h3>
              <p className="mb-1 text-muted small">{item.descripcion}</p>
              <p className="mb-1">
                Cantidad: {item.cantidad} {item.unidad} · Categoría: {item.categoria}
              </p>
            </div>
            <div className="text-end">
              {item.estado && (
                <span
                  className={`badge mb-2 d-block ${
                    item.estado === "activo" ? "text-bg-success" : "text-bg-secondary"
                  }`}
                >
                  {item.estado}
                </span>
              )}
              <div className="btn-group btn-group-sm" role="group">
                <button
                  type="button"
                  className="btn btn-outline-primary"
                  onClick={() => onEdit(item)}
                >
                  Editar
                </button>
                <button
                  type="button"
                  className="btn btn-outline-danger"
                  onClick={() => onDelete(item)}
                >
                  Eliminar
                </button>
              </div>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}
