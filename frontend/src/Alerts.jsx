function Alerts({ activities = [] }) {

  // ============================================================
  // DETERMINE ALERT SEVERITY
  // ============================================================

  const getSeverity = (activity) => {

    const text = String(
      activity?.activity || ""
    ).toLowerCase();


    // ----------------------------------------------------------
    // HIGH RISK EVENTS
    // ----------------------------------------------------------

    if (
      text.includes("failed login") ||
      text.includes("failed") ||
      text.includes("deleted") ||
      text.includes("connected") ||
      text.includes("usb")
    ) {

      return {
        level: "HIGH",
        color: "#dc2626",
        icon: "🚨"
      };

    }


    // ----------------------------------------------------------
    // MEDIUM RISK EVENTS
    // ----------------------------------------------------------

    if (
      text.includes("renamed") ||
      text.includes("rename")
    ) {

      return {
        level: "MEDIUM",
        color: "#f59e0b",
        icon: "🟠"
      };

    }


    // ----------------------------------------------------------
    // NORMAL / LOW RISK EVENTS
    // ----------------------------------------------------------

    return {
      level: "LOW",
      color: "#2563eb",
      icon: "🔵"
    };

  };


  // ============================================================
  // SHOW ONLY LATEST 10 EVENTS
  // ============================================================

  const latestActivities = activities
    .slice(0, 10);


  // ============================================================
  // UI
  // ============================================================

  return (

    <div className="alerts">

      <h2>
        🚨 Live Security Alerts
      </h2>


      <table>

        <thead>

          <tr>

            <th>
              Severity
            </th>

            <th>
              Alert
            </th>

            <th>
              Time
            </th>

          </tr>

        </thead>


        <tbody>

          {latestActivities.length > 0 ? (

            latestActivities.map(
              (item, index) => {

                const severity =
                  getSeverity(item);


                return (

                  <tr
                    key={`${item.time}-${item.activity}-${index}`}
                  >

                    {/* =========================
                        SEVERITY
                    ========================== */}

                    <td
                      style={{
                        color:
                          severity.color,

                        fontWeight:
                          "bold"
                      }}
                    >

                      {severity.icon}{" "}

                      {severity.level}

                    </td>


                    {/* =========================
                        ALERT
                    ========================== */}

                    <td>

                      {item.activity}

                    </td>


                    {/* =========================
                        TIME
                    ========================== */}

                    <td>

                      {item.time}

                    </td>

                  </tr>

                );

              }

            )

          ) : (

            <tr>

              <td
                colSpan="3"
                style={{
                  textAlign: "center",
                  padding: "30px"
                }}
              >

                No security alerts detected.

              </td>

            </tr>

          )}

        </tbody>

      </table>

    </div>

  );

}


export default Alerts;