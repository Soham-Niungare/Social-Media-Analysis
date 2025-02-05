import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function TrendIdentification() {
  const trends = [
    { id: 1, name: "#AI", count: 1234 },
    { id: 2, name: "#MachineLearning", count: 987 },
    { id: 3, name: "#DataScience", count: 876 },
    { id: 4, name: "#BigData", count: 765 },
    { id: 5, name: "#IoT", count: 654 },
  ];

  return (
    <section className="py-12">
      <div className="mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-extrabold text-gray-900 mb-6">
          Trend Identification
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trends.map((trend) => (
            <Card key={trend.id} className="cursor-pointer">
              <CardHeader>
                <CardTitle>{trend.name}</CardTitle>
                <CardDescription>Trending topic</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold">{trend.count} mentions</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
