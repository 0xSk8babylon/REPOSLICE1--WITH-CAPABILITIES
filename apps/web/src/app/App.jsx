import { NavLink, Route, Routes } from "react-router-dom";

import { Shell } from "../components/Shell";
import { DashboardPage } from "../pages/DashboardPage";
import { AIContextPage } from "../pages/AIContextPage";
import { ArchitecturePage } from "../pages/ArchitecturePage";
import { DesignAdvisorPage } from "../pages/DesignAdvisorPage";
import { HomeModelPage } from "../pages/HomeModelPage";
import { C1ExperiencePage } from "../pages/C1ExperiencePage";
import { ProductLibraryPage } from "../pages/ProductLibraryPage";
import { ScenarioComparisonPage } from "../pages/ScenarioComparisonPage";
import { SystemDesignBuilderPage } from "../pages/SystemDesignBuilderPage";
import { TakeoffEstimatePage } from "../pages/TakeoffEstimatePage";

// Minimal, homeowner-safe navigation for U1. Existing routes are preserved
// (still defined below and deep-linkable); only the primary nav is trimmed and
// relabeled away from contractor/endpoint language.
const navItems = [
  { to: "/", label: "Overview" },
  { to: "/experience", label: "Explore" },
  { to: "/home-model", label: "Energy Twin" },
  { to: "/design-builder", label: "Goals" },
  { to: "/design-advisor", label: "Readiness" },
  { to: "/scenario-comparison", label: "Upgrade Paths" },
];

function Navigation() {
  return (
    <nav className="topnav">
      {navItems.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
          end={item.to === "/"}
        >
          {item.label}
        </NavLink>
      ))}
    </nav>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route
        path="*"
        element={
          <Shell navigation={<Navigation />}>
            <Routes>
              <Route path="/home-model" element={<HomeModelPage />} />
              <Route path="/experience" element={<C1ExperiencePage />} />
              <Route path="/design-builder" element={<SystemDesignBuilderPage />} />
              <Route path="/product-library" element={<ProductLibraryPage />} />
              <Route path="/scenario-comparison" element={<ScenarioComparisonPage />} />
              <Route path="/design-advisor" element={<DesignAdvisorPage />} />
              <Route path="/ai-context" element={<AIContextPage />} />
              <Route path="/architecture" element={<ArchitecturePage />} />
              <Route path="/takeoff-estimate" element={<TakeoffEstimatePage />} />
            </Routes>
          </Shell>
        }
      />
    </Routes>
  );
}
