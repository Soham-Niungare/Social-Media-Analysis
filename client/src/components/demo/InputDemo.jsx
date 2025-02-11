import { useState } from "react";
import axios from "axios";
import { SentimentChart } from "./SentimentChart";
import { EngagementChart } from "./EngagementChart";
import { Input } from "../ui/input";
import { Spinner } from "../ui/Spinner";
import { Button } from "../ui/button";

export function InputDemo() {
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [chartVisible, setChartVisible] = useState(false);
  const [totalTweets, setTotalTweets] = useState(null);
  const [positivePercentage, setPositivePercentage] = useState(null);
  const [negativePercentage, setNegativePercentage] = useState(null);
  const [neutralPercentage, setNeutralPercentage] = useState(null);
  const [engagementMetrics, setEngagementMetrics] = useState([]);
  const [error, setError] = useState(null);

  const handleInputChange = (event) => {
    setSearchQuery(event.target.value);
    if (error) setError(null);
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setError("Please enter a search term");
      return;
    }

    setLoading(true);
    setChartVisible(false);
    setError(null);

    console.log("User Input:", searchQuery);

    try {
      const response = await axios.post("http://127.0.0.1:8081/api/variable", {
        searchQuery: searchQuery.trim(),
      });

      const {
        sentiment_analysis,
        engagement_metrics
      } = response.data;

      // const randomOffset = Math.floor(Math.random() * (501 - 100)) ;
      // const newTotal = Math.min(sentiment_analysis.total + randomOffset, 10000);

      setEngagementMetrics(engagement_metrics);
      setTotalTweets(sentiment_analysis.total);
      setPositivePercentage(sentiment_analysis.positive_percentage);
      setNegativePercentage(sentiment_analysis.negative_percentage);
      setNeutralPercentage(sentiment_analysis.neutral_percentage);
      setEngagementMetrics(engagement_metrics);
      setChartVisible(true);
    } catch (error) {
      console.error("Error during search:", error);
      setError("An error occurred while analyzing tweets. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="mt-6 mb-4 flex flex-col gap-4 px-8 md:mt-10">
      <h1 className="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
        Dive Into the Data
        <span className="text-blue-600 dark:text-blue-500"> Discover Key Trends in</span> Tweets.
      </h1>

      <p className="text-lg font-normal text-gray-500 lg:text-xl dark:text-gray-400 mb-4">
        At InsightPulse, we focus on unlocking insights from social media data, empowering users to analyze trends, conversations, and engagement on Twitter
      </p>

      <div className="flex flex-col gap-4 justify-center items-center sm:flex-row py-16 border-r border-b border-gray-600 rounded-3xl shadow-[rgba(0,_0,_0,_0.24)_0px_3px_8px]">
        <Input
          type="text"
          placeholder="Search Tweets"
          value={searchQuery}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          className="flex w-[80%] bg-white text-gray-500 rounded-xl sm:w-[30%] border border-gray-500 py-6"
        />
        <Button
          className="py-6"
          onClick={handleSearch}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Search"}
        </Button>
      </div>

      {loading && (
        <div className="flex justify-center my-4">
          <Spinner />
        </div>
      )}

      {error && (
        <div className="text-red-500 text-center my-4">
          {error}
        </div>
      )}

      {chartVisible && (
        <div className="flex flex-wrap gap-4 justify-between">
          <div className="w-full sm:w-[48%]">
            <SentimentChart
              total={totalTweets}
              positivePercentage={positivePercentage}
              negativePercentage={negativePercentage}
              neutralPercentage={neutralPercentage}
            />
          </div>
          <div className="w-full sm:w-[48%]">
            <EngagementChart engagementData={engagementMetrics} />
          </div>
        </div>
      )}
    </div>
  );
}
