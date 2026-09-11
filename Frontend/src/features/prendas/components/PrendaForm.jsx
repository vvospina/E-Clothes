import { useEffect, useState } from "react";

const INITIAL_FORM = Object.freeze({
  nombre: "",
  descripcion: "",
  categoria: "",
  cantidad: "",
  estado: "activo",
});

/**
 * Formulario controlado de prendas. Se reutiliza para crear y editar.
 */
export default function PrendaForm({ editingItem, onSubmit, onCancelEdit }) {
  const [form, setForm] = useState(INITIAL_FORM);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (editingItem) {
      setForm({
        nombre: editingItem.nombre ?? "",
        descripcion: editingItem.descripcion ?? "",
        categoria: editingItem.categoria ?? "",
        cantidad: editingItem.cantidad ?? "",
        estado: editingItem.estado ?? "activo",
      });
    } else {
      setForm(INITIAL_FORM);
    }
  }, [editingItem]);

  const handleChange = ({ target }) => {
    setForm((current) => ({ ...current, [target.name]: target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);

    try {
      await onSubmit({
        nombre: form.nombre.trim(),
        descripcion: form.descripcion.trim(),
        categoria: form.categoria.trim(),
        cantidad: Number(form.cantidad),
        estado: form.estado,
      });
      if (!editingItem) {
        setForm(INITIAL_FORM);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="prenda-nombre" className="form-label">
          Nombre
        </label>
        <input
          id="prenda-nombre"
          type="text"
          name="nombre"
          className="form-control"
          placeholder="Ej. Camisa de lino blanca"
          value={form.nombre}
          onChange={handleChange}
          minLength={3}
          maxLength={100}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="prenda-descripcion" className="form-label">
          Descripción
        </label>
        <textarea
          id="prenda-descripcion"
          name="descripcion"
          className="form-control"
          rows={2}
          placeholder="Describe la prenda"
          value={form.descripcion}
          onChange={handleChange}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="prenda-categoria" className="form-label">
          Categoría
        </label>
        <input
          id="prenda-categoria"
          type="text"
          name="categoria"
          className="form-control"
          placeholder="Ej. Camisa, Pantalón, Vestido (Segunda mano, nuevo)"
          value={form.categoria}
          onChange={handleChange}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="row">
        <div className="col-md-6 mb-3">
          <label htmlFor="prenda-cantidad" className="form-label">
            Cantidad
          </label>
          <input
            id="prenda-cantidad"
            type="number"
            name="cantidad"
            className="form-control"
            min="0.01"
            step="any"
            value={form.cantidad}
            onChange={handleChange}
            required
            disabled={isSubmitting}
          />
        </div>

        <div className="col-md-6 mb-3">
          <label htmlFor="prenda-estado" className="form-label">
            Estado
          </label>
          <select
            id="prenda-estado"
            name="estado"
            className="form-select"
            value={form.estado}
            onChange={handleChange}
            disabled={isSubmitting}
          >
            <option value="activo">Activo</option>
            <option value="inactivo">Inactivo</option>
          </select>
        </div>
      </div>

      <div className="d-flex gap-2 mt-2">
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting
            ? "Guardando…"
            : editingItem
              ? "Guardar cambios"
              : "Publicar prenda"}
        </button>
        {editingItem && (
          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={onCancelEdit}
            disabled={isSubmitting}
          >
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}
