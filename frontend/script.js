async function changeText() {
    const data = await fetch('http://127.0.0.1:5000/')
  .then(response => response.json())
  .then(json => json)

  console.log(data)

document.getElementById("heading").innerText = data.title
document.getElementById("completed").innerText = data.completed

}   

