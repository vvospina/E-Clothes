import { useEffect, useState } from "react";
import AlertMessage from "../../../shared/components/AlertMessage.jsx";
import LoadingSpinner from "../../../shared/components/LoadingSpinner.jsx";
import PageHeader from "../../../shared/components/PageHeader.jsx";
import { getErrorMessage } from "../../../shared/utils/getErrorMessage.js";
import ConsejoFilter from "../components/ConsejoFilter.jsx";
import ConsejoForm from "../components/ConsejoForm.jsx";
import ConsejoList from "../components/ConsejoList.jsx";
import { createConsejo, listConsejos } from "../services/consejoService.js";

/**
 * Página contenedora del módulo de Sostenibilidad e impacto ambiental.
 *
 * Este es el único microservicio que ya cumple el contrato acordado
 * (/api/v1/consejos), por lo que puede integrarse contra el backend real
 * apenas esté disponible, sin depender de mocks (VITE_MOCK_CONSEJOS=false).
 */
export default function ConsejosPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState(null);

  const loadConsejos = async (categoria = "", signal) => {
    setLoading(true);
    setFeedback(null);

    try {
      const data = await listConsejos({ categoria, signal });
      setItems(Array.isArray(data) ? data : []);
    } catch (error) {
      if (error.code !== "ERR_CANCELED") {
        setFeedback({
          type: "danger",
          message: getErrorMessage(error, "No fue posible cargar los consejos."),
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
    loadConsejos("", controller.signal);
    return () => controller.abort();
  }, []);

  const handleCreateConsejo = async (consejo) => {
    setFeedback(null);

    try {
      await createConsejo(consejo);
      setFeedback({ type: "success", message: "Consejo publicado correctamente." });
      await loadConsejos();
    } catch (error) {
      setFeedback({
        type: "danger",
        message: getErrorMessage(error, "No fue posible publicar el consejo."),
      });
      throw error;
    }
  };

  return (
    <section aria-labelledby="consejos-title">
      <PageHeader
        id="consejos-title"
        title="Consejos ambientales"
        subtitle="Publica y consulta consejos de cuidado y sostenibilidad."
      />

      <AlertMessage type={feedback?.type} message={feedback?.message} />

      <div className="row g-4">
        <div className="col-lg-5">
          <article className="card shadow-sm h-100">
            <div className="card-body p-4">
              <h2 className="h5 mb-4">Nuevo consejo</h2>
              <ConsejoForm onSubmit={handleCreateConsejo} />
            </div>
          </article>
        </div>

        <div className="col-lg-7">
          <article className="card shadow-sm h-100">
            <div className="card-body p-4">
              <h2 className="h5 mb-3">Consejos publicados</h2>
              <ConsejoFilter onFilter={loadConsejos} isLoading={loading} />
              {loading ? (
                <LoadingSpinner label="Cargando consejos" />
              ) : (
                <ConsejoList items={items} />
              )}
            </div>
          </article>
        </div>
      </div>
    </section>
  );
}
