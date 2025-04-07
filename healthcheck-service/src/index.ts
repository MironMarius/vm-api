import axios from "axios";
import dotenv from "dotenv";

// Load environment variables from .env
dotenv.config();

const API_URL = process.env.API_URL;
const MACHINE_ID = process.env.MACHINE_ID;

if (!API_URL) {
  console.error("API_URL environment variable not set");
  process.exit(1);
}

if (!MACHINE_ID) {
  console.error("MACHINE_ID environment variable not set");
  process.exit(1);
}

const healthcheckEndpoint: string = `${API_URL}/healthcheck/${MACHINE_ID}`;
async function sendHealthcheck(): Promise<void> {
  try {
    console.log(`Sending POST request to ${healthcheckEndpoint}`);
    const response = await axios.post(healthcheckEndpoint);
    console.log(`Healthcheck success: ${response.status}`);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error(`Axios error: ${error.message}`);
    } else {
      console.error(`Unexpected error: ${error}`);
    }
  }
}

// Send the first healthcheck immediately
sendHealthcheck();

// Schedule subsequent healthchecks every 30 seconds
setInterval(sendHealthcheck, 30 * 1000);
