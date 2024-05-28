import React, { useState, useEffect } from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import Card from "@mui/material/Card";
import CardMedia from "@mui/material/CardMedia";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import doctor1 from "./components/doctor1.jpg";
import { FiberManualRecord, Stop } from "@mui/icons-material";
import axios from "axios";
import RecordRTC, { StereoAudioRecorder } from "recordrtc";
import "./App.css";

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [themeProfile, setThemeProfile] = useState("tiramisu");
  const [recorder, setRecorder] = useState<RecordRTC | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  
  const sessionID = new Date().getTime().toString();


  useEffect(() => {
    document.body.className = `${
      darkMode ? "dark-mode" : "light-mode"
    } ${themeProfile}`;
  }, [darkMode, themeProfile]);

  const theme = createTheme({
    palette: {
      mode: darkMode ? "dark" : "light",
      primary: {
        main: getComputedStyle(document.documentElement)
          .getPropertyValue("--primary-color")
          .trim(),
      },
      background: {
        default: getComputedStyle(document.documentElement)
          .getPropertyValue("--background-color")
          .trim(),
        paper: getComputedStyle(document.documentElement)
          .getPropertyValue("--box-background-color")
          .trim(),
      },
      text: {
        primary: getComputedStyle(document.documentElement)
          .getPropertyValue("--text-color")
          .trim(),
      },
    },
    typography: {
      fontFamily: "Poppins, sans-serif",
      allVariants: {
        textTransform: "lowercase",
        fontWeight: 400,
      },
    },
  });

  const handleToggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem("darkMode", newDarkMode.toString());
  };

  const handleMenuToggle = () => {
    setMenuOpen(!menuOpen);
  };


  const handleThemeProfileChange = (event: SelectChangeEvent<string>) => {
    const selectedTheme = event.target.value;
    setThemeProfile(selectedTheme);
    localStorage.setItem("themeProfile", selectedTheme);
  };

  useEffect(() => {
    const savedDarkMode = localStorage.getItem("darkMode");
    if (savedDarkMode !== null) {
      setDarkMode(savedDarkMode === "true");
    }
  
    const savedThemeProfile = localStorage.getItem("themeProfile");
    if (savedThemeProfile !== null) {
      setThemeProfile(savedThemeProfile);
    }
  }, []);
  
  useEffect(() => {
    // Set up the recorder
    const requestMicrophoneAccess = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        const recorder = new RecordRTC(stream, {
          type: "audio",
          mimeType: "audio/wav",
          recorderType: StereoAudioRecorder,
          numberOfAudioChannels: 1,
          desiredSampRate: 16000,
        });
        setRecorder(recorder);
      } catch (error) {
        console.error("Failed to get microphone access:", error);
      }
    };

    requestMicrophoneAccess();
  }, []);

  const startRecording = () => {
    recorder?.startRecording();
    setIsRecording(true);
  };

  const stopRecording = async () => {
    recorder?.stopRecording(() => {
      const blob = recorder.getBlob();
      sendAudioToServer(blob);
      recorder.reset(); // Reset or destroy the recorder if necessary
      setupRecorder(); // Setup the recorder again for a new session
    });
    setIsRecording(false);
  };

  let mediaStream: MediaStream; // Keep a reference to the stream

  const setupRecorder = async () => {
    if (mediaStream) {
      mediaStream.getTracks().forEach((track) => track.stop()); // Stop all tracks before starting a new one
    }
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      const newRecorder = new RecordRTC(mediaStream, {
        type: "audio",
        mimeType: "audio/wav",
        recorderType: StereoAudioRecorder,
        numberOfAudioChannels: 1,
        desiredSampRate: 16000,
      });
      setRecorder(newRecorder);
    } catch (error) {
      console.error("Failed to get microphone access:", error);
    }
  };
  const sendAudioToServer = async (audioBlob: Blob) => {
    try {
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");
      formData.append("language", "vi-VN");
      formData.append("voice_name", "vi-VN-Neural2-D");
      formData.append("voice_gender", "MALE");
      formData.append("session_id", sessionID || "new");

      const response = await axios.post(
        "http://ec2-54-198-198-28.compute-1.amazonaws.com:8000/session-conversation/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      const { transcript, audio } = response.data;
      // Handle the received transcript and audio
      setTranscript(transcript);
      console.log("Transcript:", transcript);
      playReceivedAudio(audio);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const playReceivedAudio = (audioBase64: string) => {
    const audioBlob = base64ToBlob(audioBase64, "audio/mp3");
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
  };

  const base64ToBlob = (base64Data: string, contentType: string): Blob => {
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: contentType });
  };

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ flexGrow: 1, position: "relative", minHeight: "100vh" }}>
        <AppBar position="fixed" color="inherit" sx={{ zIndex: 1400 }}>
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              aria-label="menu"
              onClick={handleMenuToggle}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Health<span style={{ fontWeight: "bold" }}>buddy</span>
            </Typography>
            <IconButton color="inherit" onClick={handleToggleDarkMode}>
              {darkMode ? <DarkModeIcon /> : <LightModeIcon />}
            </IconButton>
          </Toolbar>
        </AppBar>
        {menuOpen && (
          <Box
            className={`dropdown-menu ${menuOpen ? "open" : ""}`}
            sx={{ zIndex: 1300 }}
          >
            <FormControl fullWidth margin="normal">
              <InputLabel>Color</InputLabel>
              <Select value={themeProfile} onChange={handleThemeProfileChange}>
                <MenuItem value="tiramisu">Tiramisu</MenuItem>
                <MenuItem value="alpine">Alpine</MenuItem>
                <MenuItem value="dracula">Dracula</MenuItem>
                <MenuItem value="black-and-white">Black & White</MenuItem>
              </Select>
            </FormControl>
          </Box>
        )}
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            minHeight: "calc(100vh - 64px)",
          }}
        >
          <Card
            sx={{ maxWidth: 405, maxHeight: 700, mt: 8, zIndex: 1200, position: "relative" }}
          >
            <IconButton
              color="inherit"
              onClick={startRecording}
              sx={{ position: "absolute", top: 5, left: 5 }}
            >
              <FiberManualRecord
                sx={{ color: isRecording ? "grey" : "red", fontSize: "3rem" }}
              />
            </IconButton>
            <IconButton
              color="inherit"
              onClick={stopRecording}
              sx={{ position: "absolute", top: 5, right: 5 }}
            >
              <Stop sx={{ fontSize: "3rem" }} />
            </IconButton>
            <CardMedia
              component="img"
              height="140"
              image={doctor1}
              alt="doctor"
              sx={{ width: "100%", height: "auto" }} // Ensure the image covers the card area
            />
            <Box
              sx={{
                position: "absolute",
                bottom: 0,
                width: "100%",
                textAlign: "center",
                bgcolor: "rgba(0, 0, 0, 0.7)",
                color: "white",
                padding: "8px",
              }}
            >
              {isRecording ? "Recording..." : "Tap record to start"}
            </Box>
          </Card>
        </Box>
        <Typography
          variant="body2"
          color="textSecondary"
          component="p"
          sx={{
            textAlign: "center",
            bgcolor: "rgba(0, 0, 0, 0.7)",
            color: "white",
            padding: 1,
          }}
        >
          {transcript || "No caption available"} 
        </Typography>
      </Box>
    </ThemeProvider>
  );
};

export default App;
