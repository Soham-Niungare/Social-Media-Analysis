export function NewsCard({ article }) {
  return (
    <>
      <div className="border border-gray-400 rounded-b-3xl hover:shadow-[rgba(0,_0,_0,_0.24)_0px_3px_8px]">
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block"
        >
          {" "}
          {article.urlToImage && (
            <img
              alt={article.title}
              src={article.urlToImage}
              className="h-24 w-full object-cover sm:h-32 lg:h-64"
            />
          )}
          <div className="m-2">
            <h3 className="mt-4 text-lg font-bold text-gray-900 sm:text-xl">
              {article.title} {/* Display title */}
            </h3>

            <p className="mt-2 max-w-sm text-gray-700">
              {article.description} {/* Display description */}
            </p>
          </div>
        </a>
      </div>
    </>
  );
}
