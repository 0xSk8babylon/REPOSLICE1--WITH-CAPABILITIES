import { NavLink, Route, Routes } from "react-router-dom";

import { Shell } from "../components/Shell";
import { DashboardPage } from "../pages/DashboardPage";
import { AIContextPage } from "../pages/AIContextPage";
import { DesignAdvisorPage } from "../pages/DesignAdvisorPage";
import { HomeModelPage } from "../pages/HomeModelPage";
import { ProductLibraryPage } from "../pages/ProductLibraryPage";
import { ScenarioComparisonPage } from "../pages/ScenarioComparisonPage";
import { SystemDesignBuilderPage } from "../pages/SystemDesignBuilderPage";
import { TakeoffEstimatePage } from "../pages/TakeoffEstimatePage";

const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/home-model", label: "Home / Property Model" },
  { to: "/design-builder", label: "System Design Builder" },
  { to: "/product-library", label: "Product Library" },
  { to: "/scenario-comparison", label: "Scenario Comparison" },
  { to: "/design-advisor", label: "Design Advisor" },
  { to: "/ai-context", label: "AI Context" },
  { to: "/takeoff-estimate", label: "Takeoff / Estimate" },
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
    <Shell navigation={<Navigation />}>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/home-model" element={<HomeModelPage />} />
        <Route path="/design-builder" element={<SystemDesignBuilderPage />} />
        <Route path="/product-library" element={<ProductLibraryPage />} />
        <Route path="/scenario-comparison" element={<ScenarioComparisonPage />} />
        <Route path="/design-advisor" element={<DesignAdvisorPage />} />
        <Route path="/ai-context" element={<AIContextPage />} />
        <Route path="/takeoff-estimate" element={<TakeoffEstimatePage />} />
      </Routes>
    </Shell>
  );
}
