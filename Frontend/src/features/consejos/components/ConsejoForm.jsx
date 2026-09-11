import { useState } from "react";

const INITIAL_FORM = Object.freeze({
  titulo: "",
  contenido: "",
  categoria: "",
});

/**
 * Formulario controlado para publicar un consejo ambiental.
 */
export default function ConsejoForm({ onSubmit }) {
  const [form, setForm] = useState(INITIAL_FORM);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = ({ target }) => {
    setForm((current) => ({ ...current, [target.name]: target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);

    try {
      await onSubmit({
        titulo: form.titulo.trim(),
        contenido: form.contenido.trim(),
        categoria: form.categoria.trim(),
      });
      setForm(INITIAL_FORM);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="consejo-titulo" className="form-label">
          Título
        </label>
        <input
          id="consejo-titulo"
          type="text"
          name="titulo"
          className="form-control"
          placeholder="Ej. Lava tus prendas con agua fría"
          value={form.titulo}
          onChange={handleChange}
          minLength={3}
          maxLength={150}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="consejo-contenido" className="form-label">
          Contenido
        </label>
        <textarea
          id="consejo-contenido"
          name="contenido"
          className="form-control"
          rows={3}
          placeholder="Contenido del consejo ambiental"
          value={form.contenido}
          onChange={handleChange}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-4">
        <label htmlFor="consejo-categoria" className="form-label">
          Categoría
        </label>
        <input
          id="consejo-categoria"
          type="text"
          name="categoria"
          className="form-control"
          placeholder="Ej. Cuidado de prendas, reutilización, reciclaje textil"
          value={form.categoria}
          onChange={handleChange}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="d-grid">
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting ? "Publicando…" : "Publicar consejo"}
        </button>
      </div>
    </form>
  );
}
