import React, { useState } from "react";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import Stepper from "@mui/material/Stepper";

import * as Api from "../api";
import XmlConversionStatus from "./XmlConversionStatus";
import XmlFileConversionState from "./XmlFileConversionState";
import XmlConvertFileSelect from "./XmlConvertFileSelect";

const XmlConvert = () => {
  const steps = [
    { label: "Upload files" },
    { label: "Review & Export" }
  ];

  const [activeStep, setActiveStep] = useState(0);
  const [conversionState, setConversionState] = useState([]);

  const handleFileSelect = async (acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      return;
    }

    const conversionState = acceptedFiles.map(file => (
      XmlFileConversionState({
        id: file.name,
        status: XmlConversionStatus.PROCESSING,
        file
      })
    ));

    setConversionState(conversionState);

    const response = await Api.postConvert(acceptedFiles);

    console.log(response);
  };

  const handleFileClear = () => {
    setConversionState([]);
  };

  const content = (() => {
    if (activeStep === 0) {
      return (
        <XmlConvertFileSelect
          state={conversionState}
          onSelect={handleFileSelect}
          onClear={handleFileClear}
        />
      )
    } else if (activeStep === 1) {
      return null;
    }

    return null;
  })();

  const nextButtonDisabled = (() => {
    if (activeStep === 0) {
      if (conversionState.length === 0) {
        return true;
      }

      const ready = conversionState.every(
        ({ status }) => status === XmlConversionStatus.SUCCESS
      );

      return !ready;
    }

    return false;
  })();

  return (
    <>
      <Stepper activeStep={activeStep} sx={{ pt: 3, pb: 5 }}>
        {steps.map(({ label }) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <Box>
        {content}
      </Box>
      <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
        {activeStep !== 0 && (
          <Button sx={{ mt: 3, ml: 1 }}>
            Back
          </Button>
        )}
        <Button
          variant="contained"
          sx={{ mt: 3, ml: 1 }}
          disabled={nextButtonDisabled}
        >
          {activeStep === steps.length - 1 ? 'Place order' : 'Next'}
        </Button>
      </Box>
    </>
  );
};

export default XmlConvert;
