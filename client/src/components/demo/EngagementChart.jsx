import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export function EngagementChart({ engagementData }) {
  const labels = engagementData.map((item) => item.metric);
  const positive = engagementData.map((item) => item.positive);
  const neutral = engagementData.map((item) => item.neutral);
  const negative = engagementData.map((item) => item.negative);

  const data = {
    labels,
    datasets: [
      {
        label: "Positive",
        data: positive,
        backgroundColor: "#2A9D8F", 
      },
      {
        label: "Neutral",
        data: neutral,
        backgroundColor: "#E9C46A", 
      },
      {
        label: "Negative",
        data: negative,
        backgroundColor: "#E76E50", 
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
        labels: {
          color: "#333",
          font: {
            size: 14,
          },
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#333",
          font: {
            size: 12,
          },
        },
      },
      y: {
        beginAtZero: true,
        ticks: {
          color: "#333",
          font: {
            size: 12,
          },
        },
      },
    },
  };

  return (
    <div className="w-full max-w-3xl mx-auto bg-white p-4 rounded-xl shadow-lg min-h-96">
      <h2 className="text-lg md:text-2xl font-bold text-center mb-4 text-gray-800">
        Engagement Metrics - Histogram
      </h2>
      <Bar data={data} options={options} />
    </div>
  );
}
