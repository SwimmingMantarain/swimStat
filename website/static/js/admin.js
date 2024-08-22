async function restartSSHConnection() {
    const response = await fetch("/restart-tunnel", {
        method: "POST",
        body: JSON.stringify({})
    }).then((_res) => {
        window.location.href = "/";
    });
}

const fetchData = () => {
    fetch('/admin', {method: 'POST', headers: {'Content-Type': 'application/json'}, body:JSON.stringify({"diag" : "diag"})}).then(response => {
        return response.json();
    }).then(data => {
        data = data[0];

        const temps = data[0];
        const cores = data[1];
        const temp_avg = data[2];
        const meminfo = data[3];

        const diagBlocks = document.querySelectorAll(
            '#system-diagnostics #diagnostics-block'
        );

        // Temperature
        const tempBlock = diagBlocks[0];
        // Keep the header
        const tempHeader = tempBlock.querySelector('h1');
        tempBlock.innerHTML = '';
        tempBlock.appendChild(tempHeader);
        temps.forEach((coretemp, index) => {
            const p = document.createElement('p');
            p.textContent = `Core ${index}: +${coretemp}°C`;
            tempBlock.appendChild(p);
        });

        // CPU Core Usage
        const coreUsageBlock = diagBlocks[1];
        // Keep the header
        const coreUsageHeader = coreUsageBlock.querySelector('h1');
        coreUsageBlock.innerHTML = '';
        coreUsageBlock.appendChild(coreUsageHeader);
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
        ).textContent = `${temps.length} Cores: +${temp_avg}°C`;
        cpuAveragesBlock.querySelector(
            '#freq-avg'
        ).textContent = `Average CPU Frequency: ${((cores.reduce((a, b) => a + b, 0) / cores.length) / 1000.0).toFixed(2)} GHz`;

        // Memory Usage
        const memUsageBlock = diagBlocks[3];
        memUsageBlock.querySelector(
            '#memory-usage'
        ).textContent = `Memory Usage: ${((meminfo[0] - meminfo[1])).toFixed(2)}/${(meminfo[0]).toFixed(2)} GB`;
        memUsageBlock.querySelector(
            '#memory-available'
        ).textContent = `Memory Available: ${(meminfo[1]).toFixed(2)} GB`;
    });
};

fetchData();
setInterval(fetchData, 10000);