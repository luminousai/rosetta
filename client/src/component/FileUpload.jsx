import React from "react";
import { useDropzone } from "react-dropzone";

import { styled } from "@mui/system";

const Root = styled("div")(theme => ({

}));

const FileUpload = ({ children }) => {
  const { getRootProps, getInputProps } = useDropzone({
    accept: {""}
  });

  return (
    <Root>

    </Root>
  );
};

export default FileUpload;
