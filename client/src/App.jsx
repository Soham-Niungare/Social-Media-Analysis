import { useEffect, useState } from "react";
import axios from "axios";
import { HeroSection } from "./components/demo/HeroSection";
import { InputDemo } from "./components/demo/InputDemo";
import { Sidebar } from "./components/demo/Sidebar";
import { NewsSection } from "./components/demo/NewsSection";
import { Footer } from "./components/demo/Footer";

function App() {
  const [array, setArray] = useState([]);

  const fetchAPI = async () => {
    const response = await axios.get("http://127.0.0.1:8081/api/users");
    setArray(response.data.users);
  };

  useEffect(() => {
    fetchAPI();
  }, []);

  return (
    <>
      <div className="w-full  flex flex-col gap-4 bg-gray-200">
        <div className="grid grid-cols-1 lg:grid-cols-[auto_1fr] lg:gap-6 mx-2 mt-2 md:mx-0">
          <Sidebar></Sidebar>
          <div className="flex flex-col gap-2">
            <HeroSection></HeroSection>
            <InputDemo></InputDemo>
            <NewsSection></NewsSection>
          </div>
        </div>
        <Footer></Footer>
      </div>
    </>
  );
}

export default App;
