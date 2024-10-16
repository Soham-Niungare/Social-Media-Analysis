import { Input } from "@/components/ui/input";
import { Button } from "../ui/button";

export function InputDemo() {
  return (
    <>
      <div className="mt-6 mb-4">
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
            className="flex w-[80%] bg-white text-gray-500 rounded-xl sm:w-[30%] border border-gray-500 py-6"
          />
          <Button className="py-6">Search</Button>
        </div>
      </div>
    </>
  );
}
