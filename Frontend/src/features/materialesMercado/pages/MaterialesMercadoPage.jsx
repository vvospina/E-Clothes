import { useEffect, useState } from "react";
import AlertMessage from "../../../shared/components/AlertMessage.jsx";
import LoadingSpinner from "../../../shared/components/LoadingSpinner.jsx";
import PageHeader from "../../../shared/components/PageHeader.jsx";
import { getErrorMessage } from "../../../shared/utils/getErrorMessage.js";
import MaterialMercadoFilter from "../components/MaterialMercadoFilter.jsx";
import MaterialMercadoList from "../components/MaterialMercadoList.jsx";
import { listMaterialesMercado } from "../services/materialMercadoService.js";

/**
 * Página contenedora del módulo de Valoración económica (mercado).
 *
 * Es un módulo exclusivamente de consulta: no expone creación, edición ni
 * eliminación porque el contrato de este microservicio solo define
 * operaciones GET.
 */
export default function MaterialesMercadoPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState(null);

  const loadMateriales = async (nombre = "", signal) => {
    setLoading(true);
    setFeedback(null);

    try {
      const data = await listMaterialesMercado({ nombre, signal });
      setItems(Array.isArray(data) ? data : []);
    } catch (error) {
      if (error.code !== "ERR_CANCELED") {
        setFeedback({
          type: "danger",
          message: getErrorMessage(error, "No fue posible cargar los materiales."),
        });
      }
    } finally {
      if (!signal || !signal.aborted) {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    const controller = new AbortController();
    loadMateriales("", controller.signal);
    return () => controller.abort();
  }, []);

  return (
    <section aria-labelledby="mercado-title">
      <PageHeader
        id="mercado-title"
        title="Materiales de mercado"
        subtitle="Consulta y filtra los materiales disponibles para valoración económica."
      />

      <AlertMessage type={feedback?.type} message={feedback?.message} />

      <article className="card shadow-sm">
        <div className="card-body p-4">
          <MaterialMercadoFilter onFilter={loadMateriales} isLoading={loading} />

          {loading ? (
            <LoadingSpinner label="Cargando materiales" />
          ) : (
            <MaterialMercadoList items={items} />
          )}
        </div>
      </article>
    </section>
  );
}
