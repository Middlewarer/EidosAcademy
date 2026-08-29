import { Outlet } from "react-router-dom";
import Header from "../components/initial/Header";
import Footer from "../components/initial/Footer";
import "../styles/Home.css";

function Layout() {
  return (
    <>
      <Header />
      <Outlet />
      <Footer />
    </>
  );
}

export default Layout;