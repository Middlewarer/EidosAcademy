import { Outlet } from "react-router-dom";
import Header from "../components/initial/Header";
import Footer from "../components/initial/Footer";
import LearningHelper from "../components/LearningHelper";
import "../styles/Home.css";

function Layout() {
  return (
    <>
      <Header />
      <Outlet />
      <Footer />
      <LearningHelper />
    </>
  );
}

export default Layout;
