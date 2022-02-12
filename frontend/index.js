const getBathroomStatus = (bathroomName) => {
    // Fetches the bathroom status from the server
    fetch('https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/get/all')
        .then(response => response.json())
        // get first element of the array
        .then(data => data[bathroomName-1])
        .then(data => {
            var currentDate = new Date();
            if (data.status) {
                document.getElementById('card' + bathroomName).style = "background-color: hsl(110, 100%, 65%); flex-direction: column;";
                // remaining time is time now - time last updated in seconds
                document.getElementById('time' + bathroomName).innerHTML = "";
            } else {
                document.getElementById('card' + bathroomName).style = "background-color: red; flex-direction: column;";
                document.getElementById('time' + bathroomName).innerHTML = data.time_pass;
            }
        })
}

const getEstimateTime = () => {
    fetch('https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/get/average/all')
        .then(response => response.json())
        .then(data => {
                document.getElementById("remaining").innerHTML = parseInt(data.average_time) + " seconds";
        })
}

window.setInterval (() => {
    getBathroomStatus(1)
    getBathroomStatus(2)
    getBathroomStatus(3)
},1000);

window.setInterval (() => {
    getEstimateTime()
},1000);