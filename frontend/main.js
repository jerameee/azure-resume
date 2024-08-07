window.addEventListener('DOMContentLoaded', () =>{
    getVisitCount();
})

const functionApi = 'http://localhost:5004/api/main';

const getVisitCount = () => {
    let count = 0;
    fetch(functionApi).then(response => {
        return response.json()
    }).then(response => {
        console.log("Website called function API.");
        count = response.new_count;
        document.getElementById("counter").innerText = count;
    }).catch(function(error) {
        console.log(error);
    });
    return count;
}