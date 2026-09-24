import React from "react";

function Explanation({
  riskScore = 0,
  prediction = "LOW",
  reasons = [],
  activities = []
}) {
  const score = Number(riskScore) || 0;
  const level = String(prediction || "LOW").toUpperCase();

  const riskColor =
    score >= 70 ? "#dc2626" :
    score >= 40 ? "#f59e0b" :
    "#16a34a";

  const status =
    score >= 70 ? "High Risk Activity" :
    score >= 40 ? "Suspicious Activity" :
    "Normal Activity";

  const riskTitle =
    score >= 70 ? "HIGH RISK" :
    score >= 40 ? "MEDIUM RISK" :
    "LOW RISK";

  const riskIcon =
    score >= 70 ? "🚨" :
    score >= 40 ? "⚠️" :
    "✅";

  const riskMessage =
    score >= 70
      ? "Multiple security events indicate potentially suspicious employee activity requiring immediate investigation."
      : score >= 40
      ? "The employee's activity shows unusual security events and should continue to be monitored."
      : "The employee's activity currently appears normal.";

  const action =
    score >= 70
      ? "Investigate the employee's recent security activity, review suspicious events and verify whether the activity is authorized."
      : score >= 40
      ? "Continue monitoring the employee and review recent security events for unusual behavior."
      : "Continue monitoring the employee's activity.";

  /* Create factors from actual live activities */
  const factors = [];

  if (Array.isArray(activities)) {
    const failed = activities.filter(a =>
      String(a.activity || a.action || "").toLowerCase().includes("failed")
    ).length;

    const usb = activities.filter(a =>
      String(a.activity || a.action || "").toLowerCase().includes("usb")
    ).length;

    const deleted = activities.filter(a =>
      String(a.activity || a.action || "").toLowerCase().includes("delete")
    ).length;

    const renamed = activities.filter(a =>
      String(a.activity || a.action || "").toLowerCase().includes("rename")
    ).length;

    const modified = activities.filter(a =>
      String(a.activity || a.action || "").toLowerCase().includes("modify")
    ).length;

    const login = activities.filter(a =>
      String(a.activity || a.action || "").toLowerCase().includes("login")
    ).length;

    if (failed > 0) {
      factors.push({
        icon: "🔐",
        title: "Failed Login Attempts",
        text: `${failed} failed login event${failed > 1 ? "s" : ""} detected.`,
        points: failed * 15
      });
    }

    if (usb > 0) {
      factors.push({
        icon: "🔌",
        title: "USB Device Activity",
        text: `${usb} USB-related event${usb > 1 ? "s" : ""} detected.`,
        points: usb * 20
      });
    }

    if (deleted > 0) {
      factors.push({
        icon: "🗑️",
        title: "File Deletion",
        text: `${deleted} file deletion event${deleted > 1 ? "s" : ""} detected.`,
        points: deleted * 15
      });
    }

    if (renamed > 0) {
      factors.push({
        icon: "✏️",
        title: "File Rename Activity",
        text: `${renamed} file rename event${renamed > 1 ? "s" : ""} detected.`,
        points: renamed * 10
      });
    }

    if (modified > 0) {
      factors.push({
        icon: "📝",
        title: "File Modification Activity",
        text: `${modified} file modification event${modified > 1 ? "s" : ""} detected.`,
        points: modified * 5
      });
    }
  }

  /* Use backend reasons if available */
  if (factors.length === 0 && Array.isArray(reasons) && reasons.length > 0) {
    reasons.forEach((reason) => {
      if (typeof reason === "string") {
        factors.push({
          icon: "⚠️",
          title: reason,
          text: "Security event contributing to the risk assessment.",
          points: ""
        });
      } else {
        factors.push({
          icon: reason.icon || "⚠️",
          title: reason.title || reason.factor || "Security Event",
          text:
            reason.description ||
            reason.message ||
            "Security event contributing to the risk assessment.",
          points: reason.score ?? reason.points ?? ""
        });
      }
    });
  }

  /* High-risk fallback */
  if (score >= 70 && factors.length === 0) {
    factors.push({
      icon: "🚨",
      title: "Elevated Security Risk",
      text: "The monitoring system has detected activity resulting in a high overall risk score.",
      points: score
    });
  }

  return (
    <section
      className="explanation-section"
      style={{
        width: "100%",
        boxSizing: "border-box",
        padding: "42px 38px 35px",
        background: "#ffffff",
        borderTop: "4px solid #009688",
        borderRadius: "0 0 28px 28px",
        marginTop: "28px"
      }}
    >

      {/* HEADER */}
      <div
        style={{
          textAlign: "center",
          marginBottom: "32px"
        }}
      >
        <h2
          style={{
            margin: 0,
            color: "#00796b",
            fontSize: "36px",
            fontWeight: 800
          }}
        >
          🧠 AI Decision Explanation
        </h2>

        <p
          style={{
            margin: "8px 0 0",
            color: "#6389a0",
            fontSize: "17px",
            fontWeight: 600
          }}
        >
          Explainable analysis of detected security events
        </p>
      </div>


      {/* SUMMARY */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
          gap: "18px",
          marginBottom: "22px"
        }}
      >

        <div
          style={{
            minHeight: "105px",
            border: "1px solid #b9e1e6",
            borderRadius: "18px",
            background: "#f9ffff",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center"
          }}
        >
          <span
            style={{
              color: "#7191a3",
              fontSize: "16px",
              fontWeight: 700
            }}
          >
            AI ANALYSIS STATUS
          </span>

          <strong
            style={{
              marginTop: "12px",
              color: riskColor,
              fontSize: "24px"
            }}
          >
            {status}
          </strong>
        </div>


        <div
          style={{
            minHeight: "105px",
            border: "1px solid #b9e1e6",
            borderRadius: "18px",
            background: "#f9ffff",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center"
          }}
        >
          <span
            style={{
              color: "#7191a3",
              fontSize: "16px",
              fontWeight: 700
            }}
          >
            RISK SCORE
          </span>

          <strong
            style={{
              marginTop: "12px",
              color: riskColor,
              fontSize: "24px"
            }}
          >
            {score}%
          </strong>
        </div>


        <div
          style={{
            minHeight: "105px",
            border: "1px solid #b9e1e6",
            borderRadius: "18px",
            background: "#f9ffff",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center"
          }}
        >
          <span
            style={{
              color: "#7191a3",
              fontSize: "16px",
              fontWeight: 700
            }}
          >
            AI PREDICTION
          </span>

          <strong
            style={{
              marginTop: "12px",
              color: riskColor,
              fontSize: "24px"
            }}
          >
            {level}
          </strong>
        </div>

      </div>


      {/* DETECTION REASONS */}
      <div
        style={{
          border: "1px solid #b9e1e6",
          borderRadius: "20px",
          background: "#fbffff",
          padding: "26px 22px 22px",
          marginBottom: "22px"
        }}
      >

        <div
          style={{
            textAlign: "center"
          }}
        >
          <h2
            style={{
              margin: 0,
              color: "#008577",
              fontSize: "31px",
              fontWeight: 800
            }}
          >
            🔎 Detection Reasons
          </h2>

          <p
            style={{
              margin: "7px 0 18px",
              color: "#6389a0",
              fontSize: "17px"
            }}
          >
            Security factors contributing to the current risk assessment
          </p>

          <div
            style={{
              height: "38px",
              borderRadius: "25px",
              background: "#e8f7f5",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#008577",
              fontWeight: 800,
              fontSize: "14px",
              marginBottom: "18px"
            }}
          >
            {factors.length} Factor{factors.length !== 1 ? "s" : ""}
          </div>
        </div>


        {factors.length > 0 ? (

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "10px"
            }}
          >

            {factors.map((factor, index) => (

              <div
                key={index}
                style={{
                  minHeight: "72px",
                  border: "1px solid #cce4e8",
                  borderRadius: "15px",
                  background: "#ffffff",
                  display: "flex",
                  alignItems: "center",
                  padding: "10px 16px",
                  boxSizing: "border-box"
                }}
              >

                <div
                  style={{
                    width: "46px",
                    height: "46px",
                    borderRadius: "12px",
                    background: "#fff1f1",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "23px",
                    flexShrink: 0
                  }}
                >
                  {factor.icon}
                </div>


                <div
                  style={{
                    flex: 1,
                    marginLeft: "14px"
                  }}
                >
                  <h3
                    style={{
                      margin: 0,
                      color: "#172033",
                      fontSize: "17px"
                    }}
                  >
                    {factor.title}
                  </h3>

                  <p
                    style={{
                      margin: "5px 0 0",
                      color: "#6a8ca0",
                      fontSize: "14px"
                    }}
                  >
                    {factor.text}
                  </p>
                </div>


                {factor.points !== "" && (
                  <div
                    style={{
                      padding: "10px 13px",
                      borderRadius: "10px",
                      background: "#fff0f0",
                      color: "#dc2626",
                      fontWeight: 800,
                      fontSize: "14px"
                    }}
                  >
                    +{factor.points}
                  </div>
                )}

              </div>

            ))}

          </div>

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "22px 10px 12px"
            }}
          >
            <div
              style={{
                width: "54px",
                height: "54px",
                margin: "0 auto 12px",
                borderRadius: "50%",
                background: "#e9f9f0",
                color: "#16a34a",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "30px"
              }}
            >
              ✓
            </div>

            <h3
              style={{
                margin: "0 0 8px",
                color: "#172033",
                fontSize: "21px"
              }}
            >
              No specific suspicious events identified
            </h3>

            <p
              style={{
                margin: 0,
                color: "#6a8ca0",
                fontSize: "16px"
              }}
            >
              The current risk level is based on the overall monitored activity.
            </p>
          </div>

        )}

      </div>


      {/* FINAL RISK */}
      <div
        style={{
          border: "1px solid #c9e8d5",
          borderRadius: "20px",
          background: score >= 70 ? "#fff8f8" : "#f7fcf8",
          minHeight: "145px",
          display: "grid",
          gridTemplateColumns: "220px 220px 1fr",
          alignItems: "center",
          padding: "22px 30px",
          boxSizing: "border-box",
          marginBottom: "20px"
        }}
      >

        <div style={{ textAlign: "center" }}>
          <span
            style={{
              color: "#7191a3",
              fontSize: "15px",
              fontWeight: 700
            }}
          >
            FINAL RISK SCORE
          </span>

          <strong
            style={{
              display: "block",
              marginTop: "5px",
              color: riskColor,
              fontSize: "40px",
              fontWeight: 800
            }}
          >
            {score}%
          </strong>
        </div>


        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "9px"
          }}
        >
          <span style={{ fontSize: "25px" }}>
            {riskIcon}
          </span>

          <strong
            style={{
              color: "#172033",
              fontSize: "22px"
            }}
          >
            {riskTitle}
          </strong>
        </div>


        <div
          style={{
            color: "#4f6880",
            fontSize: "16px",
            lineHeight: 1.5
          }}
        >
          {riskMessage}
        </div>

      </div>


      {/* RECOMMENDED ACTION */}
      <div
        style={{
          minHeight: "78px",
          border: "1px solid #cce4e8",
          borderRadius: "17px",
          background: "#faffff",
          display: "flex",
          alignItems: "center",
          padding: "12px 20px",
          boxSizing: "border-box"
        }}
      >

        <div
          style={{
            width: "48px",
            height: "48px",
            borderRadius: "12px",
            background: "#eaf7f7",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "24px",
            flexShrink: 0
          }}
        >
          🛡️
        </div>

        <div style={{ marginLeft: "15px" }}>

          <h3
            style={{
              margin: 0,
              color: "#172033",
              fontSize: "17px"
            }}
          >
            Recommended Action
          </h3>

          <p
            style={{
              margin: "5px 0 0",
              color: "#6389a0",
              fontSize: "14px"
            }}
          >
            {action}
          </p>

        </div>

      </div>

    </section>
  );
}

export default Explanation;