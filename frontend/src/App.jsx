import "./App.css";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Advantages from "./components/Advantages";
import CoursesLanding from "./components/Courses";
import StudyProcessLanding from "./components/StudyProcess";
import AboutSection from "./components/AboutSection";
import ReviewSection from "./components/ReviewSection";
import FAQSection from "./components/FAQSection";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="app">

      <Header />

      <main>
        <Hero />
        <Advantages />
        <CoursesLanding />
        <StudyProcessLanding />
        <AboutSection />
        <ReviewSection />
        <FAQSection />



        





        <Footer />


      </main>


    </div>
  );
}


export default App;