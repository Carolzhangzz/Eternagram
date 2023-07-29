import React from 'react';
import "./popup.css";
import alertFn from "./../../tool/alert-tips";
import { useState, useRef, useEffect } from "react";

const Popup = ({ isShow, closeEvent }) => {
  const popupRef = useRef(0);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);

  const closePopup = () => {
    //if (value.trim() === "") return;
    if (username.trim() === "" || password.trim() === "") {
      alertFn({ title: "Please enter your account and password." });
      return;
    }
    closeEvent(username, password, isLogin);
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
          if (activeElem.className === "confirm") {
            return;
          }
          // document.querySelector(".confirm").focus();
        }
      }
    }
  }, [isShow]);

  const ChangeIsLogin = (value) => {
    setIsLogin(value);
    setPassword("");
    setUsername("");
  };

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
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => {
                if (e.code === "Enter") closePopup();
              }}
              placeholder="password"
            />
          </div>
          <div className="popup-footer">
            <button className="confirm" onClick={closePopup}>
              {isLogin ? "Log in" : "Sign up"}
            </button>
          </div>
        </div>
        <div className="tips">
          {isLogin ? (
            <div>
              Don't have an account?
              <b
                onClick={() => {
                  ChangeIsLogin(false);
                }}
              >
                Sign up
              </b>
            </div>
          ) : (
            <div>
              Have an account?
              <b
                onClick={() => {
                  ChangeIsLogin(true);
                }}
              >
                Log in
              </b>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Popup;
