import { useState } from "react";

/**
 * Barra de filtro por nombre. Delega la búsqueda a la página contenedora.
 */
export default function MaterialMercadoFilter({ onFilter, isLoading }) {
  const [nombre, setNombre] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    onFilter(nombre.trim());
  };

  const handleClear = () => {
    setNombre("");
    onFilter("");
  };

  return (
    <form className="row g-2 align-items-end mb-4" onSubmit={handleSubmit}>
      <div className="col-sm-8">
        <label htmlFor="mercado-nombre" className="form-label">
          Filtrar por nombre
        </label>
        <input
          id="mercado-nombre"
          type="text"
          className="form-control"
          placeholder="Ej. algodón"
          value={nombre}
          onChange={(event) => setNombre(event.target.value)}
          disabled={isLoading}
        />
      </div>
      <div className="col-sm-4 d-flex gap-2">
        <button type="submit" className="btn btn-primary w-100" disabled={isLoading}>
          Buscar
        </button>
        <button
          type="button"
          className="btn btn-outline-secondary"
          onClick={handleClear}
          disabled={isLoading}
        >
          Limpiar
        </button>
      </div>
    </form>
  );
}
