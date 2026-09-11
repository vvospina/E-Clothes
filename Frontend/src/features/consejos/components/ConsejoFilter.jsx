import { useState } from "react";

/**
 * Barra de filtro por categoría. Delega la búsqueda a la página contenedora.
 */
export default function ConsejoFilter({ onFilter, isLoading }) {
  const [categoria, setCategoria] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    onFilter(categoria.trim());
  };

  const handleClear = () => {
    setCategoria("");
    onFilter("");
  };

  return (
    <form className="row g-2 align-items-end mb-4" onSubmit={handleSubmit}>
      <div className="col-sm-8">
        <label htmlFor="consejo-filtro-categoria" className="form-label">
          Filtrar por categoría
        </label>
        <input
          id="consejo-filtro-categoria"
          type="text"
          className="form-control"
          placeholder="Ej. reciclaje textil"
          value={categoria}
          onChange={(event) => setCategoria(event.target.value)}
          disabled={isLoading}
        />
      </div>
      <div className="col-sm-4 d-flex gap-2">
        <button type="submit" className="btn btn-primary w-100" disabled={isLoading}>
          Filtrar
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
