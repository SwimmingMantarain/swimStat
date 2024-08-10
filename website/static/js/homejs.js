// Example data, replace with actual data from your database
var totalKmSwum = 45; // Total kilometers swum
var totalKmSets = 30; // Total kilometers of sets

// Update summary statistics in the DOM
document.getElementById("totalKmSwum").textContent = totalKmSwum;
document.getElementById("totalKmSets").textContent = totalKmSets;

var ctx = document.getElementById("swimStatsChart").getContext("2d");
var swimStatsChart = new Chart(ctx, {
  type: "line", // Type of chart: line, bar, etc.
  data: {
    labels: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
    ], // X-axis labels
    datasets: [
      {
        label: "Swimming Distance (meters)",
        data: [1200, 1500, 800, 1700, 1900, 1600, 2100], // Dummy data
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});