import { useState, useEffect } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/navigation";
import { Navigation } from "swiper/modules";

export function TrendIdentification() {
  const [trends, setTrends] = useState([]);
  const [selectedTrend, setSelectedTrend] = useState(null);
  const [tweets, setTweets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState("India");
  const countryOptions = [
    "Worldwide",
    "United States",
    "India",
    "United Kingdom",
    "Canada",
    "Australia",
    "Japan",
    "Brazil",
    "Germany",
    "France",
    "Russia",
    "South Africa",
    "Indonesia",
    "Mexico",
    "Italy",
    "Spain",
    "Turkey",
    "Saudi Arabia",
    "South Korea",
    "Argentina",
    "Netherlands",
    "Sweden",
    "Switzerland",
    "Malaysia",
    "Thailand",
    "Nigeria",
    "Singapore",
    "Philippines",
    "Pakistan",
    "Egypt",
    "Vietnam",
  ];

  useEffect(() => {
    fetchTrends(selectedCountry);
  }, [selectedCountry]);

  const fetchTrends = async (country) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get("http://127.0.0.1:8081/api/trends", {
        params: { country: country },
      });

      let filteredTrends = response.data.trends.filter(
        (trend) => trend.tweet_volume
      );

      setTrends(filteredTrends);
    } catch (err) {
      console.error("Error fetching trends:", err);
      setError("Failed to load trends.");
    } finally {
      setLoading(false);
    }
  };

  const fetchTweets = async (trendName) => {
    setLoading(true);
    setError(null);
    setSelectedTrend(trendName);

    try {
      const response = await axios.post("http://127.0.0.1:8081/api/trends", {
        searchQuery: trendName,
      });
      setTweets(response.data.tweets || []);
    } catch (err) {
      console.error("Error fetching tweets:", err);
      setError("Failed to load tweets.");
    } finally {
      setLoading(false);
    }
  };

  const handleCountryChange = (event) => {
    setSelectedCountry(event.target.value);
  };

  const chunkedTrends = [];
  for (let i = 0; i < trends.length; i += 8) {
    chunkedTrends.push(trends.slice(i, i + 8));
  }

  return (
    <section className="py-12 mt-6 flex flex-col gap-4 px-8 md:mt-10 flex-grow bg-gray-300">
      <h1 className="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900  md:text-5xl lg:text-6xl dark:text-white">
        Trending Now: Unveiling the 
        <span className="text-blue-600 dark:text-blue-500">
          {" "}
          Most Talked-About
        </span>{" "}
        Topics! 
      </h1>
      
      <p className="text-lg font-normal text-gray-500 lg:text-xl dark:text-gray-400 mb-4">
        At InsightPulse, we focus on unlocking insights from social media
        data, empowering users to analyze trends, conversations, and engagement
        on Twitter. 
      </p>
      <div className="flex flex-col gap-4 justify-center items-center sm:flex-row py-16 border-r border-b border-gray-600 bg-gray-200 rounded-3xl shadow-[0_35px_60px_-15px_rgba(0,0,0,0.3)]">
        <select
          value={selectedCountry}
          onChange={handleCountryChange}
          className="flex w-[80%] bg-white text-gray-800 text-xl font-semibold pl-4 rounded-xl sm:w-[30%] border border-gray-500 py-6"
        >
          {countryOptions.map((country) => (
            <option key={country} value={country}>
              {country}
            </option>
          ))}
        </select>
      </div>
      <h2 className="text-3xl font-extrabold text-gray-900 mb-6">
         Trending in {selectedCountry} {/* Display selectedCountry */}
       </h2>

       {loading && <p className="mt-4 text-center">Loading trends...</p>}
       {error && <p className="text-red-500">{error}</p>}

       {/* Swiper with Pagination for 8 trends per page */}
       <Swiper
        navigation={true}
        modules={[Navigation]}
        spaceBetween={20}
        className="w-full"
      >
        {chunkedTrends.map((trendPage, index) => (
          <SwiperSlide key={index}>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
              {trendPage.map((trend, i) => (
                <Card
                  key={i}
                  className="cursor-pointer hover:shadow-lg w-full"
                  onClick={() => fetchTweets(trend.name)}
                >
                  <CardHeader>
                    <CardTitle>{trend.name}</CardTitle>
                    <CardDescription>Trending topic</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-2xl font-bold">{trend.tweet_volume} mentions</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </SwiperSlide>
        ))}
      </Swiper>

      {selectedTrend && tweets.length > 0 && (
        <div className="mt-8">
          <h3 className="text-2xl font-bold">Tweets for {selectedTrend}</h3>
          <ul className="mt-4 space-y-4">
            {tweets.map((tweet, index) => (
              <li key={index} className="p-4 border rounded-lg shadow-md">
                <p className="text-gray-700">{tweet.text}</p>
                <p className="text-sm text-gray-500">- {tweet.user}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}


