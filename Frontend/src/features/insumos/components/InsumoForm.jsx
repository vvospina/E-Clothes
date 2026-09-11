import { useEffect, useState } from "react";

const INITIAL_FORM = Object.freeze({
  nombre: "",
  descripcion: "",
  categoria: "",
  cantidad: "",
  unidad: "kg",
  estado: "activo",
});

/**
 * Formulario controlado de insumos.
 *
 * Se reutiliza para crear y para editar: cuando recibe `editingItem` precarga
 * los campos y cambia la etiqueta del botón principal.
 */
export default function InsumoForm({ editingItem, onSubmit, onCancelEdit }) {
  const [form, setForm] = useState(INITIAL_FORM);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (editingItem) {
      setForm({
        nombre: editingItem.nombre ?? "",
        descripcion: editingItem.descripcion ?? "",
        categoria: editingItem.categoria ?? "",
        cantidad: editingItem.cantidad ?? "",
        unidad: editingItem.unidad ?? "kg",
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
        unidad: form.unidad.trim(),
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
        <label htmlFor="insumo-nombre" className="form-label">
          Nombre
        </label>
        <input
          id="insumo-nombre"
          type="text"
          name="nombre"
          className="form-control"
          placeholder="Ej. Retazos de algodón"
          value={form.nombre}
          onChange={handleChange}
          minLength={3}
          maxLength={100}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="insumo-descripcion" className="form-label">
          Descripción
        </label>
        <textarea
          id="insumo-descripcion"
          name="descripcion"
          className="form-control"
          rows={2}
          placeholder="Describe el insumo"
          value={form.descripcion}
          onChange={handleChange}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="insumo-categoria" className="form-label">
          Categoría
        </label>
        <input
          id="insumo-categoria"
          type="text"
          name="categoria"
          className="form-control"
          placeholder="Ej. Hilo, Lana, Tela"
          value={form.categoria}
          onChange={handleChange}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="row">
        <div className="col-md-6 mb-3">
          <label htmlFor="insumo-cantidad" className="form-label">
            Cantidad
          </label>
          <input
            id="insumo-cantidad"
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
          <label htmlFor="insumo-unidad" className="form-label">
            Unidad
          </label>
          <input
            id="insumo-unidad"
            type="text"
            name="unidad"
            className="form-control"
            placeholder="Ej. kg, unidad"
            value={form.unidad}
            onChange={handleChange}
            required
            disabled={isSubmitting}
          />
        </div>
      </div>

      <div className="mb-4">
        <label htmlFor="insumo-estado" className="form-label">
          Estado
        </label>
        <select
          id="insumo-estado"
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

      <div className="d-flex gap-2">
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting
            ? "Guardando…"
            : editingItem
              ? "Guardar cambios"
              : "Publicar insumo"}
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
