const player1Button = document.querySelector("#player1Button");
const player2Button = document.querySelector("#player2Button");
const player1Container = document.querySelector(".player1Container");
const player2Container = document.querySelector(".player2Container");

player1Button.addEventListener("click", async () => {
  const recording = document.createElement("div");
  recording.setAttribute("class", "recordingContainer1 hidden");
  recording.setAttribute("id", "recordingContainer1");
  recording.innerHTML = `
    <button class="pulsatingCircle"><i class="fa-solid fa-circle"></i></button>
    <h3 class="recordingText">Recording</h3>
  `
  player1Container.prepend(recording);
  const recordingContainer = document.querySelector("#recordingContainer1");
  player1Button.classList.add("hidden");
  recordingContainer.classList.remove("hidden");
  player2Button.disabled = false;
  player2Button.classList.add("disabled");
  try {
    const response = await fetch("/getfocuslevels", { method: "GET" });
    const response2 = await fetch("http://127.0.0.1:5000/parse-json", { method: "GET" });
    const data = await response.json();
    // Whatever we want to do with the data recorded from the the EEG
    // Put the logic here
    console.log(data['alpha']);
  } catch (error) {
    console.error(error.message);
  }
  try {
    const response = await fetch(("http://127.0.0.1:5000/run-all"),{ method: "GET" });
    console.log(data);
  } catch (error) {
    console.error(error.message);
  }
  player1Button.classList.remove("hidden");
  recordingContainer.classList.add("hidden");
  player2Button.disabled = false;
  player2Button.classList.remove("disabled");
});
player2Button.addEventListener("click", async () => {
  const recording = document.createElement("div");
  recording.setAttribute("class", "recordingContainer2 hidden");
  recording.setAttribute("id", "recordingContainer2");
  recording.innerHTML = `
    <button class="pulsatingCircle"><i class="fa-solid fa-circle"></i></button>
    <h3 class="recordingText">Recording</h3>
  `
  player2Container.prepend(recording);
  const recordingContainer = document.querySelector("#recordingContainer2");
  player2Button.classList.add("hidden");
  recordingContainer.classList.remove("hidden");
  player1Button.disabled = false;
  player1Button.classList.add("disabled");
  try {
    const response = await fetch("/getfocuslevels", { method: "GET" });
    const response2 = await fetch("http://127.0.0.1:5000/parse-json", { method: "GET" });
    const data = await response.json();
    // Whatever we want to do with the data recorded from the the EEG
    // Put the logic here
    console.log(data['alpha']);
  } catch (error) {
    console.error(error.message);
  }
  player2Button.classList.remove("hidden");
  recordingContainer.classList.add("hidden");
  player1Button.disabled = false;
  player1Button.classList.remove("disabled");
});
  