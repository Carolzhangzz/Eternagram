import "./popup.css";
import { useState, useRef, useEffect } from "react";

const Popup = ({ isShow, closeEvent }) => {
  const popupRef = useRef(0);
  const [username, setUsername] = useState("");
  const [code, setCode] = useState("");

  const closePopup = () => {
	//if (value.trim() === "") return;
    if (username.trim() === "" || code.trim() === "") return;
    const data = popupRef.current.animate([{ opacity: 1 }, { opacity: 0 }], {
      duration: 300,
      iterations: 1,
      easing: "ease-out",
    });
    data.onfinish = (e) => {
      closeEvent(username,code);
    };
  };
  useEffect(() => {
    if (isShow) {
      popupRef.current.animate([{ opacity: 1 }], {
        duration: 0,
        iterations: 1,
        fill: "forwards",
      });
      document.addEventListener("keyup", detectTabKey);

      function detectTabKey(e) {
        if (e.keyCode === 9) {
          const activeElem = document.activeElement;
          if (activeElem.className=== "confirm") {
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
            <img src="/logo.png" alt="" />
            {/* <b>Please enter your id before starting the game!!!</b> */}
          </div>
          <div className="popup-content">
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="user name"
            />
            <input
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              onKeyDown={(e) => {
                if (e.code === "Enter") closePopup();
              }}
              placeholder="pin code"
            />
          </div>
          <div className="popup-footer">
            {/* <button className='cancel'>Ok,i already know</button> */}
            <button className="confirm" onClick={closePopup}>
              {/* Ok,i already know */}
              Log in
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Popup;

