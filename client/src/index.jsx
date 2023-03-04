import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import React from "react";
import ReactDomClient from "react-dom/client";

import { App } from "./component";

const root = ReactDomClient.createRoot(document.querySelector("#app"));

root.render(<App />);

module.hot.accept();
