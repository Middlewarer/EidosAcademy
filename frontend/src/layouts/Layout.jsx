import { useEffect } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Header from "../components/initial/Header";
import Footer from "../components/initial/Footer";
import LearningHelper from "../components/LearningHelper";
import ScrollToTopButton from "../components/ScrollToTopButton";
import "../styles/Home.css";

function Layout() {
  const location = useLocation();

  useEffect(() => {
    if (!location.hash) {
      window.scrollTo({ top: 0, behavior: "auto" });
      return undefined;
    }

    const frame = window.requestAnimationFrame(() => {
      const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      target?.scrollIntoView({ block: "start" });
    });
    return () => window.cancelAnimationFrame(frame);
  }, [location.pathname, location.hash]);

  return (
    <>
      <Header />
      <Outlet />
      <Footer />
      <ScrollToTopButton />
      <LearningHelper />
    </>
  );
}

export default Layout;
