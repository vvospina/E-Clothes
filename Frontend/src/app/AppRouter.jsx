import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import ProtectedRoute from "../features/auth/routes/ProtectedRoute.jsx";
import useAuth from "../features/auth/hooks/useAuth.js";
import LoadingSpinner from "../shared/components/LoadingSpinner.jsx";
import AppLayout from "../shared/layouts/AppLayout.jsx";
import NotFoundPage from "../shared/pages/NotFoundPage.jsx";

// Las páginas se cargan únicamente cuando la ruta correspondiente se visita.
const LoginPage = lazy(() => import("../features/auth/pages/LoginPage.jsx"));
const HomePage = lazy(() => import("../features/home/pages/HomePage.jsx"));
const InsumosPage = lazy(() => import("../features/insumos/pages/InsumosPage.jsx"));
const MaterialesMercadoPage = lazy(() =>
  import("../features/materialesMercado/pages/MaterialesMercadoPage.jsx"),
);
const ConsejosPage = lazy(() => import("../features/consejos/pages/ConsejosPage.jsx"));
const PrendasPage = lazy(() => import("../features/prendas/pages/PrendasPage.jsx"));

/**
 * Decide el destino inicial una vez Firebase termina de restaurar la sesión.
 */
function RootRedirect() {
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner fullPage label="Verificando sesión" />;
  }

  return <Navigate to={user ? "/home" : "/login"} replace />;
}

/**
 * Mapa central de navegación de E-clothes.
 *
 * Cada ruta funcional corresponde 1 a 1 con un microservicio del equipo:
 * /insumos -> Gestión de insumos (David), /materiales-mercado -> Valoración
 * económica (Camilo), /consejos -> Sostenibilidad (Sara), /prendas -> Gestión
 * de prendas (Nicol). Todas viven bajo ProtectedRoute + AppLayout, igual que
 * el resto del panel autenticado.
 */
export default function AppRouter() {
  return (
    <Suspense fallback={<LoadingSpinner fullPage label="Cargando módulo" />}>
      <Routes>
        <Route path="/" element={<RootRedirect />} />
        <Route path="/login" element={<LoginPage />} />

        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route path="/home" element={<HomePage />} />
            <Route path="/insumos" element={<InsumosPage />} />
            <Route path="/materiales-mercado" element={<MaterialesMercadoPage />} />
            <Route path="/consejos" element={<ConsejosPage />} />
            <Route path="/prendas" element={<PrendasPage />} />
          </Route>
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
}
