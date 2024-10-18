export function Legend({ data }) {
  return (
    <>
      <div className="absolute top-2 right-2 bg-white shadow-lg p-2 rounded border">
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
