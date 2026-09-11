const currencyFormatter = new Intl.NumberFormat("es-CO", {
  style: "currency",
  currency: "COP",
  maximumFractionDigits: 0,
});

/**
 * Lista presentacional de materiales disponibles en el mercado.
 */
export default function MaterialMercadoList({ items }) {
  if (items.length === 0) {
    return <p className="text-muted mb-0">No se encontraron materiales.</p>;
  }

  return (
    <div className="row g-3">
      {items.map((item) => (
        <div className="col-md-6" key={item.id}>
          <article className="card h-100 border-0 shadow-sm">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-start">
                <h3 className="h6 mb-1">{item.nombre}</h3>
                <span className="badge text-bg-light">{item.tipo}</span>
              </div>
              <p className="text-muted small mb-2">{item.descripcion}</p>
              <p className="fw-semibold mb-0 text-success">
                {currencyFormatter.format(item.precioEstimado)}
              </p>
            </div>
          </article>
        </div>
      ))}
    </div>
  );
}
