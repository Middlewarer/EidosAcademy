import "../styles/Home.css";
import Header from "../components/initial/Header";
import Hero from "../components/initial/Hero";
import Advantages from "../components/initial/Advantages";
import CoursesLanding from "../components/courses_list/Courses";
import StudyProcessLanding from "../components/initial/StudyProcess";
import AboutSection from "../components/initial/AboutSection";
import ReviewSection from "../components/initial/ReviewSection";
import FAQSection from "../components/initial/FAQSection";
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