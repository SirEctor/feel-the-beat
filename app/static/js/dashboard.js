const firstDate = new Date();
const todaysDate = new Date();


const displayCalendar = () => {
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

  firstDate.setDate(1);

  document.querySelector("#title").innerHTML = new Date().toDateString();

  document.querySelector(".date h1").innerHTML =
    months[firstDate.getMonth()] + " " + firstDate.getFullYear();

  // current month - last day
  const lastDay = new Date(
    firstDate.getFullYear(),
    firstDate.getMonth() + 1,
    0
  ).getDate();

  // previous month - last day
  const prevLastDay = new Date(
    firstDate.getFullYear(),
    firstDate.getMonth(),
    0
  ).getDate();

  // current month - first day of the week (Sun, Mon, etc)
  const lastDayIndex = new Date(
    firstDate.getFullYear(),
    firstDate.getMonth() + 1,
    0
  ).getDay();

  const nextDays = 7 - lastDayIndex - 1;

  let days = "";
  const firstDayIndex = firstDate.getDay();

  // get prev month days
  for (let x = firstDayIndex; x > 0; x--) {
    days += `<button class="prevDateButton">${prevLastDay - x + 1}</button>`;
  }

  // get current month days
  for (let i = 1; i <= lastDay; i++) {
    if (
      i === new Date().getDate() &&
      firstDate.getMonth() === new Date().getMonth() &&
      firstDate.getFullYear() === new Date().getFullYear()
    ) {
      days += `<button class="todayButton">${i}</button>`;
    } else {
      days += `<button>${i}</button>`;
    }
  }

  const monthDays = document.querySelector(".days");

  //get next month days
  for (let j = 1; j <= nextDays; j++) {
    days += `<button class="nextDateButton">${j}</button>`;
    monthDays.innerHTML = days;
  }
};

document.querySelector(".backwardArrow").addEventListener("click", () => {
  firstDate.setMonth(firstDate.getMonth() - 1);
  displayCalendar();
});

document.querySelector(".forwardArrow").addEventListener("click", () => {
  firstDate.setMonth(firstDate.getMonth() + 1);
  displayCalendar();
});

displayCalendar();
