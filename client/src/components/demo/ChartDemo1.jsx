"use client";

import * as React from "react";
import { TrendingUp } from "lucide-react";
import { Label, Pie, PieChart } from "recharts";
import { Legend } from "./Legend";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

export function MyChart({
  total,
  positivePercentage,
  negativePercentage,
  neutralPercentage,
}) {
  const chartData = [
    {
      name: "Positive",
      value: positivePercentage || 0,
      fill: "hsl(var(--chart-2))",
    },
    {
      name: "Negative",
      value: negativePercentage || 0,
      fill: "hsl(var(--chart-1))",
    },
    {
      name: "Neutral",
      value: neutralPercentage || 0,
      fill: "hsl(var(--chart-4))",
    },
  ];

  return (
    <Card className="flex flex-col hover:shadow-[0_35px_60px_-15px_rgba(0,0,0,0.3)]">
      <CardHeader className="items-center pb-0">
        <CardTitle>Sentiment Analysis Pie Chart</CardTitle>
        <CardDescription>Real-time sentiment analysis</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0 relative">
        <Legend data={chartData} />
        <ChartContainer
          config={chartData}
          className="mx-auto aspect-square max-h-[250px]"
        >
          <PieChart>
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Pie
              data={chartData}
              dataKey="value"
              nameKey="name"
              innerRadius={60}
              strokeWidth={5}
            >
              <Label
                content={({ viewBox }) => {
                  if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                    return (
                      <text
                        x={viewBox.cx}
                        y={viewBox.cy}
                        textAnchor="middle"
                        dominantBaseline="middle"
                      >
                        <tspan
                          x={viewBox.cx}
                          y={viewBox.cy}
                          className="fill-foreground text-3xl font-bold"
                        >
                          {total.toLocaleString()}
                        </tspan>
                        <tspan
                          x={viewBox.cx}
                          y={(viewBox.cy || 0) + 24}
                          className="fill-muted-foreground"
                        >
                          Tweets Fetched
                        </tspan>
                      </text>
                    );
                  }
                }}
              />
            </Pie>
          </PieChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm">
        <div className="flex items-center gap-2 leading-none text-xl font-semibold">
          Sentiment Analysis
          <TrendingUp className="h-4 w-4" />
        </div>
        <div className="leading-none text-muted-foreground">
          Data based on fetched tweets
        </div>
      </CardFooter>
    </Card>
  );
}
