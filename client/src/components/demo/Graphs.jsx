import { MyChart } from "./ChartDemo1";
import { YourChart } from "./ChartDemo2";

export function Graphs() {
  return (
    <>
      <div className="grid grid-cols-1 gap-4 my-4 mx-4 lg:grid-cols-2 lg:gap-8">
        <MyChart />
        <YourChart />
      </div>
    </>
  );
}
