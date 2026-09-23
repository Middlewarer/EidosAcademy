import "../styles/Home.css";
import Header from "../components/initial/Header";
import Hero from "../components/initial/Hero";
import LearningPath from "../components/LearningPath";
import Advantages from "../components/initial/Advantages";
import CoursesLanding from "../components/courses_list/Courses";
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
        <LearningPath />
        <AboutSection />
        <ReviewSection />
        <FAQSection />
      </main>


    </div>
  );
}


export default Home;
