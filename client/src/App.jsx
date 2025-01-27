import { useEffect, useState } from "react";
import axios from "axios";
import { HeroSection } from "./components/demo/HeroSection";
import { InputDemo } from "./components/demo/InputDemo";
import { Sidebar } from "./components/demo/Sidebar";
import { Footer } from "./components/demo/Footer";

function App() {
  const [sentimentData, setSentimentData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
    <div className="w-full flex flex-col gap-4 bg-gray-200">
      <div className="grid grid-cols-1 lg:grid-cols-[auto_1fr] lg:gap-6 mx-2 mt-2 md:mx-0">
        <Sidebar />
        <div className="flex flex-col gap-2">
          <HeroSection />
          <InputDemo onSearch={handleSearch} />
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
          {sentimentData && (
            <div className="bg-white p-4 rounded-lg shadow">
              <h2 className="text-xl font-bold mb-4">Sentiment Analysis Results</h2>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-4 bg-green-100 rounded">
                  <div className="font-bold text-green-700">Positive</div>
                  <div>{sentimentData.positive_percentage.toFixed(1)}%</div>
                </div>
                <div className="text-center p-4 bg-red-100 rounded">
                  <div className="font-bold text-red-700">Negative</div>
                  <div>{sentimentData.negative_percentage.toFixed(1)}%</div>
                </div>
                <div className="text-center p-4 bg-gray-100 rounded">
                  <div className="font-bold text-gray-700">Neutral</div>
                  <div>{sentimentData.neutral_percentage.toFixed(1)}%</div>
                </div>
              </div>
              <div className="mt-4 text-center text-gray-600">
                Total tweets analyzed: {sentimentData.total}
              </div>
            </div>
          )}
          {/* <Blogsection /> */}
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default App;