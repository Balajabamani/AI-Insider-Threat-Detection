import "./App.css";
import { useEffect, useState } from "react";

import Charts from "./Charts";
import Alerts from "./Alerts";
import RiskTable from "./RiskTable";
import EmployeeStatus from "./EmployeeStatus";
import Explanation from "./Explanation";

import {
  CircularProgressbar,
  buildStyles
} from "react-circular-progressbar";

import "react-circular-progressbar/dist/styles.css";


function App() {

  // =====================================================
  // DASHBOARD DATA
  // =====================================================

  const [data, setData] = useState({

    login_events: 0,

    file_events: 0,

    usb_events: 0,

    failed_logins: 0,

    total_events: 0,

    prediction: "LOW",

    risk_score: 0,

    risk_level: "LOW",

    detection_reasons: [],

    suspicious_event_count: 0,

    employee: {
      name: "Alice",
      department: "Finance",
      role: "Accountant",
      login_hour: 0,
      files_opened: 0,
      usb_used: 0,
      failed_logins: 0
    },

    activities: []

  });


  // =====================================================
  // REAL-TIME DASHBOARD UPDATE
  // =====================================================

  useEffect(() => {

    const loadDashboard = () => {

      fetch("http://127.0.0.1:8000/dashboard")

        .then((response) => {

          if (!response.ok) {

            throw new Error(
              "Dashboard request failed"
            );

          }

          return response.json();

        })

        .then((result) => {

          setData((previous) => ({

            ...previous,

            ...result,


            // -----------------------------------------
            // EVENT COUNTS
            // -----------------------------------------

            login_events:
              result.login_events ??
              previous.login_events,


            file_events:
              result.file_events ??
              previous.file_events,


            usb_events:
              result.usb_events ??
              previous.usb_events,


            failed_logins:
              result.failed_logins ??
              previous.failed_logins,


            // -----------------------------------------
            // TOTAL EVENTS
            // -----------------------------------------

            total_events:
              result.total_events ??
              (
                (result.login_events ?? 0) +
                (result.file_events ?? 0) +
                (result.usb_events ?? 0) +
                (result.failed_logins ?? 0)
              ),


            // -----------------------------------------
            // AI PREDICTION
            // -----------------------------------------

            prediction:
              result.prediction ??
              previous.prediction,


            // -----------------------------------------
            // RISK SCORE
            // -----------------------------------------

            risk_score:
              result.risk_score ??
              previous.risk_score,


            risk_level:
              result.risk_level ??
              previous.risk_level,


            // -----------------------------------------
            // AI DETECTION REASONS
            // -----------------------------------------

            detection_reasons:
              result.detection_reasons ??
              previous.detection_reasons,


            suspicious_event_count:
              result.suspicious_event_count ??
              previous.suspicious_event_count,


            // -----------------------------------------
            // EMPLOYEE
            // -----------------------------------------

            employee:
              result.employee ??
              previous.employee,


            // -----------------------------------------
            // REAL-TIME ACTIVITIES
            // -----------------------------------------

            activities:
              result.activities ??
              previous.activities

          }));

        })

        .catch((error) => {

          console.error(
            "Dashboard update error:",
            error
          );

        });

    };


    // Load immediately
    loadDashboard();


    // Refresh every 2 seconds
    const interval = setInterval(
      loadDashboard,
      2000
    );


    return () => {

      clearInterval(interval);

    };

  }, []);


  // =====================================================
  // SAFE EVENT VALUES
  // =====================================================

  const loginEvents =
    Number(
      data.login_events ?? 0
    );


  const fileEvents =
    Number(
      data.file_events ?? 0
    );


  const usbEvents =
    Number(
      data.usb_events ?? 0
    );


  const failedLogins =
    Number(
      data.failed_logins ?? 0
    );


  const totalEvents =
    Number(
      data.total_events ??
      (
        loginEvents +
        fileEvents +
        usbEvents +
        failedLogins
      )
    );


  // =====================================================
  // SAFE RISK SCORE
  // =====================================================

  const riskScore =
    Math.max(
      0,
      Math.min(
        100,
        Number(
          data.risk_score ?? 0
        )
      )
    );


  // =====================================================
  // EMPLOYEE
  // =====================================================

  const employee =
    data.employee || {};


  // =====================================================
  // AI PREDICTION
  // =====================================================

  const prediction =
    data.prediction ||
    data.risk_level ||
    "LOW";


  // =====================================================
  // DETECTION REASONS
  // =====================================================

  const detectionReasons =
    Array.isArray(
      data.detection_reasons
    )
      ? data.detection_reasons
      : [];


  // =====================================================
  // RISK COLOR
  // =====================================================

  const getRiskColor = () => {

    if (riskScore >= 70) {

      return "#dc2626";

    }


    if (riskScore >= 40) {

      return "#f59e0b";

    }


    return "#16a34a";

  };


  // =====================================================
  // RISK MESSAGE
  // =====================================================

  const getRiskMessage = () => {

    if (riskScore >= 70) {

      return "⚠ Immediate Threat Detected";

    }


    if (riskScore >= 40) {

      return "⚠ Activity Requires Monitoring";

    }


    return "✓ No Immediate Threat";

  };


  // =====================================================
  // DISPLAY TOTAL
  // =====================================================

  const displayedTotal =
    totalEvents ||
    (
      loginEvents +
      fileEvents +
      usbEvents +
      failedLogins
    );


  // =====================================================
  // UI
  // =====================================================

  return (

    <div className="app">


      {/* =================================================
          HEADER
          ================================================= */}

      <header className="dashboard-header">

        <div className="header-left">

          <div className="shield-icon">
            🛡️
          </div>

        </div>


        <div className="header-title">

          <h1>

            AI Insider Threat Detection

            <br />

            Dashboard

          </h1>


          <p>
            Real-Time Employee Security Monitoring
          </p>

        </div>


        <div className="monitoring-status">

          <span className="status-pulse"></span>

          <span>
            SYSTEM MONITORING ACTIVE
          </span>

        </div>

      </header>



      {/* =================================================
          SUMMARY CARDS
          ================================================= */}

      <section className="summary-grid">


        {/* TOTAL EVENTS */}

        <div className="summary-card">

          <div className="summary-icon">
            📊
          </div>

          <div className="summary-content">

            <h3>
              Total Events
            </h3>

            <strong>
              {displayedTotal}
            </strong>

          </div>

        </div>



        {/* LOGIN EVENTS */}

        <div className="summary-card">

          <div className="summary-icon">
            🔐
          </div>

          <div className="summary-content">

            <h3>
              Login Events
            </h3>

            <strong>
              {loginEvents}
            </strong>

          </div>

        </div>



        {/* FILE EVENTS */}

        <div className="summary-card">

          <div className="summary-icon">
            📁
          </div>

          <div className="summary-content">

            <h3>
              File Events
            </h3>

            <strong>
              {fileEvents}
            </strong>

          </div>

        </div>



        {/* USB EVENTS */}

        <div className="summary-card">

          <div className="summary-icon">
            🔌
          </div>

          <div className="summary-content">

            <h3>
              USB Events
            </h3>

            <strong>
              {usbEvents}
            </strong>

          </div>

        </div>

      </section>



      {/* =================================================
          AI PREDICTION + EMPLOYEE DETAILS
          ================================================= */}

      <section className="main-information-grid">


        {/* =================================================
            AI THREAT PREDICTION
            ================================================= */}

        <div className="prediction-card">

          <h2>

            🤖

            <span>
              AI Threat Prediction
            </span>

          </h2>


          <div className="risk-circle">

            <CircularProgressbar

              value={riskScore}

              text={`${riskScore}%`}

              styles={buildStyles({

                pathColor:
                  getRiskColor(),

                textColor:
                  "#172033",

                trailColor:
                  "#dceff1",

                textSize:
                  "28px",

                pathTransitionDuration:
                  0.5

              })}

            />

          </div>


          <div

            className="prediction-status"

            style={{
              color:
                getRiskColor()
            }}

          >

            {prediction}

          </div>


          <div className="prediction-message">

            {getRiskMessage()}

          </div>


          <p className="prediction-subtext">

            AI-based analysis of monitored
            employee activity

          </p>

        </div>



        {/* =================================================
            EMPLOYEE DETAILS
            ================================================= */}

        <div className="employee-details-card">

          <h2>

            👤

            <span>
              Employee Details
            </span>

          </h2>


          <div className="employee-profile">

            <div className="employee-avatar">
              👤
            </div>


            <h3>
              {employee.name || "Alice"}
            </h3>


            <p>
              {employee.department || "Finance"}
            </p>

          </div>



          <div className="employee-stat-grid">


            {/* ROLE */}

            <div className="employee-stat">

              <span>
                Role
              </span>

              <strong>
                {employee.role ||
                  "Accountant"}
              </strong>

            </div>



            {/* LOGIN HOUR */}

            <div className="employee-stat">

              <span>
                Login Hour
              </span>

              <strong>
                {employee.login_hour ??
                  0}
              </strong>

            </div>



            {/* FILES */}

            <div className="employee-stat">

              <span>
                Files Opened
              </span>

              <strong>
                {employee.files_opened ??
                  fileEvents}
              </strong>

            </div>



            {/* USB */}

            <div className="employee-stat">

              <span>
                USB Used
              </span>

              <strong>
                {employee.usb_used ??
                  usbEvents}
              </strong>

            </div>



            {/* FAILED LOGINS */}

            <div className="employee-stat">

              <span>
                Failed Logins
              </span>

              <strong>
                {employee.failed_logins ??
                  failedLogins}
              </strong>

            </div>

          </div>

        </div>

      </section>



      {/* =================================================
          RECENT SYSTEM ACTIVITY
          ================================================= */}

      <section className="activity-section">

        <div className="activity-header">

          <div className="activity-heading">

            <h2>

              🕘

              <span>
                Recent System Activity
              </span>

            </h2>


            <p>
              Real-time monitored security events
            </p>

          </div>


          <div className="live-badge">

            <span></span>

            <strong>
              LIVE
            </strong>

          </div>

        </div>



        <div className="activity-list">

          {data.activities &&
          data.activities.length > 0 ? (

            data.activities
              .slice(0, 20)
              .map((item, index) => (

                <div

                  className="activity-row"

                  key={
                    `${item.time}-${item.activity}-${index}`
                  }

                >

                  <div className="activity-time">

                    {item.time}

                  </div>


                  <div className="activity-name">

                    {item.activity}

                  </div>

                </div>

              ))

          ) : (

            <div className="no-activity">

              No recent system activity

            </div>

          )}

        </div>

      </section>



      {/* =================================================
          ACTIVITY ANALYTICS
          ================================================= */}

      <section className="analytics-section">

        <div className="analytics-heading">

          <h2>

            📊

            <span>
              Activity Analytics
            </span>

          </h2>


          <p>
            Real-time security event visualization
          </p>

        </div>


        <div className="charts-grid">

          <Charts
            data={data}
          />

        </div>

      </section>



      {/* =================================================
          ALERTS + RISK RANKING
          ================================================= */}

      <section className="bottom-grid">


        {/* LIVE SECURITY ALERTS */}

        <div className="alerts-wrapper">

          <Alerts

            activities={
              data.activities || []
            }

          />

        </div>



        {/* EMPLOYEE RISK RANKING */}

        <div className="risk-table-wrapper">

          <RiskTable />

        </div>

      </section>



      {/* =================================================
          EMPLOYEE STATUS
          ================================================= */}

      <section className="status-section">

        <EmployeeStatus />

      </section>



      {/* =================================================
          AI EXPLANATION
          ================================================= */}

      <section className="explanation-wrapper">

        <Explanation

          riskScore={riskScore}

          prediction={prediction}

          reasons={detectionReasons}

          activities={
            data.activities || []
          }

        />

      </section>



      {/* =================================================
          FOOTER
          ================================================= */}

      <footer className="dashboard-footer">

        <span>
          🛡 AI Insider Threat Detection System
        </span>


        <span>
          Real-Time Monitoring Enabled
        </span>

      </footer>


    </div>

  );

}


export default App;