import loading from "./loading.gif"; // Make sure the path to the image is correct

export function Spinner() {
  return (
    <div className="flex flex-col gap-2 justify-center items-center">
      <img src={loading} alt="Loading..." className="w-16 h-16" />{" "}
      <p className="text-md font-semibold text-gray-600">
        Fetching data and generating insights, please wait...
      </p>
    </div>
  );
}
