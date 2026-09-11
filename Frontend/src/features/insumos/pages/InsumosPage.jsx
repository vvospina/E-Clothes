import { useEffect, useState } from "react";
import AlertMessage from "../../../shared/components/AlertMessage.jsx";
import LoadingSpinner from "../../../shared/components/LoadingSpinner.jsx";
import PageHeader from "../../../shared/components/PageHeader.jsx";
import { getErrorMessage } from "../../../shared/utils/getErrorMessage.js";
import InsumoForm from "../components/InsumoForm.jsx";
import InsumoList from "../components/InsumoList.jsx";
import {
  createInsumo,
  deleteInsumo,
  listInsumos,
  updateInsumo,
} from "../services/insumoService.js";

/**
 * Página contenedora del módulo de Gestión de insumos.
 *
 * Cubre las cuatro operaciones del contrato: crear, listar, editar y
 * eliminar. AbortController evita actualizar estado si el usuario abandona
 * la ruta durante la carga inicial.
 */
export default function InsumosPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState(null);
  const [editingItem, setEditingItem] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    const loadInsumos = async () => {
      setLoading(true);
      setFeedback(null);

      try {
        const data = await listInsumos({ signal: controller.signal });
        setItems(Array.isArray(data) ? data : []);
      } catch (error) {
        if (error.code !== "ERR_CANCELED") {
          setFeedback({
            type: "danger",
            message: getErrorMessage(error, "No fue posible cargar los insumos."),
          });
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    loadInsumos();
    return () => controller.abort();
  }, []);

  const refreshItems = async () => {
    const data = await listInsumos();
    setItems(Array.isArray(data) ? data : []);
  };

  const handleCreateOrUpdate = async (payload) => {
    setFeedback(null);

    try {
      if (editingItem) {
        await updateInsumo(editingItem.id, payload);
        setFeedback({ type: "success", message: "Insumo actualizado correctamente." });
        setEditingItem(null);
      } else {
        await createInsumo(payload);
        setFeedback({ type: "success", message: "Insumo publicado correctamente." });
      }
      await refreshItems();
    } catch (error) {
      setFeedback({
        type: "danger",
        message: getErrorMessage(error, "No fue posible guardar el insumo."),
      });
      throw error;
    }
  };

  const handleDelete = async (item) => {
    setFeedback(null);

    try {
      await deleteInsumo(item.id);
      setFeedback({ type: "success", message: "Insumo eliminado correctamente." });
      await refreshItems();
    } catch (error) {
      setFeedback({
        type: "danger",
        message: getErrorMessage(error, "No fue posible eliminar el insumo."),
      });
    }
  };

  return (
    <section aria-labelledby="insumos-title">
      <PageHeader
        id="insumos-title"
        title="Insumos"
        subtitle="Crea, edita, elimina y consulta los insumos publicados."
      />

      <AlertMessage type={feedback?.type} message={feedback?.message} />

      {loading ? (
        <LoadingSpinner label="Cargando insumos" />
      ) : (
        <div className="row g-4">
          <div className="col-lg-5">
            <article className="card shadow-sm h-100">
              <div className="card-body p-4">
                <h2 className="h5 mb-4">
                  {editingItem ? "Editar insumo" : "Nuevo insumo"}
                </h2>
                <InsumoForm
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
                <h2 className="h5 mb-3">Insumos publicados</h2>
                <InsumoList
                  items={items}
                  onEdit={setEditingItem}
                  onDelete={handleDelete}
                />
              </div>
            </article>
          </div>
        </div>
      )}
    </section>
  );
}
