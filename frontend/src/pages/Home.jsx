import "../styles/Home.css";
import Header from "../components/initial/Header";
import Hero from "../components/landing/Hero";
import Advantages from "../components/landing/Advantages";
import CoursesLanding from "../components/landing/Courses";
import StudyProcessLanding from "../components/landing/StudyProcess";
import AboutSection from "../components/landing/AboutSection";
import ReviewSection from "../components/landing/ReviewSection";
import FAQSection from "../components/landing/FAQSection";
import Footer from "../components/initial/Footer";

function Home() {
  return (
    <div className="app">
      <main>
        <Hero />
        <Advantages />
        <CoursesLanding />
        <StudyProcessLanding />
        <AboutSection />
        <ReviewSection />
        <FAQSection />
      </main>


    </div>
  );
}


export default Home;