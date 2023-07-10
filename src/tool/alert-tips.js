export default function({
  title,
  duration = 5000,
  textColor = "#747474",
  customControl = false,
}) {
  const key = Math.random()
    .toString(16)
    .slice(2, 7)
    .padEnd(
      10,
      Math.random()
        .toString(16)
        .slice(2)
    );

  const tem = `<div class="alert-tips alert-tips-${key}" style="color:${textColor}">${title}</div>`;
  const box = document.querySelector(".alert-tips-box");
  box.innerHTML += tem;
  const addAni = document.querySelector(`.alert-tips-${key}`).animate(
    [
      {
        opacity: 0,
        transform: "translateX(3em)",
      },
      {
        opacity: 1,
        transform: "translateX(0)",
      },
    ],
    {
      duration: 300,
      iterations: 1,
      fill: "forwards",
    }
  );
  addAni.onfinish = (e) => {
    e.currentTarget.effect.target.style.opacity = 1;
  };

  if (customControl) {
    let i = false;
    return () => {
      console.log("开始")
      if (i) return;
      i = true;
      console.log("执行了")
      closeFn(box, key);
    };
  }

  setTimeout(() => {
    closeFn(box, key);
  }, duration);
}

function closeFn(box, key) {
  const ani = document.querySelector(`.alert-tips-${key}`).animate(
    [
      {
        opacity: 0,
      },
    ],
    {
      duration: 300,
      iterations: 1,
      fill: "forwards",
    }
  );
  setTimeout(() => {
    const top = box.style.top;
    if (top === "") box.style.top = "-3em";
    else box.style.top = parseInt(box.style.top) - 4 + "em";
  }, 200);

  ani.onfinish = (e) => {
    e.currentTarget.effect.target.style.opacity = 0;
  };
}
