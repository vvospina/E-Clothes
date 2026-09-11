import ModuleCard from "../../../shared/components/ModuleCard.jsx";
import useAuth from "../../auth/hooks/useAuth.js";

/**
 * Panel inicial del usuario autenticado en E-clothes.
 */
export default function HomePage() {
  const { user } = useAuth();
  const displayName = user?.displayName || "Usuario autenticado";

  return (
    <section aria-labelledby="home-title">
      <div className="mb-4">
        <h1 id="home-title" className="page-title">
          Inicio
        </h1>
        <p className="text-muted mb-0">
          Selecciona el módulo al que deseas ingresar.
        </p>
      </div>

      <article className="card shadow-sm mb-4">
        <div className="card-body text-center p-4">
          <h2 className="h4">Usuario autenticado</h2>
          <p className="mb-1">
            <strong>Nombre:</strong> {displayName}
          </p>
          <p className="mb-0">
            <strong>Correo:</strong> {user?.email ?? "No disponible"}
          </p>
        </div>
      </article>

      <div className="row g-4">
        <div className="col-md-6 col-xl-3">
          <ModuleCard
            title="Insumos"
            description="Crea, edita y consulta los insumos disponibles para confección."
            to="/insumos"
            actionLabel="Ir a Insumos"
            variant="primary"
          />
        </div>

        <div className="col-md-6 col-xl-3">
          <ModuleCard
            title="Materiales de mercado"
            description="Consulta la valoración económica de materiales disponibles."
            to="/materiales-mercado"
            actionLabel="Ir a Materiales"
            variant="success"
          />
        </div>

        <div className="col-md-6 col-xl-3">
          <ModuleCard
            title="Consejos"
            description="Publica y consulta consejos de sostenibilidad e impacto ambiental."
            to="/consejos"
            actionLabel="Ir a Consejos"
            variant="secondary"
          />
        </div>

        <div className="col-md-6 col-xl-3">
          <ModuleCard
            title="Prendas"
            description="Crea, edita y consulta las prendas publicadas."
            to="/prendas"
            actionLabel="Ir a Prendas"
            variant="dark"
          />
        </div>
      </div>
    </section>
  );
}
