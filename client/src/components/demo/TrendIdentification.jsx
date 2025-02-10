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
  const country = "India";

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8081/api/trends", {
          params: { country },
        });
        let filteredTrends = response.data.trends.filter(
          (trend) => trend.tweet_volume
        );
        
        // Ensure trends are in multiples of 8
        const remainder = filteredTrends.length % 8;
        if (remainder !== 0) {
          filteredTrends = filteredTrends.slice(0, filteredTrends.length - remainder);
        }
        
        setTrends(filteredTrends);
      } catch (err) {
        console.error("Error fetching trends:", err);
        setError("Failed to load trends.");
      }
    };
    fetchTrends();
  }, []);

  const fetchTweets = async (trendName) => {
    setLoading(true);
    setError(null);
    setSelectedTrend(trendName);

    try {
      const response = await axios.post("http://127.0.0.1:8081/api/variable", {
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

  return (
    <section className="py-12">
      <div className="mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-extrabold text-gray-900 mb-6">
          Trending in {country}
        </h2>
        {error && <p className="text-red-500">{error}</p>}

        {/* Swiper Carousel showing 8 topics in a grid layout */}
        <Swiper
          navigation={true}
          modules={[Navigation]}
          spaceBetween={10}
          slidesPerView={1} /* One full-screen width slide at a time */
        >
          {Array.from({ length: Math.ceil(trends.length / 8) }, (_, index) => (
            <SwiperSlide key={index}>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {trends.slice(index * 8, (index + 1) * 8).map((trend, i) => (
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

        {loading && <p className="mt-4">Loading tweets...</p>}
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
      </div>
    </section>
  );
}