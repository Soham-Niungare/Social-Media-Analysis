import { useState } from "react";
import { MyChart } from "./ChartDemo1";
import axios from "axios";
<<<<<<< HEAD
import { Spinner } from "../ui/Spinner";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
=======
import { Spinner } from "../ui/spinner";
>>>>>>> c6b76d29a7c57eb0443c65b9a41d272b5249c7e4

export function InputDemo() {
  const [searchQuery, setSearchQuery] = useState("");
  const [responseMessage, setResponseMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [chartVisible, setChartVisible] = useState(false);
  const [totalTweets, setTotalTweets] = useState(null);
  const [positivePercentage, setPositivePercentage] = useState(null);
  const [negativePercentage, setNegativePercentage] = useState(null);
  const [neutralPercentage, setNeutralPercentage] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (event) => {
    setSearchQuery(event.target.value);
    // Clear previous error when user starts typing
    if (error) setError(null);
  };

  const handleSearch = async () => {
<<<<<<< HEAD
    // Validate input
    if (!searchQuery.trim()) {
      setError("Please enter a search term");
      return;
    }

    setLoading(true);
    setResponseMessage("");
    setChartVisible(false);
    setError(null);
    
=======
    setLoading(true);
    setResponseMessage("");
    setChartVisible(false);
>>>>>>> c6b76d29a7c57eb0443c65b9a41d272b5249c7e4
    console.log("User Input:", searchQuery);
    
    try {
      const response = await axios.post("http://127.0.0.1:8081/api/variable", {
        searchQuery: searchQuery.trim(),
      });

      const { 
        message, 
        total, 
        positive_percentage, 
        negative_percentage, 
        neutral_percentage 
      } = response.data;

<<<<<<< HEAD
      setResponseMessage(message);
      setTotalTweets(total);
      setPositivePercentage(positive_percentage);
      setNegativePercentage(negative_percentage);
      setNeutralPercentage(neutral_percentage);
      setChartVisible(true);
    } catch (error) {
      console.error("Error during search:", error);
      setError(
        error.response?.data?.message || 
        "An error occurred while analyzing tweets. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
=======
      setTotalTweets(response.data.total);
      setPositivePercentage(response.data.positive_percentage);
      setNegativePercentage(response.data.negative_percentage);
      setNeutralPercentage(response.data.neutral_percentage);
      setLoading(false);
      setChartVisible(true);
    } catch (error) {
      console.error("Error during search:", error);
      setResponseMessage("An error occurred while searching.");
      setLoading(false);
>>>>>>> c6b76d29a7c57eb0443c65b9a41d272b5249c7e4
    }
  };

  return (
<<<<<<< HEAD
    <div className="mt-6 mb-4 flex flex-col gap-4">
      <h1 className="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
        Dive Into the Data
        <span className="text-blue-600 dark:text-blue-500">
          {" "}
          Discover Key Trends in
        </span>{" "}
        Tweets.
      </h1>
      
      <p className="text-lg font-normal text-gray-500 lg:text-xl dark:text-gray-400 mb-4">
        At TweetLense, we focus on unlocking insights from social media data,
        empowering users to analyze trends, conversations, and engagement on
        Twitter
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
        <MyChart
          total={totalTweets}
          positivePercentage={positivePercentage}
          negativePercentage={negativePercentage}
          neutralPercentage={neutralPercentage}
        />
      )}
    </div>
=======
    <>
      <div className="mt-6 mb-4 flex flex-col gap-4">
        <h1 className="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
          Dive Into the Data
          <span className="text-blue-600 dark:text-blue-500">
            {" "}
            Discover Key Trends in
          </span>{" "}
          Tweets.
        </h1>
        <p className="text-lg font-normal text-gray-500 lg:text-xl dark:text-gray-400 mb-4">
          At TweetLense, we focus on unlocking insights from social media data,
          empowering users to analyze trends, conversations, and engagement on
          Twitter
        </p>
        <div className="flex flex-col gap-4 justify-center items-center sm:flex-row py-16 border-r border-b border-gray-600 rounded-3xl shadow-[rgba(0,_0,_0,_0.24)_0px_3px_8px]">
          <Input
            type="text"
            placeholder="Search Tweets"
            value={searchQuery}
            onChange={handleInputChange}
            className="flex w-[80%] bg-white text-gray-500 rounded-xl sm:w-[30%] border border-gray-500 py-6"
          />
          <Button className="py-6" onClick={handleSearch}>
            Search
          </Button>
        </div>

        {loading && (
          <div className="flex justify-center my-4">
            <Spinner />
          </div>
        )}

        {chartVisible && (
          <MyChart
            total={totalTweets}
            positivePercentage={positivePercentage}
            negativePercentage={negativePercentage}
            neutralPercentage={neutralPercentage}
          />
        )}
      </div>
    </>
>>>>>>> c6b76d29a7c57eb0443c65b9a41d272b5249c7e4
  );
}