import { useState, useEffect } from "react";

export function Home() {
  const [news, setNews] = useState([]);

  const getNews = () => {
    fetch(
      "https://newsapi.org/v2/everything?q=Apple&from=2024-10-17&sortBy=popularity&apiKey=c3ccaecb001a45e0864b03adcc94ca9c"
    )
      .then((res) => res.json())
      .then((json) => console.log(json));
  };

  useEffect(() => {
    getNews();
  }, []);

  return (
    <>
      <div>Nishad</div>
    </>
  );
}
