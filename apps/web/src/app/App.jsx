import { Navigate, Route, Routes } from "react-router-dom";

import { DashboardPage } from "../pages/DashboardPage";
import { AIContextPage } from "../pages/AIContextPage";
import { ArchitecturePage } from "../pages/ArchitecturePage";
import { DesignAdvisorPage } from "../pages/DesignAdvisorPage";
import { HomeModelPage } from "../pages/HomeModelPage";
import { ProductLibraryPage } from "../pages/ProductLibraryPage";
import { ScenarioComparisonPage } from "../pages/ScenarioComparisonPage";
import { SystemDesignBuilderPage } from "../pages/SystemDesignBuilderPage";
import { TakeoffEstimatePage } from "../pages/TakeoffEstimatePage";
import {
  BuilderShellPage,
  CapabilitiesShellPage,
  CatalogShellPage,
  ExploreShellPage,
  HeartQuillAppShell,
  HomeShellPage,
  PlannerShellPage,
} from "../pages/HeartQuillShellPage";

export default function App() {
  return (
    <HeartQuillAppShell>
      <Routes>
        <Route path="/" element={<HomeShellPage />} />
        <Route path="/home" element={<HomeShellPage />} />
        <Route path="/explore" element={<ExploreShellPage />} />
        <Route path="/planner" element={<PlannerShellPage />} />
        <Route path="/builder" element={<BuilderShellPage />} />

        <Route path="/capabilities" element={<CapabilitiesShellPage />} />
        <Route path="/internal/capabilities" element={<CapabilitiesShellPage internal />} />
        <Route path="/catalog" element={<CatalogShellPage />} />

        <Route path="/experience" element={<Navigate to="/explore" replace />} />
        <Route path="/twin" element={<Navigate to="/" replace />} />
        <Route path="/scenario" element={<Navigate to="/planner" replace />} />
        <Route path="/progress" element={<Navigate to="/builder" replace />} />

        <Route path="/dashboard-legacy" element={<DashboardPage />} />
        <Route path="/home-model" element={<HomeModelPage />} />
        <Route path="/design-builder" element={<SystemDesignBuilderPage />} />
        <Route path="/product-library" element={<ProductLibraryPage />} />
        <Route path="/scenario-comparison" element={<ScenarioComparisonPage />} />
        <Route path="/design-advisor" element={<DesignAdvisorPage />} />
        <Route path="/ai-context" element={<AIContextPage />} />
        <Route path="/architecture" element={<ArchitecturePage />} />
        <Route path="/takeoff-estimate" element={<TakeoffEstimatePage />} />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </HeartQuillAppShell>
  );
}
