import { useState, useRef } from "react";
import axios from "axios";
import { HeroSection } from "./components/demo/HeroSection";
import { InputDemo } from "./components/demo/InputDemo";
import { Navbar } from "./components/demo/Navbar";
import { TrendIdentification } from "./components/demo/TrendIdentification";
import { Footer } from "./components/demo/Footer";

function App() {
  const [sentimentData, setSentimentData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sentimentRef = useRef(null);
  const trendRef = useRef(null);

  const scrollToSection = (ref) => {
    ref.current?.scrollIntoView({ behavior: "smooth" });
  };

  const analyzeSentiment = async (searchQuery) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post("http://localhost:8081/api/variable", {
        searchQuery: searchQuery
      });
      
      setSentimentData(response.data);
    } catch (err) {
      setError(err.response?.data?.message || "An error occurred");
      console.error("Error fetching sentiment:", err);
    } finally {
      setLoading(false);
    }
  };

  // You might want to pass this function to InputDemo component
  const handleSearch = (query) => {
    analyzeSentiment(query);
  };

  return (
    <div className="w-full flex flex-col bg-gray-200">
      <Navbar scrollToSection={scrollToSection} sentimentRef={sentimentRef} trendRef={trendRef}/>
          <HeroSection />
          <div ref={sentimentRef}>
              <InputDemo onSearch={handleSearch}  />
              {loading && (
                <div className="text-center p-4">
                  Loading analysis...
                </div>
              )}
              {error && (
                <div className="text-red-500 p-4 text-center">
                  {error}
                </div>
              )} 
          </div>
          <div ref={trendRef}>
          <TrendIdentification />
          </div>
      <Footer />
    </div>
  );
}

export default App;