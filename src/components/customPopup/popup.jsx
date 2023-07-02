import "./popup.css";
import { useState, useRef, useEffect } from "react";

const Popup = ({ isShow, closeEvent }) => {
  const popupRef = useRef(0);
  const [value, setValue] = useState("");

  const closePopup = () => {
    if (value.trim() == "") return;
    const data = popupRef.current.animate([{ opacity: 1 }, { opacity: 0 }], {
      duration: 300,
      iterations: 1,
      easing: "ease-out",
    });
    data.onfinish = (e) => {
      closeEvent(value);
    };
  };
  useEffect(() => {
    if (isShow) {
      popupRef.current.animate([{ opacity: 0 }, { opacity: 1 }], {
        duration: 200,
        iterations: 1,
        fill: "forwards",
        easing: "ease-in",
      });
      document.addEventListener("keyup", detectTabKey);

      function detectTabKey(e) {
        if (e.keyCode == 9) {
          const activeElem = document.activeElement;
          if (activeElem.className == "confirm") {
            console.log(activeElem.href);
            return;
          }
          document.querySelector(".confirm").focus();
        }
      }
    }
  }, [isShow]);

  return (
    <>
      <div
        ref={(ref) => {
          popupRef.current = ref;
        }}
        className={`mask ${isShow ? "show" : "close"}`}
      >
        <div className="popup">
          <div className="popup-header">
            <b>Please enter your id before starting the game!!!</b>
          </div>
          <div className="popup-content">
            <div>Notice:</div>
            {/* <p>1. The first information you enter will become your user ID</p> */}
            <p>
              Please remember this id and enter the same id before each start to
              prevent the loss of previous game records
            </p>
            <input
              type="text"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.code == "Enter") closePopup();
              }}
              placeholder="Please input your id"
            />
          </div>
          <div className="popup-footer">
            {/* <button className='cancel'>Ok,i already know</button> */}
            <button className="confirm" onClick={closePopup}>
              {/* Ok,i already know */}
              Start
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Popup;
