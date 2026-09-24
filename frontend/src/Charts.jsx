import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Bar, Doughnut } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function Charts({ data = {} }) {
  const loginEvents = Number(data.login_events) || 0;
  const fileEvents = Number(data.file_events) || 0;
  const usbEvents = Number(data.usb_events) || 0;
  const failedLogins = Number(data.failed_logins) || 0;

  /* =========================
     SECURITY EVENT OVERVIEW
     ========================= */

  const eventOverview = {
    labels: [
      "Login Events",
      "File Events",
      "USB Events",
      "Failed Logins",
    ],
    datasets: [
      {
        label: "Security Events",
        data: [
          loginEvents,
          fileEvents,
          usbEvents,
          failedLogins,
        ],
        backgroundColor: [
          "#009688",
          "#26A69A",
          "#FF9800",
          "#E53935",
        ],
        borderRadius: 8,
        borderSkipped: false,
      },
    ],
  };

  const eventOptions = {
    responsive: true,
    maintainAspectRatio: false,

    plugins: {
      legend: {
        display: false,
      },

      tooltip: {
        backgroundColor: "#172033",
        padding: 12,
        titleFont: {
          size: 14,
          weight: "700",
        },
        bodyFont: {
          size: 13,
        },
      },
    },

    scales: {
      x: {
        grid: {
          display: false,
        },

        ticks: {
          color: "#607D8B",
          font: {
            size: 12,
            weight: "600",
          },
        },
      },

      y: {
        beginAtZero: true,

        ticks: {
          precision: 0,
          color: "#607D8B",
          font: {
            size: 12,
          },
        },

        grid: {
          color: "#E0E7EA",
        },
      },
    },
  };

  /* =========================
     FILE ACTIVITY
     ========================= */

  const fileData = {
    labels: ["File Events", "Other Events"],
    datasets: [
      {
        data: [
          fileEvents,
          Math.max(loginEvents + usbEvents + failedLogins, 0),
        ],
        backgroundColor: [
          "#26A69A",
          "#DCE5E8",
        ],
        borderWidth: 0,
      },
    ],
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,

    cutout: "68%",

    plugins: {
      legend: {
        position: "bottom",

        labels: {
          color: "#455A64",
          padding: 18,
          font: {
            size: 12,
            weight: "600",
          },
        },
      },

      tooltip: {
        backgroundColor: "#172033",
        padding: 12,
      },
    },
  };

  /* =========================
     USB USAGE
     ========================= */

  const usbData = {
    labels: ["USB Events", "No USB Activity"],
    datasets: [
      {
        data: [
          usbEvents,
          usbEvents > 0 ? 0 : 1,
        ],
        backgroundColor: [
          "#FF9800",
          "#DCE5E8",
        ],
        borderWidth: 0,
      },
    ],
  };

  const usbOptions = {
    responsive: true,
    maintainAspectRatio: false,

    cutout: "68%",

    plugins: {
      legend: {
        position: "bottom",

        labels: {
          color: "#455A64",
          padding: 18,
          font: {
            size: 12,
            weight: "600",
          },
        },
      },

      tooltip: {
        backgroundColor: "#172033",
        padding: 12,
      },
    },
  };

  return (
    <>
      {/* =========================
          SECURITY EVENT OVERVIEW
          ========================= */}

      <div className="chart-card">
        <h2>📊 Security Event Overview</h2>

        <div style={{ height: "280px" }}>
          <Bar
            data={eventOverview}
            options={eventOptions}
          />
        </div>
      </div>

      {/* =========================
          FILE ACTIVITY
          ========================= */}

      <div className="chart-card">
        <h2>📁 File Activity</h2>

        <div style={{ height: "280px" }}>
          <Doughnut
            data={fileData}
            options={doughnutOptions}
          />
        </div>
      </div>

      {/* =========================
          USB USAGE
          ========================= */}

      <div className="chart-card">
        <h2>🔌 USB Usage</h2>

        <div style={{ height: "280px" }}>
          <Doughnut
            data={usbData}
            options={usbOptions}
          />
        </div>
      </div>
    </>
  );
}

export default Charts;