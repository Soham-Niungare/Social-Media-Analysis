export function Legend({ data }) {
  return (
    <>
      <div className="hidden absolute right-10 bottom-0 bg-white shadow-lg p-2 rounded border md:block">
        {data.map((entry) => (
          <div key={entry.name} className="flex items-center mb-1">
            <div
              className="w-4 h-4 mr-2"
              style={{ backgroundColor: entry.fill }}
            ></div>
            <span className="text-sm">
              {entry.name}: {entry.value.toFixed(2)}%
            </span>
          </div>
        ))}
      </div>
    </>
  );
}
