import { createPortal } from "react-dom";
import "./index.css";
import { useEffect } from "react";

const SystemText = (props) => {
  return (
    <p className="systemText">
      <span>[SYSTEM]</span> {props.text}
    </p>
  );
};

const UserText = (props) => {
  return (
    <p className="userText">
      <span>[USER]</span> {props.text}
    </p>
  );
};

const Terminal = ({ message }) => {
  return (
    <>
      {message.map((item, index) => {
        if (item.it) {
          return <SystemText key={index} text={item.text} />;
        } else {
          return <UserText key={index} text={item.text} />;
        }
      })}
    </>
  );
};

const TerminalDiv = ({ terminalMessage }) => {
  useEffect(() => {
    setTimeout(() => {
      const element = document.querySelector(".systemText:last-child");
      element && element.scrollIntoView();
    }, 10);
  }, [terminalMessage]);
  return (
    <div className="terminalBox">
      <div className="terminalHead">Terminal</div>
      <div className="terminalContext">
        <Terminal message={terminalMessage} />
      </div>
    </div>
  );
};

export default TerminalDiv;
