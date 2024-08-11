async function killTunnel() {
    const response = await fetch("/kill-tunnel", {
        method: "POST",
        body: JSON.stringify({ user: user })
    }).then((_res) => {
        window.location.href = "/";
    });
}

const fetchData = () => {
    fetch('/admin', {method: 'POST', headers: {'Content-Type': 'application/json'}, body:JSON.stringify({"diag" : "diag"})}).then(response => {
        return response.json();
    }).then(data => {
        const coretemps = data.coretemps;
        const cores = data.cores;
        const temp_avg = data.temp_avg;
        const meminfo = data.meminfo;

        const diagBlocks = document.querySelectorAll(
            '#system-diagnostics #diagnostics-block'
        );

        // Temperature
        const tempBlock = diagBlocks[0];
        tempBlock.innerHTML = '';
        coretemps.forEach((coretemp, index) => {
            const p = document.createElement('p');
            p.textContent = `Core ${index}: +${coretemp}°C`;
            tempBlock.appendChild(p);
        });

        // CPU Core Usage
        const coreUsageBlock = diagBlocks[1];
        coreUsageBlock.innerHTML = '';
        cores.forEach((core, index) => {
            const p = document.createElement('p');
            if (core > 1000) {
                p.textContent = `Core ${index}: ${(core / 1000.0).toFixed(2)} GHz`;
            } else {
                p.textContent = `Core ${index}: ${core.toFixed(2)} MHz`;
            }
            coreUsageBlock.appendChild(p);
        });

        // CPU Averages
        const cpuAveragesBlock = diagBlocks[2];
        cpuAveragesBlock.querySelector(
            '#temp-avg'
        ).textContent = `${coretemps.length} Cores: +${temp_avg}°C`;
        cpuAveragesBlock.querySelector(
            '#freq-avg'
        ).textContent = `Average CPU Frequency: ${((cores.reduce((a, b) => a + b, 0) / cores.length) / 1000.0).toFixed(2)} GHz`;

        // Memory Usage
        const memUsageBlock = diagBlocks[3];
        memUsageBlock.querySelector(
            '#memory-usage'
        ).textContent = `Memory Usage: ${((meminfo[0] - meminfo[1]) / 1024).toFixed(1)}/${(meminfo[0] / 1024).toFixed(1)} GB`;
        memUsageBlock.querySelector(
            '#memory-available'
        ).textContent = `Memory Available: ${(meminfo[2] < 1 ? (meminfo[2] * 1024).toFixed(2) : meminfo[2].toFixed(2))} MB`;
    });
};

fetchData();
setInterval(fetchData, 10000);