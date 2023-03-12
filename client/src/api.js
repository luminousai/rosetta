const API_URL = "http://localhost:8081/";

const fetchJson = async (...options) => {
  const response = await fetch(...options);
  const data = await response.json();

  return data;
};

const postConvert = (files) => {
  const data = new FormData();

  data.append("file", files[0]);

  return fetchJson(
    new URL("convert", API_URL),
    {
      method: "POST",
      body: data
    }
  )
};

export {
  postConvert
};
