import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const ChartComponent = ({ chartData }) => {
  if (!chartData || !chartData.data) {
    return null;
  }

  const { type, data } = chartData;

  let chartConfig = {};

  if (type === 'price_trend') {
    const years = data.map(d => d.year);
    const flatRates = data.map(d => d.avg_flat_rate);
    const officeRates = data.map(d => d.avg_office_rate);
    const shopRates = data.map(d => d.avg_shop_rate);

    chartConfig = {
      type: 'line',
      data: {
        labels: years,
        datasets: [
          {
            label: 'Flat Avg Rate (₹/sqft)',
            data: flatRates,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1
          },
          {
            label: 'Office Avg Rate (₹/sqft)',
            data: officeRates,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.1
          },
          {
            label: 'Shop Avg Rate (₹/sqft)',
            data: shopRates,
            borderColor: 'rgb(255, 205, 86)',
            backgroundColor: 'rgba(255, 205, 86, 0.2)',
            tension: 0.1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Price Trends Over Years' }
        },
        scales: {
          y: {
            beginAtZero: false,
            title: { display: true, text: 'Rate (₹/sqft)' }
          },
          x: {
            title: { display: true, text: 'Year' }
          }
        }
      }
    };
  } else if (type === 'demand_trend') {
    const years = data.map(d => d.year);
    const totalSold = data.map(d => d.total_sold);
    const flatSold = data.map(d => d.flat_sold);
    const officeSold = data.map(d => d.office_sold);
    const shopSold = data.map(d => d.shop_sold);

    chartConfig = {
      type: 'bar',
      data: {
        labels: years,
        datasets: [
          {
            label: 'Total Units Sold',
            data: totalSold,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgb(54, 162, 235)',
            borderWidth: 1
          },
          {
            label: 'Flats Sold',
            data: flatSold,
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgb(75, 192, 192)',
            borderWidth: 1
          },
          {
            label: 'Offices Sold',
            data: officeSold,
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1
          },
          {
            label: 'Shops Sold',
            data: shopSold,
            backgroundColor: 'rgba(255, 205, 86, 0.6)',
            borderColor: 'rgb(255, 205, 86)',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Demand Trends Over Years' }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: 'Units Sold' }
          },
          x: {
            title: { display: true, text: 'Year' }
          }
        }
      }
    };
  } else if (type === 'price_comparison' || type === 'demand_comparison') {
    const localities = Object.keys(data);
    const years = data[localities[0]]?.map(d => d.year) || [];

    if (type === 'price_comparison') {
      const colors = [
        { border: 'rgb(75, 192, 192)', bg: 'rgba(75, 192, 192, 0.2)' },
        { border: 'rgb(255, 99, 132)', bg: 'rgba(255, 99, 132, 0.2)' },
        { border: 'rgb(255, 205, 86)', bg: 'rgba(255, 205, 86, 0.2)' },
        { border: 'rgb(54, 162, 235)', bg: 'rgba(54, 162, 235, 0.2)' }
      ];

      const datasets = localities.map((locality, idx) => ({
        label: `${locality} - Flat Rate`,
        data: data[locality].map(d => d.avg_flat_rate),
        borderColor: colors[idx % colors.length].border,
        backgroundColor: colors[idx % colors.length].bg,
        tension: 0.1
      }));

      chartConfig = {
        type: 'line',
        data: { labels: years, datasets },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Price Comparison Across Localities' }
          },
          scales: {
            y: {
              beginAtZero: false,
              title: { display: true, text: 'Rate (₹/sqft)' }
            },
            x: {
              title: { display: true, text: 'Year' }
            }
          }
        }
      };
    } else {
      const colors = [
        'rgba(75, 192, 192, 0.6)',
        'rgba(255, 99, 132, 0.6)',
        'rgba(255, 205, 86, 0.6)',
        'rgba(54, 162, 235, 0.6)'
      ];

      const datasets = localities.map((locality, idx) => ({
        label: `${locality} - Total Sold`,
        data: data[locality].map(d => d.total_sold),
        backgroundColor: colors[idx % colors.length],
        borderWidth: 1
      }));

      chartConfig = {
        type: 'bar',
        data: { labels: years, datasets },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Demand Comparison Across Localities' }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: 'Units Sold' }
            },
            x: {
              title: { display: true, text: 'Year' }
            }
          }
        }
      };
    }
  }

  return (
    <div style={{ maxWidth: '100%', height: '400px' }}>
      {chartConfig.type === 'line' ? (
        <Line data={chartConfig.data} options={chartConfig.options} />
      ) : (
        <Bar data={chartConfig.data} options={chartConfig.options} />
      )}
    </div>
  );
};

export default ChartComponent;
