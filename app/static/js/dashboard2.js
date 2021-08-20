const date_picker_element = document.querySelector(".date-picker");
const selected_date_element = document.querySelector(
  ".date-picker .selected-date"
);
const dates_element = document.querySelector(".date-picker .dates");
const mth_element = document.querySelector(".date-picker .dates .month .mth");
const next_mth_element = document.querySelector(
  ".date-picker .dates .month .next-mth"
);
const prev_mth_element = document.querySelector(
  ".date-picker .dates .month .prev-mth"
);
const days_element = document.querySelector(".date-picker .dates .days");

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

/* const cors = require("cors"); //check
const app = express();
app.use(cors()); */

let date = new Date();
let day = date.getDate();
let month = date.getMonth();
let year = date.getFullYear();

let selectedDate = date;
let selectedDay = day;
let selectedMonth = month;
let selectedYear = year;

mth_element.textContent = months[month] + " " + year;

selected_date_element.textContent = formatDate(date);
selected_date_element.dataset.value = selectedDate;

populateDates();

// EVENT LISTENERS
date_picker_element.addEventListener("click", toggleDatePicker);
next_mth_element.addEventListener("click", goToNextMonth);
prev_mth_element.addEventListener("click", goToPrevMonth);

// FUNCTIONS
function toggleDatePicker(e) {
  if (!checkEventPathForClass(e.path || (e.composedPath && e.composedPath()), "dates")) {
    dates_element.classList.toggle("active");
  }
  checkMood();
}

function goToNextMonth(e) {
  month++;
  if (month > 11) {
    month = 0;
    year++;
  }
  mth_element.textContent = months[month] + " " + year;
  populateDates();
}

function goToPrevMonth(e) {
  month--;
  if (month < 0) {
    month = 11;
    year--;
  }
  mth_element.textContent = months[month] + " " + year;
  populateDates();
}

function populateDates(e) {
  days_element.innerHTML = "";
  let amount_days = 31;

  if (month == 1) {
    amount_days = 28;
  }

  for (let i = 0; i < amount_days; i++) {
    const day_element = document.createElement("div");
    day_element.classList.add("day");
    day_element.textContent = i + 1;

    if (
      selectedDay == i + 1 &&
      selectedYear == year &&
      selectedMonth == month
    ) {
      day_element.classList.add("selected");
    }

    day_element.addEventListener("click", function () {
      selectedDate = new Date(year + "-" + (month + 1) + "-" + (i + 1));
      selectedDay = i + 1;
      selectedMonth = month;
      selectedYear = year;

      selected_date_element.textContent = formatDate(selectedDate);
      selected_date_element.dataset.value = selectedDate;

      populateDates();
      checkMood(); //Check
    });

    days_element.appendChild(day_element);
  }
}

// HELPER FUNCTIONS
function checkEventPathForClass(path, selector) {
  for (let i = 0; i < path.length; i++) {
    if (path[i].classList && path[i].classList.contains(selector)) {
      return true;
    }
  }

  return false;
}
function formatDate(d) {
  let day = d.getDate();
  if (day < 10) {
    day = "0" + day;
  }

  let month = d.getMonth() + 1;
  if (month < 10) {
    month = "0" + month;
  }

  let year = d.getFullYear();

  return day + " / " + month + " / " + year;
}

function formatDateAPI(d) {
  let day = d.getDate();
  if (day < 10) {
    day = "0" + day;
  }

  let month = d.getMonth() + 1;
  if (month < 10) {
    month = "0" + month;
  }

  let year = d.getFullYear();

  return year + "-" + month + "-" + day + " 00:00:00";
}

function checkMood() {
  const url = "https://feelthebeat.tech/api/daily-record";

  const otherPram = {
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      //date: formatDateAPI,
      date: formatDateAPI(selectedDate),
    }),
    method: "POST",
  };

  fetch(url, otherPram)
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      if (jQuery.isEmptyObject(data)) {
        document.querySelector(".dayMood").innerHTML = "No data from this day";
        document.querySelector(".songArtist").innerHTML = "";
      } else {
        console.log(data);
        var mood = data["mood"];
        var artist = data["artist"];
        var name = data["name"];

        document.querySelector(".dayMood").innerHTML = mood;
        document.querySelector(".songArtist").innerHTML = name + "-" + artist;

        switch (mood) {
          case "love":
            document.getElementById("moodEmogi").innerHTML =
              '<i class="far fa-grin-hearts emoji love"></i>';
            break;
          case "happy":
            document.getElementById("moodEmogi").innerHTML =
              '<i class="far fa-laugh-beam emoji happy"></i>';
            break;
          case "normal":
            document.getElementById("moodEmogi").innerHTML =
              '<i class="far fa-meh emoji normal"></i>';
            break;
          case "sad":
            document.getElementById("moodEmogi").innerHTML =
              '<i class="far fa-frown emoji sad"></i>';
            break;

          case "angry":
            document.getElementById("moodEmogi").innerHTML =
              '<i class="far fa-angry emoji angry"></i>';
            break;
          default:
            document.getElementById("moodEmogi").innerHTML = "<i></i>";
            break;
        }
      }
    })
    .catch((error) => console.log(error));
}
