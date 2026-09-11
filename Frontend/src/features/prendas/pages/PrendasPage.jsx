import { useEffect, useState } from "react";
import AlertMessage from "../../../shared/components/AlertMessage.jsx";
import LoadingSpinner from "../../../shared/components/LoadingSpinner.jsx";
import PageHeader from "../../../shared/components/PageHeader.jsx";
import { getErrorMessage } from "../../../shared/utils/getErrorMessage.js";
import PrendaForm from "../components/PrendaForm.jsx";
import PrendaList from "../components/PrendaList.jsx";
import {
  createPrenda,
  deletePrenda,
  listPrendas,
  updatePrenda,
} from "../services/prendaService.js";

/**
 * Página contenedora del módulo de Gestión de prendas.
 */
export default function PrendasPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState(null);
  const [editingItem, setEditingItem] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    const loadPrendas = async () => {
      setLoading(true);
      setFeedback(null);

      try {
        const data = await listPrendas({ signal: controller.signal });
        setItems(Array.isArray(data) ? data : []);
      } catch (error) {
        if (error.code !== "ERR_CANCELED") {
          setFeedback({
            type: "danger",
            message: getErrorMessage(error, "No fue posible cargar las prendas."),
          });
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    loadPrendas();
    return () => controller.abort();
  }, []);

  const refreshItems = async () => {
    const data = await listPrendas();
    setItems(Array.isArray(data) ? data : []);
  };

  const handleCreateOrUpdate = async (payload) => {
    setFeedback(null);

    try {
      if (editingItem) {
        await updatePrenda(editingItem.id, payload);
        setFeedback({ type: "success", message: "Prenda actualizada correctamente." });
        setEditingItem(null);
      } else {
        await createPrenda(payload);
        setFeedback({ type: "success", message: "Prenda publicada correctamente." });
      }
      await refreshItems();
    } catch (error) {
      setFeedback({
        type: "danger",
        message: getErrorMessage(error, "No fue posible guardar la prenda."),
      });
      throw error;
    }
  };

  const handleDelete = async (item) => {
    setFeedback(null);

    try {
      await deletePrenda(item.id);
      setFeedback({ type: "success", message: "Prenda eliminada correctamente." });
      await refreshItems();
    } catch (error) {
      setFeedback({
        type: "danger",
        message: getErrorMessage(error, "No fue posible eliminar la prenda."),
      });
    }
  };

  return (
    <section aria-labelledby="prendas-title">
      <PageHeader
        id="prendas-title"
        title="Prendas"
        subtitle="Crea, edita, elimina y consulta las prendas publicadas."
      />

      <AlertMessage type={feedback?.type} message={feedback?.message} />

      {loading ? (
        <LoadingSpinner label="Cargando prendas" />
      ) : (
        <div className="row g-4">
          <div className="col-lg-5">
            <article className="card shadow-sm h-100">
              <div className="card-body p-4">
                <h2 className="h5 mb-4">
                  {editingItem ? "Editar prenda" : "Nueva prenda"}
                </h2>
                <PrendaForm
                  editingItem={editingItem}
                  onSubmit={handleCreateOrUpdate}
                  onCancelEdit={() => setEditingItem(null)}
                />
              </div>
            </article>
          </div>

          <div className="col-lg-7">
            <article className="card shadow-sm h-100">
              <div className="card-body p-4">
                <h2 className="h5 mb-3">Prendas publicadas</h2>
                <PrendaList items={items} onEdit={setEditingItem} onDelete={handleDelete} />
              </div>
            </article>
          </div>
        </div>
      )}
    </section>
  );
}
