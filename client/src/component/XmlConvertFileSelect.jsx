import React from "react";
import { useDropzone } from "react-dropzone";

import ClearIcon from "@mui/icons-material/Clear";
import FileUploadOutlinedIcon from "@mui/icons-material/FileUploadOutlined";
import InsertDriveFileOutlinedIcon from "@mui/icons-material/InsertDriveFileOutlined";

import IconButton from "@mui/material/IconButton";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import { alpha } from "@mui/material";
import { styled } from "@mui/system";

const FileDropzone = styled("div")(({ theme, isDragActive, hasRejections }) => {
  const color = (
    hasRejections
      ? theme.palette.error.main
      : theme.palette.primary.main
  );

  const backgroundIntensity = isDragActive ? 0.07 : 0;

  return ({
    padding: 80,
    backgroundColor: alpha(color, backgroundIntensity),
    borderStyle: "dashed",
    borderWidth: 1.5,
    borderColor: color,
    borderRadius: 4,
    transition: "all .3s ease-out",
  
    "&:hover": {
      cursor: "pointer"
    },
  
    "& > div": {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
  
      "& > svg": {
        color: color,
        fontSize: 60,
        marginBottom: 30
      }
    }
  });
});

const XmlConvertFileSelect = ({ state, onSelect, onClear }) => {
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    fileRejections
  } = useDropzone({
    onDrop: onSelect,
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"]
    },
    multiple: false
  });

  const handleClearIconClick = () => {
    onClear();
  };

  const hasRejections = fileRejections.length > 0;

  const fileList = (() => {
    if (state.length === 0) {
      return null;
    }

    return (
      <List>
        {state.map(({ file: { name } }) => (
          <Paper key={name} component="li" variant="outlined">
            <ListItem
              component="div"
              secondaryAction={(
                <IconButton edge="end" onClick={handleClearIconClick}>
                  <ClearIcon />
                </IconButton>
              )}
            >
              <ListItemIcon>
                <InsertDriveFileOutlinedIcon />
              </ListItemIcon>
              <ListItemText primary={name} />
            </ListItem>
          </Paper>
        ))}
      </List>
    );
  })();

  return (
    <div>
      <FileDropzone {...getRootProps({ isDragActive, hasRejections })}>
        <input {...getInputProps()} />
        <div>
          <FileUploadOutlinedIcon />
          <Typography variant="body1" color="grey" fontWeight="bold">
            Get started by uploading your files
          </Typography>
          <Typography variant="body2" color="grey">
            {
              hasRejections
                ? "Only XLSX files are supported"
                : "Drag and drop your files here or click to browse"
            }
          </Typography>
        </div>
      </FileDropzone>
      {fileList}
    </div>
  );
};

export default XmlConvertFileSelect;
