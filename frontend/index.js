"use-strict";

const cards = document.querySelectorAll(".card");
const status = document.querySelectorAll(".status");
const timeDetails = document.querySelectorAll(".time");
const times = document.querySelectorAll(".time>p");

const changeStage = (index) => {
  cards[index].style.cssText = "background: hsl(359, 100%, 65%)";
  timeDetails[index].style.cssText = "visibility: visible;";
};

const updateData = (data) => {
  data.result.forEach((element) => {
    if (!element.isAvailable) {
      let index = Number(element.room_number);
      changeStage(index - 1);
    }
  });
};

const updateTime = (data, num) => {
  times[num - 1].textContent = data.result;
};

const getData = () => {
  fetch(`https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/get/all`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      window.setInterval(updateData(data), 2000);
      window.setInterval(updateTime(data), 2000);
    })
    .catch((err) => {
      console.log(err.message);
    });
};

const getTime = () => {
  let number = [1, 2, 3];
  number.forEach((num) => {
    fetch(
      `https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/get/average/` +
        number,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      }
    )
      .then((res) => res.json())
      .then((data) => {
        console.log(res);
        window.setInterval(updateTime(data, num), 2000);
      })
      .catch((err) => {
        console.log(err.message);
      });
  });
};
