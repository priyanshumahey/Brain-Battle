const express = require('express');
const router = express.Router();
const { promisify } = require('util');
const { Neurosity } = require("@neurosity/sdk");
require("dotenv").config();

// Refer to https://console.neurosity.co/dashboard to get the missing info
const deviceId = process.env.DEVICE_ID || "";
const email = process.env.EMAIL || "";
const password = process.env.PASSWORD || "";

const verifyEnvs = (email, password, deviceId) => {
    const invalidEnv = (env) => {
        return env === "" || env === 0;
    };
    if (invalidEnv(email) || invalidEnv(password) || invalidEnv(deviceId)) {
        console.error(
        "Please verify deviceId, email and password are in .env file, quitting..."
        );
        process.exit(0);
    }
};

const neurosity = new Neurosity({
    deviceId
});

const loggIn = async () => {
    verifyEnvs(email, password, deviceId);
    await neurosity
      .login({
        email,
        password
      })
      .catch((error) => {
        if (error === "Already logged in.") return
        throw new Error(error);
      });
};

/* GET brain activity data */
router.get("/", async function(req, res, next) {
    loggIn();
    let focusLevels = [];
    const subscription = neurosity.brainwaves("powerByBand").subscribe((brainwaves) => {
        focusLevels.push(brainwaves.data);
    });

    try {
        const setTimeoutPromise = promisify(setTimeout);
        await setTimeoutPromise(5000);
        subscription.unsubscribe();
    } catch (error) {
        // Handle any errors that may occur during the delay
        console.error("Error during delay:", error);
    }

    res.json(focusLevels);
});

module.exports = router;