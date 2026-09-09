import { useState } from "react";

const INITIAL_FORM = Object.freeze({
  name: "",
  nit: "",
  description: "", /** NUEVO ATRIBUTO */
  city: "",
  address: "", /** NUEVO ATRIBUTO */
  sector: "",
});

/**
 * Formulario reutilizable de empresas.
 *
 * La validación básica permanece en HTML y la persistencia se delega a la
 * página para que el componente no dependa directamente de Axios.
 */
export default function CompanyForm({ onSubmit }) {
  const [form, setForm] = useState(INITIAL_FORM);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = ({ target }) => {
    setForm((current) => ({
      ...current,
      [target.name]: target.value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);

    try {
      await onSubmit({
        name: form.name.trim(),
        nit: form.nit.trim(),
        description: form.description.trim(), /** NUEVO ATRIBUTO */
        city: form.city.trim(),
        address: form.address.trim(), /** NUEVO ATRIBUTO */
        sector: form.sector.trim(),
      });
      setForm(INITIAL_FORM);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="company-name" className="form-label">
          Nombre
        </label>
        <input
          id="company-name"
          type="text"
          name="name"
          className="form-control"
          placeholder="Nombre de la empresa"
          value={form.name}
          onChange={handleChange}
          autoComplete="organization"
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="company-nit" className="form-label">
          NIT
        </label>
        <input
          id="company-nit"
          type="text"
          name="nit"
          className="form-control"
          placeholder="Número de identificación tributaria"
          value={form.nit}
          onChange={handleChange}
          inputMode="numeric"
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="company-nit" className="form-label">
          Descripción
        </label>
        <input
          id="company-description"
          type="text"
          name="description"
          className="form-control"
          placeholder="¿Que hace su empresa?"
          value={form.description}
          onChange={handleChange}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="company-city" className="form-label">
          Ciudad
        </label>
        <input
          id="company-city"
          type="text"
          name="city"
          className="form-control"
          placeholder="Ciudad principal"
          value={form.city}
          onChange={handleChange}
          autoComplete="address-level2"
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="company-city" className="form-label">
          Direccion
        </label>
        <input
          id="company-city"
          type="text"
          name="address"
          className="form-control"
          placeholder="Ej: Cl. 72 #10-34, Bogotá"
          value={form.address}
          onChange={handleChange}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-4">
        <label htmlFor="company-sector" className="form-label">
          Sector
        </label>
        <input
          id="company-sector"
          type="text"
          name="sector"
          className="form-control"
          placeholder="Sector económico"
          value={form.sector}
          onChange={handleChange}
          required
          disabled={isSubmitting}
        />
      </div>

      <div className="d-grid">
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting ? "Guardando…" : "Guardar empresa"}
        </button>
      </div>
    </form>
  );
}
