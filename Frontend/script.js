class TaxiDataExplorer {
    constructor() {
        this.summary = {};
        this.tripsOverTime = [];
        this.avgSpeedByPassenger = [];
        this.charts = {};
        this.init();
    }


    async init() {
        await this.loadSummary();
        await this.loadTripsOverTime();
        await this.loadAvgSpeedByPassenger();
    }


    // Load summary stats from backend
    async loadSummary() {
        try {
            const res = await fetch('http://127.0.0.1:5000/api/summary');
            const data = await res.json();


            this.summary = data;


            document.getElementById('totalTrips').textContent = data.total_trips.toLocaleString();
            document.getElementById('avgDuration').textContent = (data.avg_duration_min || 0).toFixed(2);
            document.getElementById('vendor1Speed').textContent = (data.vendor_1_avg_speed || 0).toFixed(2);
            document.getElementById('vendor2Speed').textContent = (data.vendor_2_avg_speed || 0).toFixed(2);


        } catch (err) {
            console.error("Error loading summary:", err);
        }
    }


    // Load trips over time and populate line chart
    async loadTripsOverTime() {
        try {
            const res = await fetch('http://127.0.0.1:5000/api/trips_over_time');
            const trips = await res.json();


            this.tripsOverTime = trips;


            this.createTripsOverTimeChart();
            this.updateTripsTable();
        } catch (err) {
            console.error("Error loading trips over time:", err);
        }
    }


    // Load average speed by passenger and populate bar chart
    async loadAvgSpeedByPassenger() {
        try {
            const res = await fetch('http://127.0.0.1:5000/api/avg_speed_by_passenger');
            const speeds = await res.json();


            this.avgSpeedByPassenger = speeds;


            this.createAvgSpeedByPassengerChart();
        } catch (err) {
            console.error("Error loading avg speed by passenger:", err);
        }
    }
    
    // -------- Charts --------
    createTripsOverTimeChart() {
        const ctx = document.getElementById('tripsOverTimeChart').getContext('2d');


        const labels = this.tripsOverTime.map(t => t.pickup_date);
        const data = this.tripsOverTime.map(t => t.trip_count || 0);


        if (this.charts.tripsOverTime) this.charts.tripsOverTime.destroy();


        this.charts.tripsOverTime = new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Trips Over Time',
                    data,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102,126,234,0.2)',
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }


    createAvgSpeedByPassengerChart() {
        const ctx = document.getElementById('avgSpeedByPassengerChart').getContext('2d');


        const labels = this.avgSpeedByPassenger.map(s => `Pax ${s.passenger_count}`);
        const data = this.avgSpeedByPassenger.map(s => s.avg_speed);


        if (this.charts.avgSpeedByPassenger) this.charts.avgSpeedByPassenger.destroy();


        this.charts.avgSpeedByPassenger = new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Average Speed by Passenger',
                    data,
                    backgroundColor: '#667eea'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }


    // -------- Table --------
    updateTripsTable() {
        const tbody = document.getElementById('tripsTableBody');
        if (!tbody) return;


        tbody.innerHTML = '';


        this.tripsOverTime.slice(0, 20).forEach((trip, i) => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${i + 1}</td>
                <td>${trip.pickup_date}</td>
                <td>${trip.trip_distance || 'N/A'}</td>
                <td>${trip.fare_amount || 'N/A'}</td>
                <td>${trip.payment_type || 'N/A'}</td>
            `;
        });
    }
}


// Initialize dashboard after DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new TaxiDataExplorer();
});
